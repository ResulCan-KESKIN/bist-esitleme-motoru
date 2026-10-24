"""Sentetik enjeksiyonla etiketli degerlendirme (TASARIM.md 6.3): rastgele pay-gunlere senaryo enjekte edilir, motor
ciktisindan ozellikler hesaplanir ve gunun tablosunda o pay-gunun satiri degistirilir; yontemlerin enjekte edilen
pay-gunleri yakalama orani olculur.

- Pay-gun secimi: 10.03.2025 ve sonrasi (Z-skor icin en az 5 gun gecmis), surekli islemde en az ISLEM_EN_AZ islem,
  ozsermaye gunu ve SPK etiketli pay-gun haric. Senaryolar sirayla; saat 10:30-17:00 arasinda rastgele (kapanis haric).
- Olcek: payin o gunku toplam islem miktari (lot) H. Kapanis: emir H x KAPANIS_ORAN; yaniltici: 3 katman (son islem
  tarafin en iyi fiyatindan YANILTICI_ADIM adim geriden baslayarak; en iyi fiyat taban oynatmasinin defter orneginden),
  katman H x 0,02, karsi emir H x 0,002 (agresif: piyasadan limite KIE); yukseltme: 10 emir, her biri H x 0,005;
  karsilikli: 10 tekrar, her biri H x 0,005.
- Temiz yaniltici emir: katmanlardan islem goren miktar (senaryolar.katman_dolan) katman toplaminin KATMAN_DOLUM_EN_COK
  oranini asarsa vaka temiz sayilmaz ve degerlendirmeye alinmaz (katmanlar dolarsa senaryo buyuk agresif isleme doner).
- Kontrol: ayni pay-gunlerin enjeksiyonsuz motor ozellikleri de ayni yolla yerlestirilip puanlanir (yontem farkinin
  sahte tespit uretip uretmedigi). Ozellik farki ayrica ozet olarak yazilir.
- Olcutler: enjekte edilen pay-gunun gun icindeki yuzdelik sirasi; gun icinde ilk %1 ve %5'e girme orani;
  esik = butun tablonun ilk %1'i icin kesinlik, duyarlilik, F1.
Kullanim: python -I tespit/sentetik_degerlendir.py OZELLIKLER.parquet VAKA.csv CIKTI_KLASORU [ADET] [TOHUM]
"""
import os, sys, time

import numpy as np
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import veri, senaryolar
from motor.gun import Gun, kosular
import yontemler as y
import motor_ozellikleri as mo
from ozellikler import gunsonu_ozellikleri

GUNLUK = os.path.join(KOK, "veri", "gun-ici-emir", "gunluk")
ISLEM_EN_AZ = 300
KAPANIS_ORAN = 0.03
YANILTICI_ADIM = 4   # katmanlar ayni tarafin en iyi fiyatindan 4, 5, 6 adim geride (defterin derininde)
YANILTICI_KATMAN = 3
KATMAN_DOLUM_EN_COK = 0.01
OLCEK = float(os.environ.get("OLCEK", "1"))   # senaryo buyuklugu carpani (duyarlilik analizi)
SENARYO_SIRASI = ["kapanis", "yaniltici", "yukseltme", "karsilikli"]
PUANLAR = ["puan_zskor", "puan_kural", "puan_iforest", "puan_kesit_uc", "puan_kesit_iforest"]


def gunsonu(gun):
    return os.path.join(KOK, "veri", "gun-sonu-fiyat-hacim", f"PP_GUNSONUFIYATHACIM.M.{gun[:4]}{gun[5:7]}.parquet")


