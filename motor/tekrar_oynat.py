"""Tekrar oynatma: bir sira-gunu gercek emir eylemleriyle motorda yeniden uretir ve uretilen islemleri
PP_GUNICIISLEM ile karsilastirir (TASARIM.md 4.1, dogrulama modu).

- Gun sonu dosyasi verilirse gun bastan sona oynatilir (motor/gun.py): acilis, surekli islem, devre kesici ve EBDKS
  muzayedeleri, kapanis, kapanis fiyatindan islemler. Bolum gecisleri ve eslestirme anlari veriden alinir.
- Verilmezse yalniz surekli islem oynatilir; baslangic defteri surekli isleme gecis anindaki veriden kurulur ve
  karsilastirma ilk devre kesici / EBDKS kesintisine kadar yapilir.
- Karsilastirma anahtari: (alis emri, satis emri, fiyat, adet), bolum bolum ve butun gun. Orta nokta emirli
  islemler ve ozel islem bildirimleri kapsam disidir.
Kullanim: python -I motor/tekrar_oynat.py GUNLUK_EMIR_KLASORU ISLEM.parquet GUN KOD [--gunsonu GUNSONU.parquet]
          [--cikti KLASOR]
"""
import collections, os, sys, time

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor import veri
from motor.defter import Defter
from motor.gun import Gun
from motor.surekli_islem import SurekliIslem

ANAHTAR = ["alis_no", "satis_no", "fiyat", "adet"]
# veride islem bolumu adi -> ozet oneki
BOLUM_ONEK = {"P_SUREKLI_ISLEM": "", "P_KAPANIS_FIY_ISLEM": "kfi_", "P_ESLESTIRME": "muzayede_",
              "P_ESLESTIRMETEKFIYAT": "muzayede_", "P_ESLESTIRME_EBDK": "ebdks_muzayede_"}


def tablo(islemler, bolumler=None):
    df = pd.DataFrame([(i.sira, i.zaman, i.alis_no, i.satis_no, i.aktif_no, i.fiyat, i.adet) for i in islemler],
                      columns=["sira", "zaman", "alis_no", "satis_no", "aktif_no", "fiyat", "adet"])
    if bolumler is not None:
        df["seans"] = bolumler
    return df


def karsilastir(motor, g, onek):
    cm = collections.Counter(map(tuple, motor[ANAHTAR].to_numpy().tolist()))
    cg = collections.Counter(map(tuple, g[ANAHTAR].to_numpy().tolist()))
    ortak = sum((cm & cg).values())
    km, kg = motor[ANAHTAR].to_numpy().tolist(), g[ANAHTAR].to_numpy().tolist()
    ilk = next((i for i in range(min(len(km), len(kg))) if km[i] != kg[i]), None)
    if ilk is None and len(km) != len(kg):
        ilk = min(len(km), len(kg))

    def toplam(x):
        return pd.concat([x.groupby("alis_no")["adet"].sum(), x.groupby("satis_no")["adet"].sum()]).groupby(level=0).sum()
    b = pd.concat([toplam(motor).rename("motor"), toplam(g).rename("gercek")], axis=1).fillna(0)
    ozet = collections.OrderedDict([
        (onek + "islem_gercek", len(g)), (onek + "islem_motor", len(motor)), (onek + "islem_ortak", ortak),
        (onek + "islem_ortak_oran", round(ortak / len(g), 6) if len(g) else None),
        (onek + "adet_gercek", int(g["adet"].sum())), (onek + "adet_motor", int(motor["adet"].sum())),
        (onek + "emir_gerceklesen_ayni", f"{int((b['motor'] == b['gercek']).sum())}/{len(b)}"),
        (onek + "ilk_sapma_sirasi", ilk),
    ])
    if len(g) and (g["aktif_no"] != "").any() and (motor["aktif_no"] != "").any():
        gm = g[g["aktif_no"] != ""].merge(motor, on=ANAHTAR, suffixes=("_g", "_m"))
        ozet[onek + "aktif_taraf_ayni"] = f"{int((gm['aktif_no_g'] == gm['aktif_no_m']).sum())}/{len(gm)}"
    sapma = None
    if ilk is not None:
        sapma = pd.concat([motor.iloc[max(0, ilk - 3):ilk + 5].assign(kaynak="motor"),
                           g.iloc[max(0, ilk - 3):ilk + 5].assign(kaynak="gercek")])
    return ozet, sapma


