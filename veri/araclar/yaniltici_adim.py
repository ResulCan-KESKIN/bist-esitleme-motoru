"""pencere_degerlendir.py'yi YANILTICI_ADIM ortam degiskeniyle calistirir (kod degistirilmeden).
Kullanim: YANILTICI_ADIM=0 python -I yaniltici_adim.py OZELLIKLER.parquet VAKA.csv CIKTI 80 11"""
import os, sys, runpy

KOK = "D:/Bitirme/proje"
sys.path.insert(0, KOK)
sys.path.insert(0, os.path.join(KOK, "tespit"))
import sentetik_degerlendir as sd

sd.YANILTICI_ADIM = int(os.environ["YANILTICI_ADIM"])
print("YANILTICI_ADIM =", sd.YANILTICI_ADIM, flush=True)
betik = os.path.join(KOK, "tespit", "pencere_degerlendir.py")
sys.argv = [betik] + sys.argv[1:]
runpy.run_path(betik, run_name="__main__")
