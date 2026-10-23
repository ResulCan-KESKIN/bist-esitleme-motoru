"""SPK etiketli pay-gunlerde pencere duzeyi (TASARIM.md 6.3): her pay-gun motorla oynatilir, 5 dakikalik pencereler
puanlanir (pencere.py; kapanis penceresi gecmis kapanislara gore); pencere uyarilarindan gun puanlari uretilir ve SPK
etiketleriyle karsilastirilir.

- Pay-gunler: Mart 2025'te SPK etiketli (A, B; belirsiz gunler haric), ayni paylarin etiketsiz gunleri ve rastgele
  RASTGELE pay-gun (surekli islemde en az 300 islem). Ozsermaye gunleri haric.
- Gun puanlari: uyari penceresi sayisi (en az bir kural), bent bazinda uyari sayilari (a/b, d, f), en yuksek pencere
  Z-skor puani.
- Kaldigi yerden devam eder: sonuclar CIKTI_KLASORU/spk_pencere_gun.csv dosyasina pay-gun basina eklenir; bir
  calistirmada en cok ADET pay-gun islenir.
Kullanim: python -I tespit/spk_pencere.py OZELLIKLER.parquet VAKA.csv CIKTI_KLASORU [ADET] [--degerlendir]
"""
import csv, os, sys, time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sentetik_degerlendir as sd
import pencere as pn
import yontemler as y
import motor_ozellikleri as mo
from motor import veri
from motor.gun import Gun
from ozellikler import gunsonu_ozellikleri

RASTGELE = 300
ALANLAR = ["gun", "kod", "grup", "seviye", "pencere", "uyari", "uyari_ab", "uyari_d", "uyari_f", "en_yuksek_z", "hata"]


def secim(T, e):
    lab = e[e["seviye"].isin(["A", "B"])]
    m = T.merge(lab[["islem_kodu", "tarih", "seviye"]], on=["islem_kodu", "tarih"], how="left")
    bel = set(zip(e.loc[e["seviye"] == "B_belirsiz", "islem_kodu"], e.loc[e["seviye"] == "B_belirsiz", "tarih"]))
    m = m[[(k, t) not in bel for k, t in zip(m["islem_kodu"], m["tarih"])]]
    etiketli = m[m["seviye"].notna()].assign(grup="etiketli")
    ayni = m[m["seviye"].isna() & m["islem_kodu"].isin(etiketli["islem_kodu"])].assign(grup="ayni_pay_etiketsiz")
    diger = m[m["seviye"].isna() & ~m["islem_kodu"].isin(etiketli["islem_kodu"]) & (m["islem_sayisi"] >= sd.ISLEM_EN_AZ)]
    diger = diger.sample(n=min(RASTGELE, len(diger)), random_state=0).assign(grup="rastgele")
    return pd.concat([etiketli, ayni, diger], ignore_index=True)


def gun_puani(T, r):
    gun, kod = str(r.tarih.date()), r.islem_kodu
    df = veri.pay_gun_emirleri(sd.GUNLUK, gun, kod)
    tepe = veri.tepe_tahmini(df)
    g = Gun(df, gun, kod, sd.gunsonu(gun), tepe)
    g.calistir()
    W = pn.puanla(pn.pencere_ozellikleri(g, pn.emir_olaylari(df)))
    gecmis = T[(T["islem_kodu"] == kod) & (T["tarih"] < r.tarih)]
    W = pn.kapanis_gecmisi(W, mo.satir(g, df, gunsonu_ozellikleri(sd.gunsonu(gun), gun).loc[kod]), gecmis)
    return dict(pencere=len(W), uyari=int((W["kural_sayisi"] >= 1).sum()), uyari_ab=int(W["kural_ab"].sum()),
                uyari_d=int(W["kural_d"].sum()), uyari_f=int(W["kural_f"].sum()), en_yuksek_z=float(W["puan_zskor"].max()))


def degerlendir(out):
    from sklearn.metrics import roc_auc_score
    d = pd.read_csv(os.path.join(out, "spk_pencere_gun.csv"))
    d = d[d["hata"].isna()]
    d["uyari_orani"] = d["uyari"] / d["pencere"].clip(lower=1)
    R = []
    for ad, poz in [("A", d["seviye"] == "A"), ("B", d["seviye"] == "B"), ("A+B", d["seviye"].isin(["A", "B"]))]:
        for neg_ad, neg in [("ayni_pay", d["grup"] == "ayni_pay_etiketsiz"), ("rastgele", d["grup"] == "rastgele"),
                            ("hepsi", d["grup"] != "etiketli")]:
            x = d[poz | neg]
            for p in ["uyari", "uyari_orani", "uyari_ab", "uyari_d", "uyari_f", "en_yuksek_z"]:
                if 0 < poz[x.index].sum() < len(x):
                    R.append(dict(etiket=ad, negatif=neg_ad, puan=p, pozitif=int(poz[x.index].sum()), negatif_n=int(neg[x.index].sum()),
                                  roc_auc=roc_auc_score(poz[x.index], x[p])))
    R = pd.DataFrame(R)
    R.to_csv(os.path.join(out, "spk_pencere_degerlendirme.csv"), index=False, encoding="utf-8")
    ozet = d.groupby(["grup", d["seviye"].fillna("-")])[["uyari", "uyari_orani", "uyari_ab", "uyari_d", "uyari_f", "en_yuksek_z"]].mean()
    ozet.to_csv(os.path.join(out, "spk_pencere_ozet.csv"), encoding="utf-8")
    print(ozet.round(3).to_string())
    print(R[R["negatif"] == "hepsi"].round(3).to_string(index=False))


if __name__ == "__main__":
    arg = [a for a in sys.argv[1:] if not a.startswith("--")]
    oz, vaka, out = arg[:3]
    adet = int(arg[3]) if len(arg) > 3 else 10 ** 9
    os.makedirs(out, exist_ok=True)
    if "--degerlendir" in sys.argv:
        degerlendir(out)
        sys.exit()
    T = pd.read_parquet(oz)
    T = T[T["ozsermaye"].isna() & T["baz"].notna()].reset_index(drop=True)
    S = secim(T, y.etiketler(vaka))
    yol = os.path.join(out, "spk_pencere_gun.csv")
    bitti = set()
    if os.path.exists(yol):
        bitti = {(r["gun"], r["kod"]) for r in csv.DictReader(open(yol, encoding="utf-8"))}
    yeni = not os.path.exists(yol)
    t0, n = time.time(), 0
    with open(yol, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ALANLAR)
        if yeni:
            w.writeheader()
        for r in S.itertuples():
            gun = str(r.tarih.date())
            if (gun, r.islem_kodu) in bitti:
                continue
            if n >= adet:
                break
            satir = dict(gun=gun, kod=r.islem_kodu, grup=r.grup, seviye=r.seviye if isinstance(r.seviye, str) else "", hata="")
            try:
                satir.update(gun_puani(T, r))
            except Exception as ex:
                satir["hata"] = f"{type(ex).__name__}: {ex}"
            w.writerow(satir)
            f.flush()
            n += 1
    print(f"{n} pay-gun islendi, toplam {len(bitti) + n}/{len(S)}, {time.time() - t0:.0f} sn")
