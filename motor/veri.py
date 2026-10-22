"""DataStore gun ici verisinden motor girdisi ve karsilastirma verisi (TASARIM.md 4.1-4.2).

Emir: gun-ici-emir/gunluk/YYYY-MM-DD/pay-*.parquet (gunici_emir_gunluk_bol.py ciktisi). Islem: aylik PP_GUNICIISLEM.
Kullanici eylemleri yeni emir (sebep 6), degisiklik (5) ve iptaldir (1); diger satirlar motorun uretmesi beklenen
ciktilardir. Ilk surumde kapsam disi: kotasyon (kategori 4), ozel islem bildirimi (32), orta nokta (emir_turu 64).
Fiyatlar milli-TL'ye cevrilir.
"""
import datetime, functools, glob, os
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from .emir import Emir, YeniEmir, Degistir, Iptal

SUREKLI = "P_SUREKLI_ISLEM"
ACILIS_TOPLAMA = ("P_ACILIS_EMIR_TPL", "P_ACS_EMR_TP_EIY", "P_ACS_EMR_TP2_PY", "P_ACS_EMR_TP2_PY_EIY")
ESLESTIRME = ("P_ESLESTIRME", "P_ESLESTIRMETEKFIYAT", "P_ESLESTIRME_EBDK")
KAPANIS_TOPLAMA = ("P_KAPANIS_EMIR_TPL", "P_KAPANIS_EMIR_TPL2")
KAPANIS_FIYATI = "P_KAPANIS_FIY_ISLEM"
OZEL_ISLEM = (3, 5)   # normal_islem: ozel islem bildirimi
NORMAL, ORTA_NOKTA = 1, 64
# surekli islemi kesen bolumler: pay bazinda devre kesici ve EBDKS (06-devre-kesici.md)
KESINTI = ("P_DK_", "P_GECICI_DUR", "P_TF_EMIR_TPL", "P_ESLESTIRME_EBDK")
EMIR_SUTUN = ["emir_no", "emir_degistirilme_zamani", "alis_satis", "emir_fiyat_turu", "emir_turu", "emir_kategorisi",
              "gecerlilik_turu", "emir_durumu", "degisiklik_sebebi", "emir_miktari", "kalan_miktar", "fiyat", "seans",
              "islem_numarasi", "eslesen_miktar", "guncelleme_no", "afk"]


def milli(x):
    return np.rint(np.asarray(x, dtype=float) * 1000).astype(np.int64)


@functools.lru_cache(maxsize=4)
def _kod_dosyasi(gunluk_klasor, gun):
    """Gunun pay dosyalarinda hangi sira hangi dosyada (yalniz islem_kodu sutunu okunur)."""
    out = {}
    for f in sorted(glob.glob(os.path.join(gunluk_klasor, gun, "pay-*.parquet"))):
        for k in pc.unique(pq.read_table(f, columns=["islem_kodu"])["islem_kodu"]).to_pylist():
            out[str(k)] = f
    return out


def pay_gun_emirleri(gunluk_klasor, gun, kod):
    """Bir sira-gunun tum emir satirlari; dosya sirasi (zaman, guncelleme_no) korunur."""
    f = _kod_dosyasi(gunluk_klasor, gun).get(kod)
    if f is None:
        raise ValueError(f"{kod} {gun} icin emir satiri yok")
    t = pq.read_table(f, columns=EMIR_SUTUN, filters=[("islem_kodu", "=", kod)])
    t = t.set_column(t.schema.get_field_index("islem_numarasi"), "islem_numarasi", t["islem_numarasi"].fill_null(0))
    t = t.set_column(t.schema.get_field_index("eslesen_miktar"), "eslesen_miktar", t["eslesen_miktar"].fill_null(0))
    df = t.to_pandas()
    for c in ("alis_satis", "gecerlilik_turu", "seans", "afk"):
        df[c] = df[c].astype(str)
    df["zaman"] = df["emir_degistirilme_zamani"].astype("int64")
    df["fiyat_m"] = milli(df["fiyat"])
    df["alis"] = df["alis_satis"] == "A"
    df["kapsam"] = (df["emir_kategorisi"] == NORMAL) & ((df["emir_turu"] & ORTA_NOKTA) == 0)
    df = df.reset_index(drop=True)
    # ayni emrin bir onceki satiri (degisiklikte kalan farki icin)
    s = df.sort_values(["emir_no", "guncelleme_no"], kind="stable")
    df["onceki_kalan"] = s.groupby("emir_no")["kalan_miktar"].shift().reindex(df.index)
    df["onceki_fiyat"] = s.groupby("emir_no")["fiyat_m"].shift().reindex(df.index)
    return df


def surekli_araligi(df):
    """Surekli islemin ilk olay zamani ve (varsa) ilk kesinti zamani."""
    z = df.loc[df["seans"] == SUREKLI, "zaman"]
    if not len(z):
        raise ValueError("surekli islem bolumu yok (tek fiyatla islem goren sira olabilir)")
    bas = int(z.min())
    k = df[df["seans"].str.startswith(KESINTI) & (df["zaman"] > bas)]
    return bas, (int(k["zaman"].min()) if len(k) else None)


