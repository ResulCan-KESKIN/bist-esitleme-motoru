"""Surekli islemde fiyat-zaman onceligi: gunluk emir verisinden defter tekrar kurulur, her pasif
gerceklesmede (islem defterinde aktif_pasif = P) emrin o anki defterde oncelikli emir olup olmadigi denetlenir.

Defter: P_SUREKLI_ISLEM satirlari dahil tum satirlar zaman sirasiyla uygulanir; emir_durumu = 1, kalan > 0,
limit fiyatli (fiyat > 0), orta nokta haric emirler defterdedir. Kontrol ani T icin defter durumu
T'den kesin once uygulanan satirlardir. T aninda ayni aktif emirle gerceklesen pasif emir kumesi B:
  fiyat onceligi: B'deki en kotu fiyattan daha iyi seviyelerdeki tum emirler B'de olmali;
  zaman onceligi: fiyat seviyesinde B'deki emirler, oncelik sirasinin ilk |B| emri olmali.
Oncelik modelleri: M1 emir_giris_zamani; M2 yeni emir veya (fiyat degisikligi ya da miktar artisi);
M3 yeni emir veya herhangi bir degisiklik; M4 yeni emir veya (fiyat degisikligi ya da kalan miktar artisi);
M5 M4 + sistem yenilemesi (sebep 13, kismi gorunme kosullu emrin gorunen kisminin yenilenmesi).
Kullanim: python -I gunici_oncelik_kontrol.py GUNLUK_EMIR_KLASORU ISLEM.parquet CIKTI GUN [GUN ...] [--kod KOD,...]
"""
import sys, os, glob, datetime, collections
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

arg = sys.argv[1:]
kodlar = None
if "--kod" in arg:
    i = arg.index("--kod")
    kodlar = set(arg[i + 1].split(","))
    arg = arg[:i] + arg[i + 2:]
emir_dir, islem_src, out = arg[:3]
gunler = arg[3:]
os.makedirs(out, exist_ok=True)
ipf = pq.ParquetFile(islem_src)
iidx = ipf.schema_arrow.get_field_index("tarih")
cols = ["islem_kodu", "emir_no", "emir_giris_zamani", "emir_degistirilme_zamani", "alis_satis", "emir_turu",
        "emir_kategorisi", "emir_durumu", "degisiklik_sebebi", "emir_miktari", "kalan_miktar", "fiyat", "seans",
        "islem_numarasi", "guncelleme_no"]
MODELLER = ["M1", "M2", "M3", "M4", "M5"]


def pasifler(d):
    rgs = [i for i in range(ipf.num_row_groups)
           if ipf.metadata.row_group(i).column(iidx).statistics.min <= d <= ipf.metadata.row_group(i).column(iidx).statistics.max]
    t = ipf.read_row_groups(rgs, columns=["tarih", "islem_kodu", "ortak_sozlesme_no", "emir_no", "aktif_pasif", "seans"])
    t = t.filter(pc.and_(pc.equal(t["tarih"], pa.scalar(d)), pc.equal(t["seans"], "P_SUREKLI_ISLEM")))
    df = t.to_pandas()
    df["no"] = [int(x, 16) for x in df["ortak_sozlesme_no"]]
    p = df[df["aktif_pasif"] == "P"].set_index(["no", "emir_no"]).index
    return set(p)


