"""Gorsellestirme ve emir enjeksiyon arayuzu (TASARIM.md 6.5).

Calistirma: streamlit run arayuz/uygulama.py
- Pay ve gun secilir; gercek emir akisi motorda oynatilir (taban cizgisi).
- Senaryo secilirse sentetik emirler enjekte edilir; enjeksiyonlu fiyat taban cizgisiyle ayni grafikte gosterilir,
  sentetik aktorun islemleri isaretlenir.
- Uyarilar: 5 dakikalik pencere kurallari (tespit/pencere.py; VI-104.1 md 5/1 a/b, d, f). Bolum bantlari: muzayede,
  devre kesici, EBDKS.
"""
import os, sys

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hazirla

# reference palette (dataviz skill): categorical slots 1-2, status "serious"; light / dark steps
RENK = {"light": dict(s1="#2a78d6", s2="#eb6834", yuzey="#fcfcfb", bant="#f0efec", metin="#52514e", izgara="#e6e5e0"),
        "dark": dict(s1="#3987e5", s2="#d95926", yuzey="#1a1a19", bant="#383835", metin="#c3c2b7", izgara="#2e2e2c")}
UYARI = "#ec835a"
SENARYOLAR = {"(yok)": None, "Kapanış fiyatını etkileme": "kapanis", "Yanıltıcı emir (spoofing)": "yaniltici",
              "Adım adım fiyat yükseltme": "yukseltme", "Karşılıklı işlem": "karsilikli"}

st.set_page_config(page_title="Eşleştirme motoru", layout="wide")
tema = "dark" if getattr(getattr(st.context, "theme", None), "type", "light") == "dark" else "light"
R = RENK[tema]


@st.cache_data(show_spinner="Motor oynatılıyor…")
def oynat(gun, kod, senaryo, saat, param):
    return hazirla.oynat(gun, kod, senaryo, saat, **dict(param))


with st.sidebar:
    st.header("Oynatma")
    gun = st.selectbox("Gün", hazirla.gunler())
    kodlar = hazirla.siralar(gun)
    kod = st.selectbox("Pay", kodlar, index=kodlar.index("THYAO.E") if "THYAO.E" in kodlar else 0)
    st.header("Enjeksiyon")
    sen_ad = st.selectbox("Senaryo", list(SENARYOLAR))
    senaryo = SENARYOLAR[sen_ad]
    saat, param = None, {}
    if senaryo and senaryo != "kapanis":
        saat = st.text_input("Saat (SS:DD:ss)", "14:00:00")
    if senaryo == "kapanis":
        param = dict(alis=st.radio("Yön", ["Alış", "Satış"], horizontal=True) == "Alış",
                     miktar=st.number_input("Miktar (lot)", 1, 10_000_000, 100_000, step=10_000),
                     saniye_once=st.number_input("Eşleştirmeden kaç sn önce", 1, 200, 10))
    elif senaryo == "yaniltici":
        param = dict(yon_alis=st.radio("Yanıltıcı emir yönü", ["Satış", "Alış"], horizontal=True) == "Alış",
                     katman=st.number_input("Katman", 1, 10, 3), adim_uzak=st.number_input("En iyi fiyatın gerisinde adım", 1, 20, 2),
                     miktar=st.number_input("Katman miktarı", 1, 10_000_000, 50_000, step=10_000),
                     sure_sn=st.number_input("Süre (sn)", 1, 600, 30),
                     karsi_miktar=st.number_input("Karşı emir miktarı", 1, 1_000_000, 1_000),
                     karsi_agresif=st.radio("Karşı emir", ["Agresif", "Pasif"], horizontal=True) == "Agresif")
    elif senaryo == "yukseltme":
        param = dict(adim_sayisi=st.number_input("Adım sayısı", 1, 50, 10), aralik_sn=st.number_input("Aralık (sn)", 1, 600, 20),
                     miktar=st.number_input("Emir miktarı", 1, 10_000_000, 20_000, step=1_000))
    elif senaryo == "karsilikli":
        param = dict(tekrar=st.number_input("Tekrar", 1, 50, 5), aralik_sn=st.number_input("Aralık (sn)", 1, 600, 60),
                     miktar=st.number_input("Miktar", 1, 10_000_000, 5_000, step=1_000))
    calis = st.button("Oynat", type="primary", width="stretch")

st.title(f"{kod} · {gun}")
if not calis and "sonuc" not in st.session_state:
    st.info("Gün, pay ve isteğe bağlı bir senaryo seçip **Oynat**'a basın.")
    st.stop()
if calis:
    st.session_state["sonuc"] = (gun, kod, sen_ad, oynat(gun, kod, senaryo, saat, tuple(sorted(param.items()))))
gun, kod, sen_ad, r = st.session_state["sonuc"]
oz = r["ozet"]
et = hazirla.spk_etiketi(gun, kod)
if et:
    aciklama = {"A": "manipülasyon döneminin içinde (dönem bültende yazılı)",
                "B": "işlem yasağından önceki 20 işlem günlük pencerede (varsayım)",
                "B_belirsiz": "yasaktan önceki 2 iş günü (değerlendirme dışı)"}
    st.warning(f"SPK etiketi: **{et[0]}** · bülten {et[1]} · bu gün {aciklama.get(et[0], '')}")