def senaryo_olaylari(senaryo, g, df, gun, H, rng):
    H = H * OLCEK
    sirali = sorted((i for _, i in g.islemler), key=lambda i: i.zaman)
    tb = g.tablo
    if senaryo == "kapanis":
        kos = kosular(df)
        k = next(j for j, (s, _, _) in enumerate(kos) if s.startswith("P_KAPANIS_EMIR"))
        esl = next((b for s, b, _ in kos[k:] if s in veri.ESLESTIRME), None)
        ref = senaryolar.son_fiyat(sirali, kos[k][1])
        return senaryolar.kapanis_etkileme(kos[k][1], tb, ref, alis=bool(rng.integers(2)),
                                           miktar=max(1, int(H * KAPANIS_ORAN)), kapanis_eslestirme=esl), None
    saniye = int(rng.integers(10 * 3600 + 1800, 17 * 3600))
    t = int(pd.Timestamp(gun).value // 1000) + saniye * 1_000_000
    ref = senaryolar.son_fiyat(sirali, t)
    if ref is None:
        return [], t
    if senaryo == "yaniltici":
        return senaryolar.yaniltici_emir(t, tb, ref, yon_alis=bool(rng.integers(2)), katman=YANILTICI_KATMAN,
                                         adim_uzak=YANILTICI_ADIM, miktar=max(1, int(H * 0.02)),
                                         karsi_miktar=max(1, int(H * 0.002)),
                                         en_iyi=senaryolar.en_iyi_fiyatlar(g.defter_ornekleri, t)), t
    if senaryo == "yukseltme":
        return senaryolar.fiyat_yukseltme(t, tb, ref, adim_sayisi=10, miktar=max(1, int(H * 0.005))), t
    return senaryolar.karsilikli_islem(t, tb, ref, tekrar=10, miktar=max(1, int(H * 0.005))), t


def temiz_degil(senaryo, olaylar, kd):
    """Yaniltici emirde katmanlardan dolan miktar katman toplaminin KATMAN_DOLUM_EN_COK oranini asiyor mu."""
    if senaryo != "yaniltici":
        return False
    return kd > KATMAN_DOLUM_EN_COK * sum(o.miktar for o in olaylar[:YANILTICI_KATMAN])


def puanla(tablo, e):
    d = y.kesitsel(y.isolation_forest(y.kurallar(y.z_skorlari(tablo))))
    return d.merge(e, on=["islem_kodu", "tarih"], how="left")


def olc(d, isaret):
    """isaret: (islem_kodu, tarih) kumesi; donus: yontem basina olcutler."""
    from sklearn.metrics import roc_auc_score
    d = d[d["seviye"].isna()].copy()       # SPK etiketli pay-gunler disarida
    d["poz"] = [(k, t) in isaret for k, t in zip(d["islem_kodu"], d["tarih"])]
    out = []
    for p in PUANLAR:
        x = d[d[p].notna()].copy()
        x["sira"] = x.groupby("tarih")[p].rank(pct=True)
        pz = x[x["poz"]]
        esik = x[p].quantile(0.99)
        tp = int((pz[p] >= esik).sum())
        fp = int(((x[p] >= esik) & ~x["poz"]).sum())
        kes = tp / max(tp + fp, 1)
        duy = tp / max(len(pz), 1)
        out.append(dict(puan=p, enjekte=len(pz), roc_auc=roc_auc_score(x["poz"], x[p]) if 0 < len(pz) < len(x) else np.nan,
                        ort_gun_ici_yuzdelik=pz["sira"].mean(), gun_ici_ilk_yuzde1=(pz["sira"] >= 0.99).mean(),
                        gun_ici_ilk_yuzde5=(pz["sira"] >= 0.95).mean(), kesinlik_ust1=kes, duyarlilik_ust1=duy,
                        f1_ust1=2 * kes * duy / max(kes + duy, 1e-12)))
    return pd.DataFrame(out)


if __name__ == "__main__":
    oz, vaka, out = sys.argv[1:4]
    adet = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    rng = np.random.default_rng(int(sys.argv[5]) if len(sys.argv) > 5 else 0)
    os.makedirs(out, exist_ok=True)
    T = pd.read_parquet(oz)
    T = T[T["ozsermaye"].isna() & T["baz"].notna()].reset_index(drop=True)
    e = y.etiketler(vaka)
    etiketli = set(zip(e["islem_kodu"], e["tarih"]))
    aday = T[(T["tarih"] >= "2025-03-10") & (T["islem_sayisi"] >= ISLEM_EN_AZ)]
    aday = aday[[(k, t) not in etiketli for k, t in zip(aday["islem_kodu"], aday["tarih"])]]
    secim = aday.sample(n=min(adet, len(aday)), random_state=int(rng.integers(1 << 31))).reset_index(drop=True)
    enj, kontrol, kayit, fark = [], [], [], []
    t0 = time.time()
    for n, r in enumerate(secim.itertuples()):
        gun, kod = str(r.tarih.date()), r.islem_kodu
        senaryo = SENARYO_SIRASI[n % len(SENARYO_SIRASI)]
        try:
            df = veri.pay_gun_emirleri(GUNLUK, gun, kod)
            tepe = veri.tepe_tahmini(df)
            gs = gunsonu_ozellikleri(gunsonu(gun), gun).loc[kod]
            H = int(pq_h) if (pq_h := gs.get("hacim_tl", 0) / max(gs["kapanis"], 1e-9)) else 0
            g0 = Gun(df, gun, kod, gunsonu(gun), tepe)
            g0.calistir()
            olaylar, t = senaryo_olaylari(senaryo, g0, df, gun, H, rng)
            g1 = Gun(df, gun, kod, gunsonu(gun), tepe)
            g1.calistir(olaylar)
        except Exception as ex:
            print(gun, kod, senaryo, "HATA", type(ex).__name__, ex, flush=True)
            continue
        kd = senaryolar.katman_dolan(g1, YANILTICI_KATMAN) if senaryo == "yaniltici" else 0
        if temiz_degil(senaryo, olaylar, kd):
            print(gun, kod, senaryo, "temiz degil: katmanlardan", kd, "lot islem gordu", flush=True)
            continue
        s0, s1 = mo.satir(g0, df, gs), mo.satir(g1, df, gs)
        base = {"islem_kodu": kod, "tarih": r.tarih}
        kontrol.append({**base, **s0})
        enj.append({**base, **s1})
        sent = [i for _, i in g1.islemler if g1.sentetik_mi(i)]
        kayit.append(dict(gun=gun, kod=kod, senaryo=senaryo, olay=len(olaylar), kabul=len(g1.kabul),
                          red=len(g1.reddedilen), sentetik_islem=len(sent), sentetik_adet=sum(i.adet for i in sent),
                          katman_dolan=kd,
                          kapanis_taban=s0["kapanis"], kapanis_enj=s1["kapanis"]))
        fark.append({c: s0[c] - getattr(r, c) for c in y.OZELLIKLER if isinstance(s0.get(c), (int, float))})
        print(n + 1, gun, kod, senaryo, kayit[-1]["sentetik_islem"], f"{time.time() - t0:.0f} sn", flush=True)
    K = pd.DataFrame(kayit)
    K.to_csv(os.path.join(out, "sentetik_kayit.csv"), index=False, encoding="utf-8")
    pd.DataFrame(fark).abs().describe().T.to_csv(os.path.join(out, "motor_veri_ozellik_farki.csv"), encoding="utf-8")

    def yerlestir(satirlar):
        X = pd.DataFrame(satirlar)
        anahtar = set(zip(X["islem_kodu"], X["tarih"]))
        kalan = T[[(k, t) not in anahtar for k, t in zip(T["islem_kodu"], T["tarih"])]]
        return pd.concat([kalan, X[[c for c in T.columns if c in X.columns]]], ignore_index=True), anahtar

    R = []
    for ad, satirlar in [("enjeksiyonlu", enj), ("kontrol_enjeksiyonsuz_motor", kontrol)]:
        tablo, anahtar = yerlestir(satirlar)
        d = puanla(tablo, e)
        r_ = olc(d, anahtar)
        r_.insert(0, "kume", ad)
        R.append(r_)
        if ad == "enjeksiyonlu":
            sen = dict(zip(zip(K["kod"], pd.to_datetime(K["gun"])), K["senaryo"]))
            d["senaryo"] = [sen.get((k, t)) for k, t in zip(d["islem_kodu"], d["tarih"])]
            for s_ in SENARYO_SIRASI:
                ss = {a for a in anahtar if sen.get(a) == s_}
                if ss:
                    rs = olc(d[d["senaryo"].isna() | (d["senaryo"] == s_)], ss)
                    rs.insert(0, "kume", "senaryo:" + s_)
                    R.append(rs)
    R = pd.concat(R, ignore_index=True)
    R.to_csv(os.path.join(out, "sentetik_degerlendirme.csv"), index=False, encoding="utf-8")
    print(K.groupby("senaryo")[["sentetik_islem", "red"]].mean().round(1).to_string())
    print(R.round(3).to_string(index=False))
