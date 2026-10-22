"""BIST Pay Piyasasi eslestirme motoru (TASARIM.md 4). Python basvuru uygulamasi."""
import os as _os, sys as _sys

# denge fiyati algoritmasi ve fiyat adimi tablolari: veri/araclar/tek_fiyat_algoritma.py
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "veri", "araclar"))
