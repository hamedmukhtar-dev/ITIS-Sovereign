import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pydeck as pdk
import graphviz

# ---------------------------------------------------------
# 1. إعدادات الصفحة (وضع ملء الشاشة)
# ---------------------------------------------------------
st.set_page_config(
    page_title="ITIS | Sovereign Command",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 2. تصميم "السايبربنك المالي" (Cyber-Finance Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* الخلفية العامة */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(#111 1px, transparent 1px);
        background-size: 20px 20px;
        color: #e0e0e0;
    }
    
    /* العناوين */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    h1 { 
        background: -webkit-linear-gradient(#FFD700, #BF953F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* البطاقات الزجاجية (Glassmorphism) */
    div[data-testid="metric-container"] {
        background: rgba(25, 25, 25, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: #FFD700;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
    }
    
    /* النصوص الملونة */
    .gold-text { color: #FFD700; font-weight: bold; }
    .neon-text { color: #00FFFF; font-weight: bold; text-shadow: 0 0 5px #00FFFF; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. الهيدر (The Header)
# ---------------------------------------------------------
c1, c2 = st.columns([1, 6])
with c1:
    st.markdown("## 🦅")
with c2:
    st.title("ITIS: THE AFRICA PROTOCOL")
    st.markdown("""
    <div style='display: flex; gap: 20px; font-family: monospace;'>
        <span class='gold-text'>● STATUS: OPERATIONAL</span>
        <span class='neon-text'>● NETWORK: STARLINK LEO V2</span>
        <span class='gold-text'>● TREASURY: QNB SECURED</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# 4. العدادات الحية (Live Metrics)
# ---------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("🥇 Gold Assets (Vault)", "1,452.50 kg", "+2.1% Today")
m2.metric("💎 AI-GD Token Price", "$ 68.82", "Pegged 1:1 Gold")
m3.metric("🛰️ Active Nodes (Starlink)", "10,420", "Online")
m4.metric("✈️ Cleared Debt (IATA)", "$ 12.4M", "Liquidated")

# ---------------------------------------------------------
# 5. الكرة الأرضية التفاعلية (3D Space Map)
# ---------------------------------------------------------
st.markdown("### 🛰️ LIVE ORBITAL CONNECTIVITY (اتصال الفضاء)")

# بيانات المحاكاة (الخرطوم، الدوحة، نيويورك، لندن)
layers = [
    pdk.Layer(
        "ArcLayer",
        data=[
            {"source": [32.5599, 15.5007], "target": [51.5194, 25.2854], "color": [255, 215, 0]}, # خرطوم -> الدوحة (الذهب)
            {"source": [32.5599, 15.5007], "target": [-74.0060, 40.7128], "color": [0, 255, 255]}, # خرطوم -> نيويورك (Amex)
            {"source": [32.5599, 15.5007], "target": [-0.1278, 51.5074], "color": [255, 0, 255]}, # خرطوم -> لندن (IATA)
        ],
        get_source_position="source",
        get_target_position="target",
        get_source_color=[0, 255, 255, 160],
        get_target_color="color",
        get_width=4,
        get_height=0.5,
    ),
    pdk.Layer(
        "ScatterplotLayer",
        data=[
            {"pos": [32.5599, 15.5007], "name": "Khartoum (HQ)"},
            {"pos": [51.5194, 25.2854], "name": "Doha (Vault)"},
            {"pos": [-74.0060, 40.7128], "name": "New York (Amex)"},
        ],
        get_position="pos",
        get_color=[255, 215, 0],
        get_radius=100000,
    ),
]

view_state = pdk.ViewState(latitude=20, longitude=30, zoom=1.5, pitch=45)

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=view_state,
    layers=layers,
    tooltip={"text": "{name}"}
))

# ---------------------------------------------------------
# 6. المخططات التفصيلية (Tabs)
# ---------------------------------------------------------
tab_arch, tab_finance, tab_partners = st.tabs(["🏗️ System Architecture", "💰 Financial Engine", "🤝 Alliance"])

with tab_arch:
    st.subheader("The Sovereign Blueprint (مخطط النظام)")
    
    # مخطط Graphviz
    sys = graphviz.Digraph()
    sys.attr(rankdir='LR', bgcolor='transparent')
    sys.attr('node', shape='rect', style='rounded,filled', fillcolor='#1a1a1a', fontcolor='white', penwidth='2', color='#FFD700')
    sys.attr('edge', color='#00FFFF', penwidth='1.5', arrowsize='0.8')

    # العقد
    sys.node('U', 'User / Agent\n(Starlink Terminal)', color='#00FFFF')
    sys.node('S', 'Orbit Satellites\n(SpaceX LEO)', shape='ellipse', color='#00FFFF')
    sys.node('C', 'ITIS CORE\n(xAI Brain)', fillcolor='#333')
    sys.node('V', 'QNB VAULT\n(Physical Gold)', color='#FFD700')
    sys.node('M', 'Minting Engine\n(AI-GD Token)', color='#FFD700')
    sys.node('G', 'Global Payment\n(Amex/IATA)')

    # المسار
    sys.edge('U', 'S', ' Encrypted Signal')
    sys.edge('S', 'C', ' Data Stream')
    sys.edge('C', 'V', ' Audit Gold')
    sys.edge('V', 'M', ' Issue Token')
    sys.edge('M', 'G', ' Settlement')
    sys.edge('G', 'U', ' Ticket Confirmed')

    st.graphviz_chart(sys)

with tab_finance:
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        st.markdown("##### 💹 Liquidity Recovery Model")
        # مخطط مساحي
        chart_data = pd.DataFrame({
            'Month': pd.date_range(start='1/1/2025', periods=12),
            'Debt Recovered': np.cumsum(np.random.randn(12) + 10),
            'Gold Reserve': np.cumsum(np.random.randn(12) + 12)
        })
        st.area_chart(chart_data.set_index('Month'))
        
    with c_f2:
        st.markdown("##### 🧠 AI Fraud Detection Rate")
        # عداد دائري
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 99.9,
            title = {'text': "Safety Score %"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00FFFF"}}
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", height=300)
        st.plotly_chart(fig, use_container_width=True)

with tab_partners:
    st.success("✅ **Strategic Partners Active & Integrated**")
    cols = st.columns(3)
    cols[0].info("🛰️ **STARLINK:** 100% Uptime")
    cols[1].warning("🏦 **QNB GROUP:** Custody Active")
    cols[2].error("🛡️ **AMEX GBT:** Compliance On")

# ---------------------------------------------------------
# التذييل
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>CONFIDENTIAL SYSTEM | PROPERTY OF DAR AL KHARTOUM | EST. 1995</small><br>
    <small>POWERED BY xAI & STARLINK INFRASTRUCTURE</small>
</div>
""", unsafe_allow_html=True)
