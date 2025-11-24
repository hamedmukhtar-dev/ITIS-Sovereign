import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import graphviz
import time
import random
import string
from datetime import datetime

# ---------------------------------------------------------
# 1. إعدادات النظام
# ---------------------------------------------------------
st.set_page_config(
    page_title="ITIS | Sovereign System",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. التصميم (Black & Gold Luxury)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* الخلفية */
    .stApp { background-color: #000000; }
    
    /* النصوص */
    h1, h2, h3 { color: #D4AF37 !important; font-family: sans-serif; }
    p, li, span, label { color: #E0E0E0; font-size: 14px; }
    
    /* كروت العدادات */
    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, #111 0%, #1a1a1a 100%);
        border: 1px solid #D4AF37;
        border-left: 5px solid #D4AF37;
        padding: 15px; border-radius: 8px;
    }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; }
    div[data-testid="stMetricLabel"] { color: #FFF !important; font-weight: bold; }
    
    /* تصميم بطاقة الرحلة */
    .flight-card {
        background-color: #1a1a1a;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .airline-tag { background-color: #333; color: #fff; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; color: #888; border: 1px solid #333; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; font-weight: bold; }
    
    .stButton>button { border: 1px solid #D4AF37; color: #D4AF37; background-color: black; width: 100%; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. القائمة الجانبية
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9326/9326394.png", width=100)
    st.title("🦅 ITIS CORE")
    st.caption("Global Sovereign Economy")
    st.markdown("---")
    st.success("📡 **UPLINK:** STARLINK V2")
    st.warning("🏦 **VAULT:** QNB DOHA")
    st.info("🛡️ **GUARD:** AMEX GBT")
    st.markdown("---")
    st.write("Commander: **Hamed Mukhtar**")
    st.write("Build: **v8.1 (Stable)**")

# ---------------------------------------------------------
# 4. الرأس
# ---------------------------------------------------------
c1, c2 = st.columns([1, 5])
with c2:
    st.title("ITIS: THE GLOBAL SOVEREIGN PROTOCOL")
    st.markdown("**INFRASTRUCTURE:** `SPACE-NATIVE` | **ASSET:** `GOLD (RWA)` | **APP:** `GOLITE NDC`")
st.divider()

# ---------------------------------------------------------
# 5. الأقسام الرئيسية
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📜 VISION", 
    "🚀 LIVE OPS", 
    "🏗️ BLUEPRINT", 
    "💎 TOKENOMICS", 
    "🤝 ALLIANCE",
    "🛫 GOLITE BOOKING"
])

# === TAB 1: VISION ===
with tab1:
    st.header("1. Strategic Vision")
    st.markdown("""
    **ITIS** replaces broken ground banking with **Space-Based Defi**, utilizing **Starlink** and **Gold-Backed Tokens** to clear airline debts and empower the 'Cloud Nation'.
    """)
    try:
        scope = graphviz.Digraph()
        scope.attr(rankdir='TB', bgcolor='black')
        scope.attr('node', shape='rect', style='filled', fillcolor='#222', fontcolor='white', color='#D4AF37')
        scope.edge('DIASPORA', 'ITIS CORE'); scope.edge('AMEX CORP', 'ITIS CORE'); scope.edge('TRAVELERS', 'ITIS CORE')
        st.graphviz_chart(scope)
    exceptException:
        st.error("Diagram Error: Please check packages.txt")

# === TAB 2: LIVE OPS ===
with tab2:
    st.header("2. Command Center")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🥇 Gold Reserve", "1,452.5 kg", "+2.1%")
    m2.metric("💎 AI-GD Price", "$ 68.82", "Pegged")
    m3.metric("✈️ Debt Cleared", "$ 12.4M", "Paid")
    m4.metric("📡 Active Nodes", "10,420", "Online")
    
    fig = go.Figure(go.Scattergeo(
        lon=[32.55, 51.51, -74.00], lat=[15.50, 25.28, 40.71],
        mode='lines+markers', line=dict(width=2, color='#D4AF37')
    ))
    fig.update_layout(geo=dict(showland=True, landcolor="#111", bgcolor="black"), height=400, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="black")
    st.plotly_chart(fig, use_container_width=True)

# === TAB 3: BLUEPRINT ===
with tab3:
    st.header("3. Engineering Diagram")
    try:
        eng = graphviz.Digraph()
        eng.attr(rankdir='TB', bgcolor='#0E0E0E')
        eng.attr('node', shape='rect', style='filled', fillcolor='#1a1a1a', fontcolor='white', color='gold')
        eng.node('Space', '🛰️ STARLINK LAYER', fillcolor='#333')
        eng.node('Core', '🧠 ITIS CORE (AI)', fillcolor='#D4AF37', fontcolor='black')
        eng.node('Bank', '🏦 QNB / AMEX', fillcolor='green')
        eng.edge('User', 'Space'); eng.edge('Space', 'Core'); eng.edge('Core', 'Bank')
        st.graphviz_chart(eng)
    except:
        st.warning("Diagram requires Graphviz installed.")

# === TAB 4: TOKENOMICS ===
with tab4:
    st.header("4. AI-GD Cycle")
    try:
        token = graphviz.Digraph()
        token.attr(rankdir='LR', bgcolor='black')
        token.attr('node', shape='circle', style='filled', color='gold', fontcolor='black')
        token.edge('DEBT', 'GOLD'); token.edge('GOLD', 'TOKEN'); token.edge('TOKEN', 'PAY')
        st.graphviz_chart(token)
    except:
        st.write("Debt -> Gold -> Token -> Pay")

# === TAB 5: ALLIANCE ===
with tab5:
    st.header("5. Strategic Partners")
    c1, c2, c3 = st.columns(3)
    c1.success("🛰️ **STARLINK:** Backbone"); c2.warning("🏦 **QNB:** Treasury"); c3.info("🛡️ **AMEX:** Compliance")

# === TAB 6: GOLITE BOOKING (Integrated) ===
with tab6:
    st.header("🛫 GoLite NDC Gateway (Live Booking)")
    
    # Initialize Session State
    if "cart" not in st.session_state: st.session_state.cart = []
    
    c_search, c_cart = st.columns([3, 1])
    
    with c_search:
        with st.form("search"):
            c1, c2, c3 = st.columns(3)
            c1.text_input("From", "KRT"); c2.text_input("To", "CAI"); c3.date_input("Date")
            if st.form_submit_button("🔍 Search Flights"):
                st.session_state.search_done = True

        if st.session_state.get("search_done"):
            st.markdown("### Available Flights")
            # Flight 1
            with st.container():
                st.markdown("""
                <div class="flight-card">
                    <span class="airline-tag">SudanAir</span> <b>FL001</b> | 06:30 - 08:45 | <span style="color:#0f0">$120</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Add SudanAir", key="f1"):
                    st.session_state.cart.append({"id": "FL001", "price": 120})
                    st.toast("Added to Cart!")
            
            # Flight 2
            with st.container():
                st.markdown("""
                <div class="flight-card">
                    <span class="airline-tag">Tarco</span> <b>TR550</b> | 09:00 - 11:30 | <span style="color:#0f0">$135</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Add Tarco", key="f2"):
                    st.session_state.cart.append({"id": "TR550", "price": 135})
                    st.toast("Added to Cart!")

    with c_cart:
        st.markdown("### 🛒 Cart")
        if st.session_state.cart:
            total = sum(item['price'] for item in st.session_state.cart)
            for item in st.session_state.cart:
                st.write(f"✈️ {item['id']} (${item['price']})")
            st.markdown(f"**Total: ${total}**")
            
            if st.button("💳 Pay with AI-GD"):
                with st.spinner("Connecting Starlink..."):
                    time.sleep(2)
                st.balloons()
                pnr = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                st.success(f"PNR: {pnr}")
                st.session_state.cart = []
        else:
            st.info("Empty")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.divider()
st.caption("CONFIDENTIAL | PROPERTY OF DAR AL KHARTOUM | EST. 1995")
