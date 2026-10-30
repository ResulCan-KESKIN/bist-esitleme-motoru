"""Belge PDF'lerini uretir: ANLATIM, DURUM, TASARIM (md -> HTML -> PDF) ve VERI (HTML -> PDF).

Kullanim: python -I pdf-kaynak/uret.py [--cikti KLASOR] [ANLATIM] [DURUM] [TASARIM] [VERI]
Belge verilmezse dordu de uretilir; PDF'ler varsayilan olarak proje kokune yazilir.
Basim Microsoft Edge (headless) ile yapilir.
"""
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

KLASOR = Path(__file__).resolve().parent
KOK = KLASOR.parent
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

# belge -> md parcalari (sirayla birlestirilir); VERI dogrudan HTML'dir
KAYNAK = {
    "ANLATIM": [KLASOR / "ANLATIM-on-bilgi.md", KOK / "ANLATIM.md"],
    "DURUM": [KLASOR / "DURUM-anlatim.md"],
    "TASARIM": [KLASOR / "TASARIM-anlatim.md"],
    "VERI": [KLASOR / "VERI.html"],
}


def bas(html, pdf, profil):
    if pdf.exists():
        pdf.unlink()
    subprocess.run([str(EDGE), "--headless", "--disable-gpu", f"--user-data-dir={profil}",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri()], check=True)
    # Edge cikis yaptiktan sonra dosyanin yazilmasini bekle
    for _ in range(60):
        if pdf.exists() and pdf.stat().st_size > 0:
            return
        time.sleep(0.5)
    raise RuntimeError(f"PDF uretilmedi: {pdf}")


def main(argv):
    cikti = KOK
    if "--cikti" in argv:
        i = argv.index("--cikti")
        cikti = Path(argv[i + 1]).resolve()
        argv = argv[:i] + argv[i + 2:]
    belgeler = argv or list(KAYNAK)
    for b in belgeler:
        if b not in KAYNAK:
            sys.exit(f"bilinmeyen belge: {b} (secenekler: {', '.join(KAYNAK)})")
    gecici = Path(tempfile.mkdtemp(prefix="pdf_uret_"))
    try:
        for b in belgeler:
            parcalar = KAYNAK[b]
            if parcalar[0].suffix == ".html":
                html = parcalar[0]
            else:
                md = gecici / f"{b}.md"
                md.write_text("".join(p.read_text(encoding="utf-8") for p in parcalar), encoding="utf-8")
                html = gecici / f"{b}.html"
                subprocess.run([sys.executable, "-I", str(KLASOR / "md2html.py"), str(md), str(html),
                                str(KLASOR / "stil.css")], check=True)
            pdf = cikti / f"{b}.pdf"
            bas(html, pdf, gecici / "edge")
            print(b, "->", pdf, pdf.stat().st_size, "bayt")
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


if __name__ == "__main__":
    main(sys.argv[1:])