sonuc = collections.Counter()
ornek = []
for gun in gunler:
    d = datetime.date.fromisoformat(gun)
    pas = pasifler(d)
    for f in sorted(glob.glob(os.path.join(emir_dir, gun, "pay-*.parquet"))):
        t = pq.read_table(f, columns=cols)
        if kodlar:
            t = t.filter(pc.is_in(t["islem_kodu"], pa.array(sorted(kodlar))))
        else:
            t = t.filter(pc.match_substring(pc.cast(t["islem_kodu"], pa.string()), ".E"))
        if t.num_rows == 0:
            continue
        t = t.set_column(t.schema.get_field_index("islem_numarasi"), "islem_numarasi", t["islem_numarasi"].fill_null(0))
        df = t.to_pandas()
        df["islem_kodu"] = df["islem_kodu"].astype(str)
        for kod, g in df.groupby("islem_kodu", sort=False):
            g = g.sort_values(["emir_degistirilme_zamani", "guncelleme_no"], kind="stable")
            zt = g["emir_degistirilme_zamani"].to_numpy().astype("int64")
            no, side, prc = g["emir_no"].to_numpy(), (g["alis_satis"] == "A").to_numpy(), g["fiyat"].to_numpy()
            kal, mik, dur = g["kalan_miktar"].to_numpy(), g["emir_miktari"].to_numpy(), g["emir_durumu"].to_numpy()
            seb, gir = g["degisiklik_sebebi"].to_numpy(), g["emir_giris_zamani"].to_numpy().astype("int64")
            tur, isn = g["emir_turu"].to_numpy(), g["islem_numarasi"].to_numpy()
            seans = g["seans"].astype(str).to_numpy()
            yenilenen = set()   # sebep 13 satiri gormus emirler
            kitap = {}          # emir_no -> [taraf, fiyat, kalan, M1, M2, M3, M4, M5, miktar]
            seviye = {True: collections.defaultdict(set), False: collections.defaultdict(set)}

            def cikar(e):
                v = kitap.pop(e, None)
                if v is not None:
                    s_ = seviye[v[0]][v[1]]
                    s_.discard(e)
                    if not s_:
                        del seviye[v[0]][v[1]]

            n = len(g)
            i = 0
            while i < n:
                j = i
                while j < n and zt[j] == zt[i]:
                    j += 1
                # T = zt[i] aninda pasif gerceklesmeler (defter durumu: once uygulanan satirlar)
                B = collections.defaultdict(list)
                for k in range(i, j):
                    if isn[k] and seans[k] == "P_SUREKLI_ISLEM" and (int(isn[k]), no[k]) in pas and no[k] in kitap:
                        B[bool(side[k])].append(no[k])
                for taraf, uyeler in B.items():
                    uy = set(uyeler)
                    en_kotu = min(kitap[e][1] for e in uy) if taraf else max(kitap[e][1] for e in uy)
                    daha_iyi = [p for p in seviye[taraf] if (p > en_kotu if taraf else p < en_kotu)]
                    fiyat_ok = all(e in uy for p in daha_iyi for e in seviye[taraf][p])
                    sonuc[("fiyat", fiyat_ok)] += 1
                    lv = [(e, kitap[e]) for e in seviye[taraf][en_kotu]]
                    k_uy = [e for e, _ in lv if e in uy]
                    for mi, mod in enumerate(MODELLER):
                        sira = [e for e, _ in sorted(lv, key=lambda ev: (ev[1][3 + mi], ev[0]))]
                        ok = set(sira[:len(k_uy)]) == set(k_uy)
                        sonuc[("zaman_" + mod, ok)] += 1
                        if not ok and mod == "M5":
                            ilgili = set(sira[:len(k_uy)]) | set(k_uy)
                            sonuc[("M5_ihlal_yenilenen_emir_var", bool(ilgili & yenilenen))] += 1
                        if not ok and mod == "M5" and len(ornek) < 50:
                            ornek.append((gun, kod, pd.Timestamp(zt[i], unit='us'), taraf, en_kotu, k_uy[:5], sira[:5]))
                # satirlari uygula
                for k in range(i, j):
                    e = no[k]
                    if seb[k] == 13:
                        yenilenen.add(e)
                    aktif = dur[k] == 1 and kal[k] > 0 and prc[k] > 0 and (tur[k] & 64) == 0                         and seans[k] != "P_GUNSONU"
                    eski = kitap.get(e)
                    cikar(e)
                    if not aktif:
                        continue
                    if eski is None:
                        v = [bool(side[k]), prc[k], kal[k], gir[k], zt[k], zt[k], zt[k], zt[k], mik[k]]
                    else:
                        m2, m4, m5 = eski[4], eski[6], eski[7]
                        if seb[k] == 5 and (prc[k] != eski[1] or mik[k] > eski[8]):
                            m2 = zt[k]
                        if seb[k] == 5 and (prc[k] != eski[1] or kal[k] > eski[2]):
                            m4 = zt[k]
                            m5 = zt[k]
                        if seb[k] == 13:
                            m5 = zt[k]
                        m3 = zt[k] if seb[k] in (5, 6) else eski[5]
                        v = [bool(side[k]), prc[k], kal[k], gir[k], m2, m3, m4, m5, mik[k]]
                    kitap[e] = v
                    seviye[v[0]][v[1]].add(e)
                i = j
        print(gun, os.path.basename(f), dict(sonuc), flush=True)

pd.Series(sonuc).rename("adet").to_csv(os.path.join(out, "oncelik_sonuc.csv"), encoding="utf-8")
pd.DataFrame(ornek, columns=["gun", "kod", "zaman", "alis", "fiyat", "gerceklesen", "beklenen_ilk"]).to_csv(
    os.path.join(out, "oncelik_ihlal_ornek.csv"), index=False, encoding="utf-8")
print(dict(sonuc))
