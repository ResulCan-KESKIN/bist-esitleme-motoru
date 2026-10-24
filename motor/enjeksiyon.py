"""Enjeksiyon modu (TASARIM.md 4.1, 5): bir sira-gun once enjeksiyonsuz (taban cizgisi), sonra sentetik senaryoyla
oynatilir; sentetik aktorun islemleri ve fiyat etkisi raporlanir. Gercek akis dissal kabul edilir (gercek
katilimcilar enjeksiyona tepki vermez); bu yontemin bilinen sinirlidir.

Kullanim: python -I motor/enjeksiyon.py GUNLUK_EMIR_KLASORU GUNSONU.parquet GUN KOD SENARYO SAAT [ad=deger ...]
  SENARYO: kapanis | yaniltici | yukseltme | karsilikli   (motor/senaryolar.py; parametreler ad=deger)
  SAAT: HH:MM:SS (kapanis senaryosunda kullanilmaz)
"""
import collections, json, os, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor import veri, senaryolar
from motor.gun import Gun, kosular


def ozet_fiyatlar(g):
    isl = [i for b, i in g.islemler if b != "P_KAPANIS_FIY_ISLEM"]
    kap = next((s.get("fiyat") for _, b, s in reversed(g.muzayedeler) if s.get("fiyat") is not None), None)
    return dict(kapanis_muzayede_fiyati=kap, son_fiyat=isl[-1].fiyat if isl else None,
                en_yuksek=max((i.fiyat for i in isl), default=None), en_dusuk=min((i.fiyat for i in isl), default=None),
                islem=len(g.islemler), adet=sum(i.adet for _, i in g.islemler))


def calistir(gunluk, gunsonu, gun, kod, senaryo, saat, **param):
    df = veri.pay_gun_emirleri(gunluk, gun, kod)
    tepe = veri.tepe_tahmini(df)
    taban = Gun(df, gun, kod, gunsonu, tepe)
    taban.calistir()
    sirali = sorted((i for _, i in taban.islemler), key=lambda i: i.zaman)
    tb = taban.tablo
    if senaryo == "kapanis":
        kos = kosular(df)
        k = next(j for j, (s, _, _) in enumerate(kos) if s.startswith("P_KAPANIS_EMIR"))
        esl = next((b for s, b, _ in kos[k:] if s in veri.ESLESTIRME), None)
        ref = senaryolar.son_fiyat(sirali, kos[k][1])
        olaylar = senaryolar.kapanis_etkileme(kos[k][1], tb, ref, kapanis_eslestirme=esl, **param)
    else:
        t = int(pd.Timestamp(f"{gun} {saat}").value // 1000)
        ref = senaryolar.son_fiyat(sirali, t)
        uret = {"yaniltici": senaryolar.yaniltici_emir, "yukseltme": senaryolar.fiyat_yukseltme,
                "karsilikli": senaryolar.karsilikli_islem}[senaryo]
        ek = dict(en_iyi=senaryolar.en_iyi_fiyatlar(taban.defter_ornekleri, t)) if senaryo == "yaniltici" else {}
        olaylar = uret(t, tb, ref, **param, **ek)
    enj = Gun(df, gun, kod, gunsonu, tepe)
    enj.calistir(olaylar)
    s_isl = [(b, i) for b, i in enj.islemler if enj.sentetik_mi(i)]
    # gercek emirler arasindaki islemlerin degisimi
    anahtar = lambda i: (i.alis_no, i.satis_no, i.fiyat, i.adet)
    c0 = collections.Counter(anahtar(i) for _, i in taban.islemler)
    c1 = collections.Counter(anahtar(i) for _, i in enj.islemler if not enj.sentetik_mi(i))
    ortak = sum((c0 & c1).values())
    alis = sum(i.adet for _, i in s_isl if i.alis_no in enj.sentetik_nolar)
    satis = sum(i.adet for _, i in s_isl if i.satis_no in enj.sentetik_nolar)
    ozet = collections.OrderedDict([
        ("kod", kod), ("gun", gun), ("senaryo", senaryo), ("referans_fiyat", ref), ("parametre", param),
        ("sentetik_olay", len(olaylar)), ("reddedilen", collections.Counter(r for _, _, r in enj.reddedilen)),
        ("sentetik_islem", len(s_isl)), ("sentetik_alis_adet", alis), ("sentetik_satis_adet", satis),
        ("sentetik_islem_bolumleri", dict(collections.Counter(b for b, _ in s_isl))),
        ("taban", ozet_fiyatlar(taban)), ("enjeksiyonlu", ozet_fiyatlar(enj)),
        ("gercek_islem_degismeyen", f"{ortak}/{sum(c0.values())}"),
    ])
    return ozet, olaylar, s_isl


if __name__ == "__main__":
    gunluk, gunsonu, gun, kod, senaryo, saat = sys.argv[1:7]
    param = {}
    for a in sys.argv[7:]:
        k, v = a.split("=", 1)
        param[k] = {"True": True, "False": False}.get(v, float(v) if "." in v else int(v) if v.lstrip("-").isdigit() else v)
    ozet, olaylar, s_isl = calistir(gunluk, gunsonu, gun, kod, senaryo, saat, **param)
    print(json.dumps(ozet, ensure_ascii=False, indent=1, default=str))
