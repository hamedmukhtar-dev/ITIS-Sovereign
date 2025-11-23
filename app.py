import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import graphviz

# ---------------------------------------------------------
# 1. إعدادات النظام (System Config)
# ---------------------------------------------------------
st.set_page_config(
    page_title="ITIS | Sovereign Economy",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. تصميم "الهيبة التكنولوجية" (Dark Space & Gold Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* خلفية سوداء */
    .stApp { background-color: #000000; color: white; }
    
    /* نصوص ذهبية */
    h1, h2, h3 { color: #FFD700 !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* تصميم العدادات */
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border: 1px solid #FFD700;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.2);
    }
    div[data-testid="stMetricValue"] { color: #FFD700 !important; }
    
    /* تصميم التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #1E1E1E; border-radius: 5px; color: white; border: 1px solid #333; }
    .stTabs [aria-selected="true"] { background-color: #FFD700 !important; color: black !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. الشريط الجانبي (Status Bar)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9326/9326394.png", width=100)
    st.title("🦅 ITIS CONTROL")
    st.markdown("---")
    st.success("🛰️ Uplink: **Starlink V2 (Stable)**")
    st.info("🏦 Vault: **QNB Doha (Secure)**")
    st.warning("🛡️ Compliance: **Amex GBT (Active)**")
    st.markdown("---")
    st.write("Commander: **Hamed Mukhtar**")

# ---------------------------------------------------------
# 4. الرأس (Header)
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 5])
with col_title:
    st.title("ITIS: The Africa Protocol")
    st.markdown("#### The World's First Sovereign Economy Run on Space Infrastructure")
    st.markdown("`Status: OPERATIONAL` | `Network: STARLINK-NATIVE` | `Currency: GOLD-BACKED`")

st.divider()

# ---------------------------------------------------------
# 5. الأقسام الرئيسية (The Master Tabs)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Command Center", "🏗️ System Blueprint", "💰 Financial Engine", "🤝 Strategic Alliance"])

# === TAB 1: غرفة القيادة (الأرقام الحية) ===
with tab1:
    st.subheader("Live Sovereign Operations (العمليات الحية)")
    
    # صف العدادات
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🥇 Gold Reserve (QNB)", "1,450 kg", "+12 kg (24h)")
    c2.metric("💎 AI-GD Price", "$ 68.45", "Stable (1g Gold)")
    c3.metric("✈️ IATA Debt Cleared", "$ 4.2M", "+$500k Today")
    c4.metric("🛰️ Active Terminals", "10,240", "Starlink Nodes")

    st.markdown("---")
    
    # خريطة العمليات والذكاء الاصطناعي
    col_map, col_ai = st.columns([2, 1])
    
    with col_map:
        st.markdown("##### 🌍 Real-Time Settlement Map (Ledger)")
        map_data = pd.DataFrame({
            'lat': [15.5007, 25.276987, 24.7136, 30.0444],
            'lon': [32.5599, 55.296249, 46.6753, 31.2357],
            'Volume': [1000, 5000, 3000, 2000]
        })
        st.map(map_data, zoom=3, color='#FFD700')
    
    with col_ai:
        st.markdown("##### 🧠 OpenAI Sentinel (Security)")
        st.success("✅ FRAUD CHECK: PASSED")
        st.info("ℹ️ LIQUIDITY: OPTIMAL")
        st.warning("⚠️ ALERT: High demand detected in Port Sudan. Auto-scaling Starlink bandwidth.")

# === TAB 2: المخطط الهندسي (كيف يعمل النظام) ===
with tab2:
    st.subheader("The Sovereign Architecture (بنية النظام السيادية)")
    st.markdown("كيف نربط الفضاء بالأرض لحل أزمة السيولة:")
    
    # رسم المخطط المعقد باستخدام Graphviz
    arch = graphviz.Digraph()
    arch.attr(rankdir='LR', bgcolor='#0E1117')
    arch.attr('node', shape='box', style='filled', fillcolor='#1E1E1E', fontcolor='white', color='#FFD700')
    arch.attr('edge', color='white')

    arch.node('USER', 'Diaspora User 📱\n(Starlink App)')
    arch.node('SAT', 'Starlink Satellites 🛰️\n(Zero-Infrastructure)')
    arch.node('CORE', 'ITIS AI Core 🦅\n(Logic & Ledger)')
    arch.node('AMEX', 'Amex Gateway 🛡️\n(OFAC/KYC)')
    arch.node('QNB', 'QNB Vault 🏦\n(Gold Assets)')
    arch.node('IATA', 'Airlines/IATA ✈️\n(Settlement)')

    arch.edge('USER', 'SAT', ' Encrypted Request')
    arch.edge('SAT', 'CORE', ' LEO Uplink')
    arch.edge('CORE', 'AMEX', ' Compliance Check')
    arch.edge('AMEX', 'QNB', ' Lock Gold')
    arch.edge('QNB', 'IATA', ' Release AI-GD')
    arch.edge('IATA', 'USER', ' Ticket Issued')

    st.graphviz_chart(arch)

# === TAB 3: المحرك المالي (الأرباح وتدفق الكاش) ===
with tab3:
    st.subheader("Financial Projection & Cash Flow (نموذج الربحية)")
    
    col_fin1, col_fin2 = st.columns(2)
    
    with col_fin1:
        st.markdown("##### 📈 Revenue Growth (Hockey Stick)")
        # بيانات وهمية للنمو
        growth_data = pd.DataFrame({
            "Year": ["2025", "2026", "2027", "2028"],
            "Revenue ($M)": [15, 120, 450, 1200],
            "Gold Assets (Tons)": [1.5, 5, 12, 25]
        })
        fig_growth = px.bar(growth_data, x="Year", y=["Revenue ($M)", "Gold Assets (Tons)"], barmode='group', color_discrete_sequence=['#FFD700', '#00FFFF'])
        fig_growth.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_growth, use_container_width=True)

    with col_fin2:
        st.markdown("##### 🔄 Debt-to-Asset Swap Model")
        st.write("كيف نحول ديون الطيران المعدومة إلى ذهب:")
        # مخطط دائري
        pie_data = pd.DataFrame({
            "Stage": ["Blocked Funds (Debt)", "Gold Mining Sourcing", "AI-GD Issuance", "Airline Settlement"],
            "Value": [100, 30, 80, 100]
        })
        fig_pie = px.pie(pie_data, values='Value', names='Stage', color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)

# === TAB 4: التحالف الاستراتيجي ===
with tab4:
    st.subheader("The Strategic Alliance (شركاء النجاح)")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("### 🛰️ Starlink / X")
        st.caption("Infrastructure Partner")
        st.write("- 100% Space Connectivity")
        st.write("- X-Payments Integration")
        st.success("Target: 10k Terminals")
    
    with col_p2:
        st.markdown("### 🏦 QNB Group")
        st.caption("Treasury & Custody")
        st.write("- Physical Gold Storage")
        st.write("- Fiat Gateway (QAR/USD)")
        st.info("Role: The Bank")
    
    with col_p3:
        st.markdown("### 🛡️ Amex GBT")
        st.caption("Compliance & Network")
        st.write("- OFAC/KYC Shield")
        st.write("- Corporate Travel Flow")
        st.warning("Role: The Gatekeeper")

st.divider()
st.caption("CONFIDENTIAL: PROPERTY OF DAR AL KHARTOUM - EST. 1995")