def zaman_us(g, gun):
    g["zaman_us"] = (pd.Timestamp(gun) + pd.to_timedelta(g["zaman"])).to_numpy().astype("datetime64[us]").astype("int64")
    return g


def calistir(gunluk, islem_parquet, gun, kod, gunsonu=None):
    t0 = time.time()
    df = veri.pay_gun_emirleri(gunluk, gun, kod)
    tepe = veri.tepe_tahmini(df)
    orta = set(df.loc[(df["emir_turu"] & veri.ORTA_NOKTA) != 0, "emir_no"])
    ozet = collections.OrderedDict([("kod", kod), ("gun", gun), ("kismi_gorunme_emir", len(tepe))])
    sapmalar = {}
    if gunsonu:
        ozet["mod"] = "butun_gun"
        g_ = Gun(df, gun, kod, gunsonu, tepe)
        isl = g_.calistir()
        motor = tablo([i for _, i in isl], [b for b, _ in isl])
        ozet["muzayede_sayisi"] = len(g_.muzayedeler)
        ozet["muzayede_fiyatlari"] = ";".join(f"{b}:{s.get('fiyat')}" for _, b, s in g_.muzayedeler)
        g = veri.gercek_islemler(islem_parquet, gun, kod, tuple(BOLUM_ONEK))
        g = g[~(g["alis_no"].isin(orta) | g["satis_no"].isin(orta))]
        o, sapmalar["gun"] = karsilastir(motor, g, "gun_")
        ozet.update(o)
        for onek in dict.fromkeys(BOLUM_ONEK.values()):
            sn = [k for k, v in BOLUM_ONEK.items() if v == onek]
            o, s = karsilastir(motor[motor["seans"].isin(sn + (["eslestirme_satirsiz"] if onek == "muzayede_" else []))],
                               g[g["seans"].isin(sn)], onek)
            if o[onek + "islem_gercek"] or o[onek + "islem_motor"]:
                ozet.update(o)
                sapmalar[onek.rstrip("_") or "surekli"] = s
        ozet["sayac"] = dict(g_.sayac)
    else:
        ozet["mod"] = "yalniz_surekli"
        bas, bit = veri.surekli_araligi(df)
        ozet["kesinti"] = str(pd.Timestamp(bit, unit="us")) if bit is not None else "yok"
        d = Defter()
        for e in veri.baslangic_defteri(df, bas, tepe):
            d.ekle(e)
        olaylar, _ = veri.eylemler(df, bas, bit, tepe)
        m = SurekliIslem(d)
        for o in olaylar:
            m.isle(o)
        motor = tablo(m.islemler)
        g = zaman_us(veri.gercek_islemler(islem_parquet, gun, kod), gun)
        if bit is not None:
            g = g[g["zaman_us"] < bit]
        g = g[~(g["alis_no"].isin(orta) | g["satis_no"].isin(orta))]
        o, sapmalar["surekli"] = karsilastir(motor, g, "")
        ozet.update(o)
        ozet["sayac"] = dict(m.sayac)
    ozet["sure_sn"] = round(time.time() - t0, 1)
    return ozet, motor, sapmalar


if __name__ == "__main__":
    arg = sys.argv[1:]
    sec = {}
    for ad in ("--gunsonu", "--cikti"):
        if ad in arg:
            i = arg.index(ad)
            sec[ad] = arg[i + 1]
            arg = arg[:i] + arg[i + 2:]
    gunluk, islem_parquet, gun, kod = arg[:4]
    ozet, motor, sapmalar = calistir(gunluk, islem_parquet, gun, kod, sec.get("--gunsonu"))
    for k, v in ozet.items():
        print(f"{k}: {v}")
    out = sec.get("--cikti")
    if out:
        os.makedirs(out, exist_ok=True)
        motor.to_csv(os.path.join(out, f"{kod}_{gun}_motor_islemler.csv"), index=False, encoding="utf-8")
        with open(os.path.join(out, f"{kod}_{gun}_ozet.txt"), "w", encoding="utf-8") as f:
            for k, v in ozet.items():
                f.write(f"{k}: {v}\n")
        for ad, s in sapmalar.items():
            if s is not None:
                s.to_csv(os.path.join(out, f"{kod}_{gun}_ilk_sapma_{ad}.csv"), index=False, encoding="utf-8")
