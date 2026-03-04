import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- ANALİZ YAPILANDIRMASI ---
st.set_page_config(page_title="Geopolitical War Room", layout="wide")
st.title("🏛️ Küresel Hegemonya ve Savaş Olasılığı Analizörü (V2.1)")

# --- VERİ ÇEKME FONKSİYONU ---
@st.cache_data(ttl=3600)
def fetch_geopolitical_proxies():
    tickers = {
        "DXY": "DX-Y.NYB",       # Hegemon Gücü
        "VIX": "^VIX",            # Sistemik Korku
        "BRENT": "BZ=F",          # Enerji Darboğazı
        "GOLD": "GC=F",           # Güvenli Liman
        "SPY": "SPY",             # Batı Sermaye Gücü
        "EEM": "EEM"              # Gelişen Piyasalar (Doğu Bloku Proxy)
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

# --- 1. SAVAŞ OLASILIĞI ALGORİTMASI (CPA) ---
st.header("⚔️ Savaş Olasılığı ve Sistemik Risk Modeli")

# Ağırlıklı Risk Katsayıları
w_oil = 0.35
w_gold = 0.30
w_vix = 0.20
w_dxy = 0.15

# Olasılık Hesaplama (Normalize Edilmiş Skor)
raw_score = (geo_data["BRENT"]["volatility"] * w_oil) + \
            (geo_data["GOLD"]["volatility"] * w_gold) + \
            (geo_data["VIX"]["last"] / 50 * w_vix) + \
            (abs(geo_data["DXY"]["change"]) * w_dxy)

war_probability = min(raw_score * 10, 99.9) # 0-100 arası ölçeklendirme

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Savaş Olasılığı Endeksi (CPI)", f"%{war_probability:.2f}")
    if war_probability > 70:
        st.error("KRİTİK: Büyük güç çatışması eşiği (Kinetic Conflict Threshold) aşıldı.")
    elif war_probability > 40:
        st.warning("ALARM: Hibrit savaş ve vekalet çatışmaları yoğunlaşıyor.")
    else:
        st.success("STABİL: Hegemonik denge korunuyor.")

with col2:
    # Gösterge Paneli
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = war_probability,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Conflict Probability Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'steps' : [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "red"}]}))
    st.plotly_chart(fig, use_container_width=True)

# --- 2. HEGEMONYA NABZI (BATI VS DOĞU) ---
st.divider()
st.subheader("📡 Güç Dengesi ve Kutuplaşma (Western vs. Emerging)")
col3, col4, col5 = st.columns(3)

# Batı (SPY) vs Gelişen (EEM) Rasyosu
relative_strength = geo_data["SPY"]["last"] / geo_data["EEM"]["last"]
col3.metric("Hegemonik Üstünlük Rasyosu", f"{relative_strength:.2f}")
col3.caption("Artış: ABD Hegemonyası güçleniyor. Azalış: Çok kutupluluk artıyor.")

col4.metric("Doların Zırh Gücü (DXY)", f"{geo_data['DXY']['last']:.2f}", f"{geo_data['DXY']['change']:.2f}%")
col5.metric("Enerji Silahı (Brent)", f"{geo_data['BRENT']['last']:.2f}$", f"{geo_data['BRENT']['change']:.2f}%")

# --- 3. ANALİTİK BÜLTEN ---
st.info(f"🛡️ **Konsey Analizi:** Altın volatilitesindeki artış ({geo_data['GOLD']['volatility']:.2f}), merkez bankalarının kağıt varlıklardan kaçışını simgeler. "
        "DXY'nin 105 üzerindeki her hareketi, küresel ticaret üzerinde 'Finansal Borç Sıkışması' yaratarak jeopolitik tansiyonu besler.")