c = st.columns(4)
c[0].metric("Kapanış (taban)", f"{oz['kapanis_taban']:.2f}" if oz["kapanis_taban"] else "—")
c[1].metric("Kapanış (enjeksiyonlu)" if r["enjeksiyonlu"] is not None else "Kapanış",
            f"{oz['kapanis']:.2f}" if oz["kapanis"] else "—",
            f"{oz['kapanis'] - oz['kapanis_taban']:+.2f}" if r["enjeksiyonlu"] is not None and oz["kapanis"] else None)
c[2].metric("Sentetik işlem / adet", f"{oz['sentetik_islem']} / {oz['sentetik_adet']:,}".replace(",", "."))
c[3].metric("Kural uyarısı (5 dk pencere)", oz["uyari"])


def bantlar(fig):
    for b in r["bantlar"].itertuples():
        fig.add_vrect(x0=b.bas, x1=b.bit, fillcolor=R["bant"], opacity=0.8, layer="below", line_width=0,
                      annotation_text=b.ad, annotation_position="top left", annotation_font_size=10,
                      annotation_font_color=R["metin"])


def duzen(fig, baslik, ybaslik):
    fig.update_layout(title=dict(text=baslik, font_size=15), height=380, margin=dict(l=10, r=10, t=50, b=10),
                      hovermode="x unified", plot_bgcolor=R["yuzey"], paper_bgcolor=R["yuzey"],
                      font_color=R["metin"], legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(showgrid=False, showspikes=True, spikemode="across", spikethickness=1)
    fig.update_yaxes(title_text=ybaslik, gridcolor=R["izgara"], zeroline=False)


# fiyat
fig = go.Figure()
bantlar(fig)
tb = r["taban"]
ej = r["enjeksiyonlu"]
if ej is not None:   # once enjeksiyonlu: taban cizgisi ustte kalir, turuncu yalniz ayristigi yerde gorunur
    fig.add_trace(go.Scatter(x=ej["zaman"], y=ej["fiyat"], mode="lines", line=dict(color=R["s2"], width=2, shape="hv"),
                             name="Enjeksiyonlu", hovertemplate="%{y:.2f} TL<extra>enjeksiyonlu</extra>"))
fig.add_trace(go.Scatter(x=tb["zaman"], y=tb["fiyat"], mode="lines", line=dict(color=R["s1"], width=2, shape="hv"),
                         name="Gerçek akış (motor)", hovertemplate="%{y:.2f} TL<extra>gerçek akış</extra>"))
if ej is not None:
    s = ej[ej["sentetik"]]
    fig.add_trace(go.Scatter(x=s["zaman"], y=s["fiyat"], mode="markers", name="Sentetik aktörün işlemi",
                             marker=dict(color=R["s2"], size=9, line=dict(color=R["yuzey"], width=2)),
                             customdata=s[["adet", "bolum"]], hovertemplate="%{y:.2f} TL · %{customdata[0]} lot · "
                             "%{customdata[1]}<extra>sentetik</extra>"))
dk = r["dakika_enj"] if r["dakika_enj"] is not None else r["dakika_taban"]
u = r["uyarilar"]
fig.add_trace(go.Scatter(x=u["bas"], y=u["fiyat"], mode="markers", name="⚠ Kural uyarısı (5 dk)",
                         marker=dict(symbol="triangle-up", color=UYARI, size=11, line=dict(color=R["yuzey"], width=2)),
                         customdata=u[["bentler", "puan_zskor"]],
                         hovertemplate="⚠ bent %{customdata[0]} · en büyük |z| %{customdata[1]:.1f}<extra>uyarı</extra>"))
duzen(fig, "İşlem fiyatı", "TL")
st.plotly_chart(fig, width="stretch")

# hacim (ayri grafik: tek eksen)
fig2 = go.Figure()
bantlar(fig2)
fig2.add_trace(go.Bar(x=dk["dakika"], y=dk["hacim"], marker=dict(color=R["s1"], line_width=0), name="Dakikalık hacim",
                      hovertemplate="%{y:,} lot<extra>hacim</extra>"))
duzen(fig2, "Sürekli işlem dakikalık hacim" + (" (enjeksiyonlu)" if ej is not None else ""), "lot")
fig2.update_layout(bargap=0.15)
st.plotly_chart(fig2, width="stretch")

t0, t1, t2, t3 = st.tabs(["Uyarılar (5 dk)", "Sentetik işlemler", "Reddedilen sentetik olaylar", "Dakikalık tablo"])
with t0:
    st.dataframe(u, width="stretch", hide_index=True)
with t1:
    st.dataframe(ej[ej["sentetik"]] if ej is not None else pd.DataFrame(), width="stretch", hide_index=True)
with t2:
    st.dataframe(r["reddedilen"], width="stretch", hide_index=True)
with t3:
    st.dataframe(dk, width="stretch", hide_index=True)
