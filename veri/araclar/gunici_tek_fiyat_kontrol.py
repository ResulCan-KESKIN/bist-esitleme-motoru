"""Gun ici emir verisinden tek fiyat (muzayede) defterini yeniden kurup denge fiyatini hesaplar,
gerceklesen islem fiyati ve miktariyla karsilastirir (03-tek-fiyat.md Bolum D).

Muzayede: bir islem sirasinda emir toplama durumlarindan (TOPLAMA) sonra gelen eslestirme durumu
(ESLESTIRME) satirlari. Eslestirme ani M = ilk ESLESTIRME satirinin zamani; eslestirme satiri yoksa
(islem ve iptal olmadi) M = son toplama satiri + 1 us. Defter: M'den once her emrin son satiri,
emir_durumu = 1 ve kalan > 0. Piyasa emri (fiyat turu 2) ve fiyatsiz piyasadan limite (3, fiyat 0)
piyasa emri gibi; dengeleyici (66) ve orta nokta (emir turu 64) haric.
Referans adaylari: baz (onceki kapanis), son islem (M'den onceki son surekli/muzayede islemi).
Sinirli varyant: gunluk fiyat sinirlari; kapanis seansinda ayrica son islem fiyatinin +-%3'u (ice yuvarlanmis).
Kullanim: python -I gunici_tek_fiyat_kontrol.py GUNLUK_EMIR_KLASORU ISLEM.parquet GUNSONU.parquet CIKTI
"""
import sys, os, glob, datetime
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tek_fiyat_algoritma import denge, GRUP_TABLO, yukari_adim, asagi_adim

emir_dir, islem_src, gs_src, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
TOPLAMA = {"P_ACILIS_EMIR_TPL", "P_ACS_EMR_TP_EIY", "P_ACS_EMR_TP2_PY", "P_ACS_EMR_TP2_PY_EIY",
           "P_KAPANIS_EMIR_TPL", "P_KAPANIS_EMIR_TPL2", "P_TEKFIYAT_EMIR_TPL", "P_TEKFIYAT_EMIR_TPL2",
           "P_DK_TEKFIY_EMIR_TPL", "P_DK_TEKFIY_EMR_TPL2", "P_TF_EMIR_TPL_EBDK", "P_TF_EMIR_TPL2_EBDK"}
ESLESTIRME = {"P_ESLESTIRME", "P_ESLESTIRMETEKFIYAT", "P_ESLESTIRME_EBDK"}
MARJ = 0.10  # Mart 2025 verisinden (gunici_fiyat_adimi_sinir_kontrol.py); tarihe bagli parametre
cols = ["islem_kodu", "emir_no", "emir_giris_zamani", "emir_degistirilme_zamani", "alis_satis",
        "emir_fiyat_turu", "emir_turu", "emir_kategorisi", "emir_durumu", "degisiklik_sebebi",
        "kalan_miktar", "fiyat", "seans", "guncelleme_no"]

gs = pd.read_parquet(gs_src, columns=["trade_date", "instrument_series_code", "instrument_group",
                                      "market_segment", "previous_last_price"])
gs = gs.rename(columns={"trade_date": "tarih", "instrument_series_code": "islem_kodu"}).set_index(["tarih", "islem_kodu"])
ipf = pq.ParquetFile(islem_src)
iidx = ipf.schema_arrow.get_field_index("tarih")


def islemler(d):
    rgs = [i for i in range(ipf.num_row_groups)
           if ipf.metadata.row_group(i).column(iidx).statistics.min <= d <= ipf.metadata.row_group(i).column(iidx).statistics.max]
    t = ipf.read_row_groups(rgs, columns=["tarih", "islem_kodu", "alis_satis", "islem_adedi", "islem_fiyati",
                                         "islem_zamani", "seans", "normal_islem", "ortak_sozlesme_no"])
    t = t.filter(pc.and_(pc.equal(t["tarih"], pa.scalar(d)), pc.equal(t["alis_satis"], "A")))
    df = t.to_pandas()
    df = df[~df["normal_islem"].isin([3, 5])]
    df["zaman"] = pd.to_datetime(str(d) + " " + df["islem_zamani"])
    df["fiyat_m"] = np.rint(df["islem_fiyati"] * 1000).astype(np.int64)
    return df.sort_values(["islem_kodu", "zaman", "ortak_sozlesme_no"])


