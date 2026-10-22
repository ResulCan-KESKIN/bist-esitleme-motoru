"""SPK etiketlerinin aylara gore dagilimi (emir/ITCH verisi alinacak ay secimi icin).

A: donemi (nihai_donem_bas..nihai_donem_bit) ayla kesisen vakalar.
B: tedbir oncesi N islem gunu pencere (N kararsiz; N=20 ve yalniz N=40 ile eklenenler ayri) ayla kesisen vakalar.
Kullanim: python -I etiket_ay_ortusmesi.py VAKA.csv ILK_AY SON_AY CIKTI.csv   (aylar YYYY-MM)
"""
import sys
import pandas as pd

src, ilk, son, out = sys.argv[1:5]
v = pd.read_csv(src, dtype=str)
e = v[v.etiket_nihai == "1"].copy()
for c in ["nihai_donem_bas", "nihai_donem_bit", "nihai_tedbir_bas"]:
    e[c] = pd.to_datetime(e[c], errors="coerce")
e = e.drop_duplicates(["pay_kodu", "seviye_nihai", "nihai_donem_bas", "nihai_donem_bit", "nihai_tedbir_bas"])
satir = []
for ay in pd.period_range(ilk, son, freq="M"):
    a0, a1 = ay.start_time, ay.end_time
    A = e[(e.seviye_nihai == "A") & (e.nihai_donem_bas <= a1) & (e.nihai_donem_bit >= a0)]
    a_list = sorted({f"{r.pay_kodu} ({r.nihai_donem_bas:%d.%m.%Y}-{r.nihai_donem_bit:%d.%m.%Y})" for r in A.itertuples()})
    b = {20: set(), 40: set()}
    for r in e[(e.seviye_nihai == "B") & e.nihai_tedbir_bas.notna()].itertuples():
        for n in b:
            b0, b1 = r.nihai_tedbir_bas - pd.offsets.BDay(n), r.nihai_tedbir_bas - pd.Timedelta(days=1)
            if b0 <= a1 and b1 >= a0:
                b[n].add(f"{r.pay_kodu} (tedbir {r.nihai_tedbir_bas:%d.%m.%Y})")
    satir.append(dict(ay=str(ay), A_sayi=len({x.split(" ")[0] for x in a_list}), A_vakalar="; ".join(a_list),
                      B_sayi_N20=len(b[20]), B_vakalar_N20="; ".join(sorted(b[20])),
                      yalniz_N40_ile_eklenen_B="; ".join(sorted(b[40] - b[20]))))
T = pd.DataFrame(satir)
T.to_csv(out, index=False, encoding="utf-8-sig")
print(T.to_string())
