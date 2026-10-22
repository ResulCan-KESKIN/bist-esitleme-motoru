"""Toplu tekrar oynatma: bir gunun butun pay siralarini (.E, pay pazarlari) tekrar_oynat.calistir ile oynatir,
sira basina ozet satirini CSV'ye yazar (her sira bittikce eklenir; yarida kalirsa kaldigi yerden devam eder).

Kullanim: python -I motor/toplu_oynat.py GUNLUK_EMIR_KLASORU ISLEM.parquet GUNSONU.parquet GUN CIKTI.csv
"""
import csv, os, sys, time, traceback

import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor import veri
from motor.tekrar_oynat import calistir

PAY_PAZARLARI = ("Z", "N", "T", "W", "S")
ALANLAR = ["kod", "gun", "mod", "hata", "kismi_gorunme_emir", "muzayede_sayisi", "muzayede_fiyatlari",
           "gun_islem_gercek", "gun_islem_motor", "gun_islem_ortak", "gun_emir_gerceklesen_ayni",
           "islem_gercek", "islem_motor", "islem_ortak", "emir_gerceklesen_ayni",
           "muzayede_islem_gercek", "muzayede_islem_ortak", "muzayede_emir_gerceklesen_ayni",
           "ebdks_muzayede_islem_gercek", "ebdks_muzayede_islem_ortak", "ebdks_muzayede_emir_gerceklesen_ayni",
           "kfi_islem_gercek", "kfi_islem_ortak", "sayac", "sure_sn"]


def siralar(gunsonu, gun, gunluk):
    import datetime
    t = pq.read_table(gunsonu, columns=["trade_date", "instrument_series_code", "market_segment"],
                      filters=[("trade_date", "=", datetime.date.fromisoformat(gun))]).to_pylist()
    var = veri._kod_dosyasi(gunluk, gun)
    return sorted(r["instrument_series_code"] for r in t
                  if r["instrument_series_code"].endswith(".E") and r["market_segment"] in PAY_PAZARLARI
                  and r["instrument_series_code"] in var)


if __name__ == "__main__":
    gunluk, islem_parquet, gunsonu, gun, cikti = sys.argv[1:6]
    bitti = set()
    if os.path.exists(cikti):
        with open(cikti, encoding="utf-8") as f:
            bitti = {r["kod"] for r in csv.DictReader(f)}
    yeni = not os.path.exists(cikti)
    kodlar = [k for k in siralar(gunsonu, gun, gunluk) if k not in bitti]
    print(f"{gun}: {len(kodlar)} sira (tamamlanan {len(bitti)})", flush=True)
    t0 = time.time()
    with open(cikti, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ALANLAR, extrasaction="ignore")
        if yeni:
            w.writeheader()
        for n, kod in enumerate(kodlar, 1):
            try:
                ozet, _, _ = calistir(gunluk, islem_parquet, gun, kod, gunsonu)
                ozet["hata"] = ""
            except Exception as e:
                ozet = {"kod": kod, "gun": gun, "hata": f"{type(e).__name__}: {e}"}
                traceback.print_exc()
            w.writerow(ozet)
            f.flush()
            if n % 25 == 0:
                print(f"{n}/{len(kodlar)} {time.time() - t0:.0f} sn", flush=True)
    print("bitti", round(time.time() - t0), "sn")
