"""gunici_emir_kural_kontrol.py ciktilarini (bir ya da daha fazla parca klasoru) birlestirir ve ozetler.

Kullanim: python -I gunici_emir_kural_ozet.py CIKTI_KLASORU PARCA_KLASORU [PARCA_KLASORU ...]
"""
import sys, os, glob
import pandas as pd

out, parcalar = sys.argv[1], sys.argv[2:]
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 300)
T = {}
for p in parcalar:
    for f in glob.glob(os.path.join(p, "*.csv")):
        ad = os.path.basename(f)[:-4]
        T.setdefault(ad, []).append(pd.read_csv(f))
for ad, ls in T.items():
    d = pd.concat(ls)
    keys = [c for c in d.columns if c != "adet"]
    T[ad] = d.groupby(keys, dropna=False).adet.sum().reset_index()
    T[ad].to_csv(os.path.join(out, ad + ".csv"), index=False, encoding="utf-8")


def yaz(baslik, x):
    print("\n==", baslik)
    print(x.to_string())


d = T["degisiklik"]
yaz("degisiklik: kategori x giris_degisti", d.groupby(["emir_kategorisi", "giris_degisti", "giris_eq_deg"]).adet.sum())
n = d[d.emir_kategorisi == 1]
yaz("normal emir degisiklikleri: bolum x fiyat x miktar",
    n.groupby(["seans", "fiyat_yon", "miktar_yon"]).adet.sum().unstack(["fiyat_yon", "miktar_yon"], fill_value=0))
s = T["sebep_seans_durum"]
yaz("kullanici iptali (sebep 1) bolum bazinda", s[s.degisiklik_sebebi == 1].groupby("seans").adet.sum())
yaz("ilk satir sebebi", T["ilk_satir_sebebi"].groupby(["grup", "degisiklik_sebebi", "emir_durumu"]).adet.sum())
yaz("guncelleme_no atlama", T["guncelleme_no_atlama"].groupby(["grup", "atlama"]).adet.sum())
yaz("islem satiri tutarliligi", T["islem_satiri"].groupby(["grup", "kalan_tutarli", "miktar_sabit", "giris_sabit"]).adet.sum())
yaz("KIE aktif satirlari", T["kie_aktif"].groupby(["grup", "seans"]).adet.sum())
z = T["emir_son_durum"]
yaz("emrin son satiri (pay)", z[z.grup == "pay"].groupby(["emir_durumu", "degisiklik_sebebi", "seans"]).adet.sum())
y = T["yeni_emir_pazar"]
ac = y[(y.sonek == "E") & y.seans.str.contains("ACILIS|ACS_")]
yaz("aciliste yeni emir: pazar x fiyat turu", ac.groupby(["pazar", "emir_fiyat_turu"]).adet.sum().unstack(fill_value=0))
yaz("kapanis seansi +-%3", T["kapanis_yuzde3"].groupby(["ref", "durum", "gunluk_sinir_icinde", "sebep"]).adet.sum())
yaz("kapanis fiyatindan islemler: emir fiyati = kapanis fiyati", T["kfi_fiyat"].groupby(["degisiklik_sebebi", "esit"]).adet.sum())
ss = T["sistem_sebep"]
yaz("sistem sebepleri", ss.groupby(["degisiklik_sebebi", "seans", "onceki_durum", "emir_durumu", "fiyat_degisti",
                                   "kalan_degisti"]).adet.sum().sort_values(ascending=False).head(40))
