# ============================================================
# ITIS — SOVEREIGN FINANCIAL SYSTEM (V8 ULTIMATE BUILD)
# Full Professional Version — Black × Gold Edition
# Integrated: GoLite Agency Dashboard + PNR + Webhook Sim
# ============================================================

import os
import json
import time
import uuid
import random
import string
import streamlit as st
import graphviz
from datetime import datetime

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(
    page_title="ITIS | Sovereign System",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Theme / Styling
# ----------------------------
st.markdown("""
<style>
    /* General Dark Theme */
    .stApp { background-color: #000000; color: #EDEDED; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; font-family: 'Segoe UI', sans-serif; }
    p, li, span, div, label { color: #E0E0E0 !important; font-size: 14px; }
    
    /* Buttons */
    .stButton>button { background-color: #0b0b0b; border: 1px solid #D4AF37; color: #D4AF37; width: 100%; border-radius: 5px; }
    .stButton>button:hover { background-color: #D4AF37; color: black; }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, #111 0%, #1a1a1a 100%);
        border: 1px solid #D4AF37;
        border-left: 5px solid #D4AF37;
        padding: 15px; border-radius: 8px;
    }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { background-color: #1b1b1b; color: #888; border: 1px solid #333; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; font-weight: bold; }
    
    /* GoLite Card Style */
    .flight-card { background-color: #0f1724; border: 1px solid #1f2937; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .airline-tag { background-color: #333; color: #fff; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------
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
    st.write("Build: **v8.0 (Ultimate)**")

# ----------------------------
# Header
# ----------------------------
c1, c2 = st.columns([1, 5])
with c2:
    st.title("ITIS: THE GLOBAL SOVEREIGN PROTOCOL")
    st.markdown("**INFRASTRUCTURE:** `SPACE-NATIVE` | **ASSET:** `GOLD (RWA)` | **APP:** `GOLITE NDC`")
st.divider()

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs([
    "📜 VISION", 
    "🚀 LIVE OPS", 
    "🏗️ BLUEPRINT", 
    "💎 TOKENOMICS", 
    "🤝 ALLIANCE",
    "🛫 GOLITE DASHBOARD"
])

# =========================================================
# TAB 1: VISION
# =========================================================
with tabs[0]:
    st.header("1. Strategic Vision")
    st.markdown("""
    **ITIS** replaces broken ground banking with **Space-Based Defi**, utilizing **Starlink** and **Gold-Backed Tokens** to clear airline debts and empower the 'Cloud Nation'.
    """)
    scope = graphviz.Digraph()
    scope.attr(rankdir='TB', bgcolor='black')
    scope.attr('node', shape='rect', style='filled', fillcolor='#222', fontcolor='white', color='#D4AF37')
    scope.edge('DIASPORA', 'ITIS CORE'); scope.edge('AMEX CORP', 'ITIS CORE'); scope.edge('TRAVELERS', 'ITIS CORE')
    st.graphviz_chart(scope)

# =========================================================
# TAB 2: LIVE OPS
# =========================================================
with tabs[1]:
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

# =========================================================
# TAB 3: BLUEPRINT
# =========================================================
with tabs[2]:
    st.header("3. Engineering Diagram")
    eng = graphviz.Digraph()
    eng.attr(rankdir='TB', bgcolor='#0E0E0E')
    eng.attr('node', shape='rect', style='filled', fillcolor='#1a1a1a', fontcolor='white', color='gold')
    eng.node('Space', '🛰️ STARLINK LAYER', fillcolor='#333')
    eng.node('Core', '🧠 ITIS CORE (AI)', fillcolor='#D4AF37', fontcolor='black')
    eng.node('Bank', '🏦 QNB / AMEX', fillcolor='green')
    eng.edge('User', 'Space'); eng.edge('Space', 'Core'); eng.edge('Core', 'Bank')
    st.graphviz_chart(eng)

# =========================================================
# TAB 4: TOKENOMICS
# =========================================================
with tabs[3]:
    st.header("4. AI-GD Cycle")
    st.info("Debt -> Gold -> Token -> Settlement")
    token = graphviz.Digraph()
    token.attr(rankdir='LR', bgcolor='black')
    token.attr('node', shape='circle', style='filled', color='gold', fontcolor='black')
    token.edge('DEBT', 'GOLD'); token.edge('GOLD', 'TOKEN'); token.edge('TOKEN', 'PAY')
    st.graphviz_chart(token)

# =========================================================
# TAB 5: ALLIANCE
# =========================================================
with tabs[4]:
    st.header("5. Strategic Partners")
    c1, c2, c3 = st.columns(3)
    c1.success("🛰️ **STARLINK:** Backbone"); c2.warning("🏦 **QNB:** Treasury"); c3.info("🛡️ **AMEX:** Compliance")

# =========================================================
# TAB 6: GOLITE DASHBOARD (Integrated V2)
# =========================================================
with tabs[5]:
    st.header("🛫 GoLite NDC Dashboard (Live Demo)")
    
    # Session State Init
    if "gl_cart" not in st.session_state: st.session_state.gl_cart = []
    if "gl_bookings" not in st.session_state: st.session_state.gl_bookings = []
    if "gl_passengers" not in st.session_state: st.session_state.gl_passengers = []

    col_main, col_side = st.columns([3, 1])

    with col_main:
        # 1. Search
        with st.expander("🔍 Search Flights", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            with c1: from_loc = st.text_input("From", "Khartoum (KRT)")
            with c2: to_loc = st.text_input("To", "Cairo (CAI)")
            with c3: date_f = st.date_input("Date")
            with c4: pax = st.number_input("Pax", 1, 9, 1)
            
        # 2. Results (Mock)
        st.markdown("### Available Flights")
        
        flights = [
            {"id": "SD102", "air": "SudanAir", "time": "09:00 - 11:30", "price": 120},
            {"id": "TR550", "air": "Tarco Air", "time": "14:00 - 16:30", "price": 135},
            {"id": "BN303", "air": "Badr Air", "time": "18:00 - 20:30", "price": 140}
        ]
        
        for f in flights:
            with st.container():
                st.markdown(f"""
                <div class="flight-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span class="airline-tag">{f['air']}</span> 
                            <span style="margin-left:10px; color:#ccc;">{f['time']}</span>
                        </div>
                        <div style="color:#00FF00; font-weight:bold;">${f['price']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {f['id']}", key=f['id']):
                    st.session_state.gl_cart.append(f)
                    st.toast(f"Added {f['air']} to Cart")

        # 3. Passenger Details
        st.markdown("### 👤 Passenger Manifest")
        with st.form("pax_form"):
            p_name = st.text_input("Full Name")
            p_pass = st.text_input("Passport Number")
            if st.form_submit_button("Save Passenger"):
                st.session_state.gl_passengers.append({"name": p_name, "pass": p_pass})
                st.success("Passenger Saved")

    with col_side:
        # Cart & Checkout
        st.markdown("### 🛒 Cart")
        if not st.session_state.gl_cart:
            st.info("Cart is empty")
        else:
            total = 0
            for item in st.session_state.gl_cart:
                st.write(f"✈️ {item['air']} (${item['price']})")
                total += item['price']
            
            st.markdown(f"**Total: ${total}**")
            
            if st.button("💳 Pay & Issue PNR"):
                if not st.session_state.gl_passengers:
                    st.error("Add passenger info first!")
                else:
                    with st.spinner("Connecting to Starlink..."):
                        time.sleep(1.5)
                    pnr = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    st.balloons()
                    st.success(f"Ticket Issued! PNR: {pnr}")
                    # Add to bookings
                    st.session_state.gl_bookings.append({"pnr": pnr, "total": total, "status": "CONFIRMED"})
                    st.session_state.gl_cart = [] # Clear cart

        # My Bookings
        if st.session_state.gl_bookings:
            st.markdown("---")
            st.markdown("### 🎟️ My Bookings")
            for b in st.session_state.gl_bookings:
                st.code(f"PNR: {b['pnr']} | ${b['total']}")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.divider()
st.caption("CONFIDENTIAL | PROPERTY OF DAR AL KHARTOUM | EST. 1995")