def _tepe_tutarli(p, satirlar):
    """p tepe buyuklugu, emrin pasif gerceklesmelerindeki sebep 13 isaretlerini uretebiliyor mu.
    Veride sebep 13 gorunen kismi bitiren islemde yazilir. Yenilemeden (ve muzayededen surekli isleme geciste)
    sonraki ilk islem 3 ya da 13 olabilir. Ayni islemde yenilenen kisimdan da eslesilebilir (tek islem yazilir)."""
    v, serbest, muzayede = None, False, False   # serbest: siradaki islemde 13 isareti gorunen kisim bitmeden de olabilir
    for seb, z, kal, q, once, surekli, giris in satirlar:
        if not surekli or z == giris:
            v = None   # muzayede ya da giristeki agresif eslesme: gorunen kisim kurali yok
            muzayede = not surekli
            continue
        if v is None:
            v, serbest = min(p, once), muzayede
        if seb == 5:
            v = min(p, kal) if kal > once else min(v, kal)
            continue
        if seb not in (3, 13):
            continue
        if q < v:
            if seb == 13 and not serbest:
                return False
            v -= q
            serbest = False
            continue
        if kal == 0:
            return True
        if seb != 13:
            return False
        gizli, kalan_q = once - v, q - v
        v = min(p, gizli)
        while kalan_q >= v and kalan_q > 0:
            kalan_q -= v
            gizli -= v
            v = min(p, gizli)
        v -= kalan_q
        serbest = kalan_q == 0
    return True