def muzayedeler(g):
    """g: tek sira, zamana gore sirali. (tur, M, eslesme_var) listesi."""
    s = g["seans"].to_numpy()
    t = g["emir_degistirilme_zamani"].to_numpy()
    out, i, n = [], 0, len(g)
    while i < n:
        if s[i] in TOPLAMA:
            j = i
            while j < n and s[j] in TOPLAMA:
                j += 1
            tur = s[j - 1]
            if j < n and s[j] in ESLESTIRME:
                out.append((tur, t[j], True))
                k = j
                while k < n and s[k] in ESLESTIRME:
                    k += 1
                i = k
            else:
                out.append((tur, t[j - 1] + np.timedelta64(1, "us"), False))
                i = j
        else:
            i += 1
    return out


def sinif(tur, M):
    h = pd.Timestamp(M).hour
    if tur.startswith("P_ACILIS") or tur.startswith("P_ACS_"):
        return "acilis"
    if tur.startswith("P_KAPANIS"):
        return "kapanis"
    if tur.startswith("P_DK_"):
        return "pay_devre_kesici"
    if tur.endswith("_EBDK"):
        return "ebdks"
    if tur.startswith("P_TEKFIYAT"):
        return "tek_fiyat_gun_ici"
    return "diger_" + str(h)


