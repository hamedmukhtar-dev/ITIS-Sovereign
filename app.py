import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="ITIS | Sovereign Command",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. التصميم
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    div[data-testid="stMetricValue"] { color: #FFD700; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9326/9326394.png", width=80)
    st.title("🦅 ITIS CONTROL")
    st.caption("Sovereign Travel Economy")
    st.markdown("---")
    st.success("📡 Network: Starlink LEO")
    st.info("🏦 Treasury: QNB (Qatar)")
    st.warning("🛡️ Security: Amex/OFAC")
    st.markdown("---")
    st.write("Commander: **Hamed Mukhtar**")

# 4. الشاشة الرئيسية
st.title("🌍 ITIS: Integrated Travel Intelligence System")
st.markdown("### The First AI-GD (Gold Backed) Economy")
st.divider()

# العدادات
col1, col2, col3, col4 = st.columns(4)
col1.metric("🥇 Gold Reserve (QNB)", "1,450 kg", "+12 kg")
col2.metric("💎 AI-GD Price", "$ 68.45", "Stable")
col3.metric("✈️ Tickets Issued", "8,240", "+15%")
col4.metric("🛰️ Active Users", "2.3M", "Starlink")

st.divider()

# الرسوم البيانية
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📈 Liquidity Recovery")
    chart_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Recovered ($M)': [10, 30, 50, 70, 90, 115]
    })
    st.line_chart(chart_data.set_index('Month'))

with c2:
    st.subheader("🧠 OpenAI Sentinel")
    st.success("✅ SYSTEM SECURE")
    st.info("ℹ️ Insight: High demand for Port Sudan -> Cairo.")

# التذييل
st.divider()
st.caption("CONFIDENTIAL - PROPERTY OF DAR AL KHARTOUM (2025)")