def tepe_tahmini(df):
    """Kismi gorunme kosullu emirlerin gorunen kisim buyuklugu (veride yazili degildir, TASARIM.md 4.2).
    Once ilk yenilemeye kadar pasif olarak gerceklesen miktar denenir; sebep 13 dizisini tutarli uretmiyorsa emrin
    islem miktarlari ve yenileme araliklarindan uretilen adaylarin tutarli olan en buyugu secilir."""
    tepe = {}
    adaylar = set(df.loc[df["degisiklik_sebebi"] == 13, "emir_no"])
    s = df[df["emir_no"].isin(adaylar)].sort_values(["emir_no", "guncelleme_no"], kind="stable")
    for no, g in s.groupby("emir_no", sort=False):
        giris = int(g["zaman"].iloc[0]) if g["degisiklik_sebebi"].iloc[0] == 6 else None
        satirlar, once = [], None
        for seb, z, kal, q, sn in zip(g["degisiklik_sebebi"], g["zaman"], g["kalan_miktar"], g["eslesen_miktar"],
                                      g["seans"]):
            satirlar.append((seb, z, kal, q, kal if once is None else once, sn == SUREKLI, giris))
            once = kal
        pasif = [r for r in satirlar if r[5] and r[1] != giris]
        if not pasif:
            continue
        bas = pasif[0][4]
        aday = {int(r[3]) for r in pasif if r[0] in (3, 13) and r[3] > 0}
        yen = [r for r in pasif if r[0] == 13]
        for j, r in enumerate(yen, 1):
            for k in range(j, j + 2):
                aday.add(int((bas - r[2]) // k))
        ilk = int(bas - yen[0][2]) if yen and bas - yen[0][2] > 0 else None
        if ilk is not None and _tepe_tutarli(ilk, satirlar):
            tepe[no] = ilk
            continue
        uygun = [p for p in aday if p > 0 and _tepe_tutarli(p, satirlar)]
        if uygun:
            tepe[no] = max(uygun)
        elif ilk is not None:
            tepe[no] = ilk
    return tepe


def baslangic_defteri(df, bas, tepe):
    """Surekli isleme gecerken defterdeki emirler, oncelik sirasinda (once uygulanan satirlar, model M5)."""
    s = df[(df["zaman"] < bas) & df["kapsam"]]
    son = {}
    for r in s.itertuples(index=False):
        aktif = r.emir_durumu == 1 and r.kalan_miktar > 0 and r.fiyat_m > 0 and r.seans != "P_GUNSONU"
        eski = son.get(r.emir_no)
        if not aktif:
            son.pop(r.emir_no, None)
            continue
        if eski is None or r.fiyat_m != eski[1] or r.kalan_miktar > eski[2] or r.degisiklik_sebebi == 13:
            t = r.zaman
        else:
            t = eski[3]
        son[r.emir_no] = (r.alis, r.fiyat_m, r.kalan_miktar, t, r.gecerlilik_turu)
    emirler = []
    for no, (alis, p, kal, t, gec) in sorted(son.items(), key=lambda kv: kv[1][3]):
        tp = tepe.get(no)
        emirler.append(Emir(no, bool(alis), int(p), int(kal), gecerlilik=gec, tepe=tp,
                            gorunen=min(tp, int(kal)) if tp else int(kal), zaman=int(t)))
    return emirler


def eylemler(df, bas, bit, tepe, seanslar=(SUREKLI,)):
    """Verilen bolumlerdeki kullanici eylemleri, [bas, bit) araliginda, zaman sirasinda (ayni us'de dosya sirasi)."""
    s = df[df["seans"].isin(seanslar) & df["kapsam"] & df["degisiklik_sebebi"].isin([6, 5, 1]) & (df["zaman"] >= bas)]
    if bit is not None:
        s = s[s["zaman"] < bit]
    s = s.sort_values("zaman", kind="stable")
    out = []
    for r in s.itertuples(index=False):
        if r.degisiklik_sebebi == 6:
            out.append(YeniEmir(r.zaman, r.emir_no, bool(r.alis), int(r.fiyat_m), int(r.emir_miktari),
                                int(r.emir_fiyat_turu), r.gecerlilik_turu, tepe.get(r.emir_no), bool(r.emir_turu & 2)))
        elif r.degisiklik_sebebi == 5:
            fark = 0 if pd.isna(r.onceki_kalan) else int(r.kalan_miktar - r.onceki_kalan)
            # AFK (acente/fon kodu) dolu emirde fiyati ve kalani degismeyen degisiklik onceligi kaybettirir (veri)
            gorunmeyen = r.afk == "E" and fark == 0 and r.fiyat_m == r.onceki_fiyat
            out.append(Degistir(r.zaman, r.emir_no, int(r.fiyat_m), fark, gorunmeyen))
        else:
            out.append(Iptal(r.zaman, r.emir_no))
    ayni = int(s["zaman"].duplicated(keep=False).sum())
    return out, ayni


def sira_bilgisi(gunsonu_parquet, gun, kod):
    """Gun sonu dosyasindan arac grubu, pazar ve baz fiyat (onceki kapanis, milli-TL)."""
    t = pq.read_table(gunsonu_parquet, columns=["trade_date", "instrument_series_code", "instrument_group",
                                               "market_segment", "previous_last_price"],
                      filters=[("trade_date", "=", datetime.date.fromisoformat(gun)), ("instrument_series_code", "=", kod)])
    if t.num_rows == 0:
        raise ValueError(f"{kod} {gun} gun sonu satiri yok")
    r = t.to_pylist()[0]
    baz = r["previous_last_price"]
    return r["instrument_group"], r["market_segment"], (int(round(baz * 1000)) if baz and baz > 0 else None)


@functools.lru_cache(maxsize=2)
def _gun_islemleri(islem_parquet, gun):
    d = datetime.date.fromisoformat(gun)
    f = pq.ParquetFile(islem_parquet)
    ti = f.schema_arrow.get_field_index("tarih")
    rgs = [i for i in range(f.num_row_groups)
           if f.metadata.row_group(i).column(ti).statistics.min <= d <= f.metadata.row_group(i).column(ti).statistics.max]
    t = f.read_row_groups(rgs, columns=["tarih", "islem_kodu", "ortak_sozlesme_no", "alis_satis", "islem_adedi",
                                         "islem_fiyati", "emir_no", "islem_zamani", "normal_islem", "seans",
                                         "aktif_pasif"])
    return t.filter(pc.equal(t["tarih"], pa.scalar(d)))


def gercek_islemler(islem_parquet, gun, kod, seanslar=(SUREKLI,)):
    """Verilen bolumlerdeki islemler (ozel islem bildirimi haric): islem basina bir satir
    (sira = ortak_sozlesme_no, onaltilik)."""
    t = _gun_islemleri(islem_parquet, gun)
    t = t.filter(pc.and_(pc.equal(t["islem_kodu"], kod),
                         pc.and_(pc.is_in(t["seans"], pa.array(list(seanslar))),
                                 pc.invert(pc.is_in(t["normal_islem"], pa.array(list(OZEL_ISLEM), pa.int16()))))))
    df = t.to_pandas()
    a = df[df["alis_satis"] == "A"].set_index("ortak_sozlesme_no")
    s = df[df["alis_satis"] == "S"].set_index("ortak_sozlesme_no")
    g = a[["islem_adedi", "islem_fiyati", "emir_no", "islem_zamani", "aktif_pasif", "seans"]].join(
        s[["emir_no", "aktif_pasif"]], rsuffix="_s", how="inner")
    out = pd.DataFrame({
        "sira": [int(x, 16) for x in g.index],
        "zaman": g["islem_zamani"].to_numpy(),
        "alis_no": g["emir_no"].to_numpy(),
        "satis_no": g["emir_no_s"].to_numpy(),
        "fiyat": milli(g["islem_fiyati"]),
        "adet": g["islem_adedi"].to_numpy().astype(np.int64),
        "aktif_no": np.where(g["aktif_pasif"] == "A", g["emir_no"], np.where(g["aktif_pasif_s"] == "A", g["emir_no_s"], "")),
        "seans": g["seans"].to_numpy(),
    })
    return out.sort_values("sira").reset_index(drop=True)