kayit = []
for gun in sorted(os.path.basename(p) for p in glob.glob(os.path.join(emir_dir, "20*"))):
    d = datetime.date.fromisoformat(gun)
    isl = islemler(d)
    isl_g = {k: v for k, v in isl.groupby("islem_kodu", sort=False)}
    for f in sorted(glob.glob(os.path.join(emir_dir, gun, "pay-*.parquet"))):
        t = pq.read_table(f, columns=cols)
        t = t.filter(pc.not_equal(t["emir_kategorisi"], 32))
        df = t.to_pandas()
        for kod, g in df.groupby("islem_kodu", sort=False):
            if not g["seans"].isin(TOPLAMA).any():
                continue
            try:
                r = gs.loc[(d, kod)]
                grup, pazar, baz = r["instrument_group"], r["market_segment"], r["previous_last_price"]
            except KeyError:
                grup, pazar, baz = None, None, np.nan
            tablo = GRUP_TABLO.get(grup)
            if tablo is None:
                continue
            baz_m = int(round(baz * 1000)) if baz and baz > 0 else None
            taban = yukari_adim(baz_m * (1 - MARJ), tablo) if baz_m else None
            tavan = asagi_adim(baz_m * (1 + MARJ), tablo) if baz_m else None
            ti = isl_g.get(kod)
            zt = g["emir_degistirilme_zamani"].to_numpy()
            for tur, M, esl in muzayedeler(g):
                once = g[zt < M]
                son = once.drop_duplicates("emir_no", keep="last")
                akt0 = son[(son["emir_durumu"] == 1) & (son["kalan_miktar"] > 0) & ((son["emir_turu"] & 64) == 0)]
                # gerceklesen
                gf, gq, son_islem = None, 0, None
                if ti is not None:
                    zz = ti["zaman"].to_numpy()
                    e = ti[(zz >= M - np.timedelta64(1, "s")) & (zz <= M + np.timedelta64(300, "s")) & ti["seans"].isin(ESLESTIRME).to_numpy()]
                    if len(e):
                        gq = int(e["islem_adedi"].sum())
                        fs = e["fiyat_m"].unique()
                        gf = int(fs[0]) if len(fs) == 1 else -len(fs)
                    o = ti[zz < M - np.timedelta64(1, "s")]
                    if len(o):
                        son_islem = int(o["fiyat_m"].iloc[-1])
                for kot in ("dahil", "haric"):
                    akt = akt0 if kot == "dahil" else akt0[akt0["emir_kategorisi"] != 4]
                    dng = akt["emir_fiyat_turu"] == 66
                    piy = ((akt["emir_fiyat_turu"] == 2) | ((akt["emir_fiyat_turu"] == 3) & (akt["fiyat"] == 0))) & ~dng
                    lim = ~piy & ~dng & (akt["fiyat"] > 0)
                    A_ = akt["alis_satis"] == "A"
                    fm = np.rint(akt["fiyat"].to_numpy() * 1000).astype(np.int64)
                    q = akt["kalan_miktar"].to_numpy()
                    la, ls = (lim & A_).to_numpy(), (lim & ~A_).to_numpy()
                    ortak = dict(tarih=d, islem_kodu=kod, grup=grup, pazar=pazar, tur=tur, sinif=sinif(tur, M), M=M,
                                 eslestirme_satiri=esl, baz=baz_m, son_islem=son_islem, taban=taban, tavan=tavan,
                                 kotasyon=kot, n_kotasyon=int((akt0["emir_kategorisi"] == 4).sum()),
                                 n_emir=len(akt), n_piyasa=int(piy.sum()), n_dengeleyici=int(dng.sum()),
                                 piy_alis=int(q[(piy & A_).to_numpy()].sum()), piy_satis=int(q[(piy & ~A_).to_numpy()].sum()),
                                 dng_alis=int(q[(dng & A_).to_numpy()].sum()), dng_satis=int(q[(dng & ~A_).to_numpy()].sum()),
                                 gercek_fiyat=gf, gercek_miktar=gq)
                    # kapanis seansi: son islem fiyatinin +-%3'u (ice yuvarlanmis) ile gunluk sinirin kesisimi (madde 72)
                    k_alt, k_ust = taban, tavan
                    if sinif(tur, M) == "kapanis" and son_islem:
                        k_alt = max(x for x in (taban, yukari_adim(son_islem * 0.97, tablo)) if x is not None)
                        k_ust = min(x for x in (tavan, asagi_adim(son_islem * 1.03, tablo)) if x is not None)
                    for refad, ref in (("baz", baz_m), ("son", son_islem if son_islem else baz_m)):
                        for sinirli in (True, False):
                            res = denge(fm[la], q[la], fm[ls], q[ls], ortak["piy_alis"], ortak["piy_satis"], tablo,
                                        k_alt if sinirli else None, k_ust if sinirli else None, ref)
                            x = dict(ortak)
                            x.update(ref_tur=refad, sinirli=sinirli)
                            x.update({k: (str(v) if isinstance(v, list) else v) for k, v in res.items()})
                            # dengeleyici emirler: denge fiyatinda kalan emirlerle, sonra birbirleriyle (madde 52-55)
                            ek = 0
                            if res.get("fiyat") is not None and len(res.get("aday_fazla", [])) and (ortak["dng_alis"] or ortak["dng_satis"]):
                                p0 = res["fiyat"]
                                Dp = ortak["piy_alis"] + int(q[la][fm[la] >= p0].sum())
                                Sp = ortak["piy_satis"] + int(q[ls][fm[ls] <= p0].sum())
                                da, ds = ortak["dng_alis"], ortak["dng_satis"]
                                if Dp > Sp:
                                    k1 = min(Dp - Sp, ds); ds -= k1
                                else:
                                    k1 = min(Sp - Dp, da); da -= k1
                                ek = k1 + min(da, ds)
                            x["miktar_dengeleyicili"] = (res.get("miktar") or 0) + ek
                            kayit.append(x)
        print(gun, os.path.basename(f), len(kayit), flush=True)

R = pd.DataFrame(kayit)
R.to_parquet(os.path.join(out, "tek_fiyat_sonuc.parquet"))
R["fiyat_uyar"] = R["fiyat"].fillna(-1).astype(np.int64) == R["gercek_fiyat"].fillna(-1).astype(np.int64)
R["miktar_uyar"] = R["miktar_dengeleyicili"].fillna(0).astype(np.int64) == R["gercek_miktar"].fillna(0).astype(np.int64)
ana = R[(R.ref_tur == "baz") & R.sinirli & (R.kotasyon == "haric")]
print(ana.groupby(["sinif", "adim"]).agg(n=("fiyat_uyar", "size"), fiyat=("fiyat_uyar", "sum"), miktar=("miktar_uyar", "sum")).to_string())
print(R.groupby(["kotasyon", "ref_tur", "sinirli", "sinif"]).agg(n=("fiyat_uyar", "size"), fiyat=("fiyat_uyar", "sum")).to_string())
