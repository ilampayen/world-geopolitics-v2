import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests

# --- KONSEY ANALİZ YAPILANDIRMASI ---
st.set_page_config(page_title="Geopolitical War Room V2.2", layout="wide")
st.title("🏛️ Küresel Hegemonya ve Sistemik Risk Analizörü (V2.2)")

# --- 1. DİJİTAL SIZMA PROTOKOLÜ (RATE LIMIT BYPASS) ---
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
})

@st.cache_data(ttl=3600)
def fetch_geopolitical_proxies():
    tickers = {
        "DXY": "DX-Y.NYB",       # Hegemon Gücü
        "VIX": "^VIX",            # Sistemik Korku
        "BRENT": "BZ=F",          # Enerji Darboğazı
        "GOLD": "GC=F",           # Güvenli Liman
        "LMT": "LMT",             # Savunma Sanayii (Savaş Beklentisi)
        "BDRY": "BDRY"            # Tedarik Zinciri (Lojistik)
    }
    data = {}
    
    for name, t in tickers.items():
        try:
            # Oturum mühimmatı ile veri çekme
            ticker = yf.Ticker(t, session=session)
            hist = ticker.history(period="1mo")
            
            if hist.empty:
                raise ValueError(f"{name} verisi boş")

            data[name] = {
                "last": hist['Close'].iloc[-1],
                "volatility": hist['Close'].pct_change().std() * 100,
                "change": ((hist['Close'].iloc[-1] / hist['Close'].iloc[-2]) - 1) * 100
            }
        except Exception:
            # Safe Mode: Veri çekilemezse sistem durmaz, nötr değer döner
            data[name] = {"last": 100.0, "volatility": 0.5, "change": 0.0}
            
    return data

# Veri yükleme
with st.spinner('Jeopolitik veriler süzülüyor...'):
    geo_data = fetch_geopolitical_proxies()

# --- 2. STRATEJİK PARAMETRE GİRİŞLERİ ---
st.sidebar.header("🕹️ Stratejik Parametreler")

# Nükleer Caydırıcılık (Deterrence Factor)
# 1: Düşük Caydırıcılık, 5: Yüksek Caydırıcılık
deterrence = st.sidebar.slider("Nükleer Caydırıcılık (M.A.D.)", 1.0, 5.0, 3.5)
st.sidebar.caption("Yüksek değer, nükleer dehşet dengesinin savaşı frenlediğini simgeler.")

# Tedarik Zinciri Kırılganlığı (Supply Chain Fragility)
# Navlun volatilitesini risk çarpanı olarak kullanıyoruz
supply_fragility = geo_data["BDRY"]["volatility"] * 2 

# --- 3. SAVAŞ OLASILIĞI ALGORİTMASI (V2.2) ---
st.header("⚔️ Gelişmiş Savaş Olasılığı ve Çöküş Modeli")

# Ağırlık Katsayıları (Rasyonel Sabitler)
w_oil = 0.30
w_gold = 0.25
w_supply = 0.25
w_defense = 0.20

# Ham Risk Hesabı
raw_risk = (geo_data["BRENT"]["volatility"] * w_oil) + \
           (geo_data["GOLD"]["volatility"] * w_gold) + \
           (supply_fragility * w_supply) + \
           (geo_data["LMT"]["volatility"] * w_defense)

# Caydırıcılık Filtresi ve VIX Duyarlılığı
# Formül: (Raw_Risk / Deterrence) * Log(VIX)
cpi_score = (raw_risk / deterrence) * np.log1p(geo_data["VIX"]["last"])
war_probability = min(cpi_score * 5, 99.9)

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Savaş Olasılığı (CPI)", f"%{war_probability:.2f}")
    st.write(f"**Nükleer Frenleme:** {deterrence}x")
    st.write(f"**Lojistik Kırılganlık:** {supply_fragility:.2f}")
    
    if war_probability > 75:
        st.error("KRİTİK: Sistemik çöküş ve topyekün çatışma riski.")
    elif war_probability > 45:
        st.warning("YÜKSEK: Yapısal kırılmalar ve bölgesel savaşlar.")
    else:
        st.success("DÜŞÜK: Hegemonik istikrar ve caydırıcılık aktif.")

with col2:
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = war_probability,
        title = {'text': "Conflict & Collapse Probability"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkred"},
            'steps' : [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "red"}]}))
    st.plotly_chart(fig, use_container_width=True)

# --- 4. YAPI SAL KIRILGANLIK GÖSTERGELERİ ---
st.divider()
st.subheader("📡 Jeopolitik Isı Haritası Verileri")
c3, c4, c5 = st.columns(3)

c3.metric("Lojistik Baskı (BDRY Vol)", f"{geo_data['BDRY']['volatility']:.2f}%")
c4.metric("Savunma Primi (LMT)", f"{geo_data['LMT']['last']:.2f}$", f"{geo_data['LMT']['change']:.2f}%")
c5.metric("Hegemon Gücü (DXY)", f"{geo_data['DXY']['last']:.2f}")

st.info("🛡️ **Konsey Analizi:** Nükleer caydırıcılık (M.A.D.), paydadaki dengeleyici güçtür. "
        "Eğer Navlun (BDRY) ve Petrol (Brent) volatilitesi aynı anda yükseliyorsa, "
        "bu durum piyasa korkusundan bağımsız bir 'fiziksel çöküş' sinyalidir.")
