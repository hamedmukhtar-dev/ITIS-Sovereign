import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import graphviz

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(
    page_title="ITIS Sovereign Command",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. تصميم عالي التباين (وضوح تام)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* خلفية سوداء بالكامل */
    .stApp { background-color: #000000; }
    
    /* نصوص بيضاء وذهبية واضحة */
    h1, h2, h3, h4 { color: #FFD700 !important; font-family: sans-serif; }
    p, div, span { color: #E0E0E0; }
    
    /* كروت العدادات */
    div[data-testid="metric-container"] {
        background-color: #111111;
        border: 1px solid #FFD700;
        padding: 10px;
        border-radius: 8px;
    }
    div[data-testid="stMetricValue"] { color: #FFD700 !important; }
    div[data-testid="stMetricLabel"] { color: #FFFFFF !important; }
    
    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab"] { color: white; border: 1px solid #333; }
    .stTabs [aria-selected="true"] { background-color: #FFD700; color: black !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. الهيدر والشريط الجانبي
# ---------------------------------------------------------
with st.sidebar:
    st.title("🦅 ITIS CONTROL")
    st.success("✅ SYSTEM ONLINE")
    st.info("🏦 QNB VAULT CONNECTED")
    st.warning("🛡️ AMEX GBT SECURE")

st.title("🦅 ITIS: THE AFRICA PROTOCOL")
st.markdown("#### 🛰️ The First Sovereign Space-Economy (Starlink + Gold)")
st.divider()

# ---------------------------------------------------------
# 4. العدادات الحية (واضحة جداً)
# ---------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("🥇 Gold Reserve (QNB)", "1,452 kg", "+2%")
c2.metric("💎 AI-GD Price", "$ 68.82", "Pegged")
c3.metric("✈️ IATA Debt Cleared", "$ 12.4M", "Liquidated")
c4.metric("🛰️ Active Nodes", "10,420", "Online")

st.divider()

# ---------------------------------------------------------
# 5. التبويبات الرئيسية
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🌍 3D GLOBAL OPS", "🏗️ BLUEPRINT", "💰 FINANCE"])

# === TAB 1: الكرة الأرضية ثلاثية الأبعاد (بدون مفاتيح) ===
with tab1:
    st.subheader("🛰️ Live Orbital Connectivity")
    
    # رسم الكرة الأرضية باستخدام Plotly (مضمونة الظهور)
    fig_globe = go.Figure()

    # إضافة الخطوط (المسارات)
    fig_globe.add_trace(go.Scattergeo(
        lon = [32.55, 51.51, 32.55, -74.00, 32.55, 55.27],
        lat = [15.50, 25.28, 15.50, 40.71, 15.50, 25.20],
        mode = 'lines',
        line = dict(width = 2, color = '#FFD700'),
        name = 'Starlink Uplink'
    ))

    # إضافة النقاط (المدن)
    fig_globe.add_trace(go.Scattergeo(
        lon = [32.55, 51.51, -74.00, 55.27],
        lat = [15.50, 25.28, 40.71, 25.20],
        text = ['Khartoum (HQ)', 'Doha (Vault)', 'New York (Amex)', 'Dubai (Hub)'],
        mode = 'markers+text',
        marker = dict(size = 10, color = '#00FFFF', line=dict(width=1, color='white')),
        textposition="top center",
        name = 'Nodes'
    ))

    # إعدادات شكل الكرة الأرضية
    fig_globe.update_layout(
        title = 'Live Settlement Layer (Starlink Network)',
        showlegend = False,
        geo = dict(
            projection_type = "orthographic", # شكل كرة ثلاثية الأبعاد
            showland = True,
            landcolor = "#1E1E1E",
            showocean = True,
            oceancolor = "#000000",
            showcountries = True,
            countrycolor = "#333333",
            bgcolor = "black"
        ),
        height=600,
        margin={"r":0,"t":30,"l":0,"b":0},
        paper_bgcolor="black",
        font=dict(color="white")
    )
    
    st.plotly_chart(fig_globe, use_container_width=True)

# === TAB 2: المخطط الهندسي ===
with tab2:
    st.subheader("🏗️ System Architecture")
    
    sys = graphviz.Digraph()
    sys.attr(rankdir='LR', bgcolor='#111111')
    sys.attr('node', shape='box', style='filled', fillcolor='#222222', fontcolor='white', color='#FFD700')
    sys.attr('edge', color='white')

    sys.node('A', 'Starlink 🛰️')
    sys.node('B', 'ITIS AI Core 🦅')
    sys.node('C', 'QNB Vault 🏦')
    sys.node('D', 'Airlines ✈️')

    sys.edge('A', 'B', ' Data')
    sys.edge('B', 'C', ' Gold Lock')
    sys.edge('C', 'D', ' Payment')

    st.graphviz_chart(sys)

# === TAB 3: المحرك المالي ===
with tab3:
    st.subheader("💰 Liquidity Engine")
    # رسم بياني بسيط
    chart_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'Gold Assets': [10, 30, 60, 90, 120]
    })
    st.bar_chart(chart_data.set_index('Month'))

st.divider()
st.caption("CONFIDENTIAL | PROPERTY OF DAR AL KHARTOUM 2025")
