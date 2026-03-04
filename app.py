import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- KONSEY ANALİZ YAPILANDIRMASI ---
st.set_page_config(page_title="Geopolitical War Room V2.2", layout="wide")
st.title("🏛️ Küresel Hegemonya ve Sistemik Risk Analizörü (V2.2)")

# --- 1. VERİ MERKEZİ ---
@st.cache_data(ttl=3600)
def fetch_geopolitical_proxies():
    tickers = {
        "DXY": "DX-Y.NYB",       # Hegemon Gücü
        "VIX": "^VIX",            # Sistemik Korku
        "BRENT": "BZ=F",          # Enerji Darboğazı (Hürmüz Proxy)
        "GOLD": "GC=F",           # Güvenli Liman
        "LMT": "LMT",             # Savunma Sanayii (Savaş Beklentisi)
        "BDRY": "BDRY"            # Tedarik Zinciri (Navlun/Lojistik Proxy)
    }
    data = {}
    for name, t in tickers.items():
        ticker = yf.Ticker(t)
        hist = ticker.history(period="1mo")
        data[name] = {
            "last": hist['Close'].iloc[-1],
            "volatility": hist['Close'].pct_change().std() * 100,
            "change": ((hist['Close'].iloc[-1] / hist['Close'].iloc[-2]) - 1) * 100
        }
    return data

geo_data = fetch_geopolitical_proxies()

# --- 2. GELİŞMİŞ PARAMETRE GİRİŞLERİ (MANUEL + PROXY) ---
st.sidebar.header("🕹️ Stratejik Parametreler")

# Nükleer Caydırıcılık (Deterrence Factor)
# 1: Düşük Caydırıcılık (Riskli), 5: Yüksek Caydırıcılık (Stabil)
deterrence = st.sidebar.slider("Nükleer Caydırıcılık Seviyesi (M.A.D.)", 1.0, 5.0, 3.5)
st.sidebar.caption("Yüksek değer, nükleer eşiğin çatışmayı frenlediğini simgeler.")

# Tedarik Zinciri Kırılganlığı (Supply Chain Fragility)
supply_fragility = geo_data["BDRY"]["volatility"] * 2 

# --- 3. SAVAŞ OLASILIĞI ALGORİTMASI (V2.2) ---
st.header("⚔️ Gelişmiş Savaş Olasılığı ve Çöküş Modeli")

# Ağırlıklar
w_oil = 0.30
w_gold = 0.25
w_supply = 0.25
w_defense = 0.20

# Ham Risk Skoru
raw_risk = (geo_data["BRENT"]["volatility"] * w_oil) + \
           (geo_data["GOLD"]["volatility"] * w_gold) + \
           (supply_fragility * w_supply) + \
           (geo_data["LMT"]["volatility"] * w_defense)

# Caydırıcılık Filtresi ve VIX Çarpanı
# Formül: (Risk / Caydırıcılık) * Log(VIX)
cpi_score = (raw_risk / deterrence) * np.log1p(geo_data["VIX"]["last"])
war_probability = min(cpi_score * 5, 99.9)

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Savaş Olasılığı (CPI)", f"%{war_probability:.2f}")
    st.write(f"**Nükleer Frenleme:** {deterrence}x")
    st.write(f"**Tedarik Zinciri Baskısı:** {supply_fragility:.2f}")
    
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

# --- 4. SİSTEMİK İZLEME PANELİ ---
st.divider()
st.subheader("📡 Yapısal Kırılganlık Göstergeleri")
c3, c4, c5 = st.columns(3)

c3.metric("Navlun Volatilitesi (BDRY)", f"{geo_data['BDRY']['volatility']:.2f}%")
c4.metric("Savunma Primi (LMT)", f"{geo_data['LMT']['last']:.2f}$", f"{geo_data['LMT']['change']:.2f}%")
c5.metric("Hegemon Gücü (DXY)", f"{geo_data['DXY']['last']:.2f}")

st.info("🛡️ **Konsey Analizi:** Nükleer caydırıcılık, büyük güçler arasındaki doğrudan kinetik teması engellerken; "
        "tedarik zinciri kırılganlığı 'ekonomik boğulma' riskini ölçer. Navlun (BDRY) fiyatlarındaki aşırı volatilite, "
        "darboğazlardaki fiziksel tıkanıklığın en rasyonel öncü göstergesidir.")
