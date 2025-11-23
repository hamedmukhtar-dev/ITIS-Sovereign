import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import graphviz

# ---------------------------------------------------------
# 1. إعدادات النظام
# ---------------------------------------------------------
st.set_page_config(
    page_title="ITIS | Global Sovereign System",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. تصميم الهيبة الملكية (Royal Dark & Gold)
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
    p, li, span { color: #E0E0E0; font-size: 16px; }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, #111 0%, #1a1a1a 100%);
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 8px;
    }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; }
    div[data-testid="stMetricLabel"] { color: #FFF !important; font-weight: bold; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border: 1px solid #333; color: white; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; font-weight: bold; border: 1px solid #D4AF37; }
    
    .stButton>button {
        border: 1px solid #D4AF37;
        color: #D4AF37;
        background-color: black;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. القائمة الجانبية
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9326/9326394.png", width=100)
    st.title("🦅 ITIS CONTROL")
    st.caption("Global Sovereign Economy")
    st.markdown("---")
    st.info("📡 **Connectivity:** Starlink Global")
    st.warning("🏦 **Treasury:** QNB Group")
    st.success("🛡️ **Compliance:** Amex GBT / OFAC")
    st.markdown("---")
    st.write("Commander: **Hamed Mukhtar**")
    st.write("Version: **5.1 (Visual Edition)**")

# ---------------------------------------------------------
# 4. الرأس
# ---------------------------------------------------------
c1, c2 = st.columns([1, 5])
with c2:
    st.title("ITIS: THE GLOBAL SOVEREIGN PROTOCOL")
    st.markdown("### 🌍 The First Cloud-Nation Economy Run on Space Infrastructure")
    st.markdown("**Status:** `LIVE GLOBALLY` | **Asset:** `GOLD (RWA)` | **Scope:** `UNLIMITED`")
st.divider()

# ---------------------------------------------------------
# 5. الأقسام الرئيسية
# ---------------------------------------------------------
tab_vision, tab_ops, tab_arch, tab_token, tab_partners = st.tabs([
    "📜 GLOBAL VISION", 
    "🚀 LIVE OPERATIONS", 
    "🏗️ SYSTEM ARCHITECTURE", 
    "💎 AI-GD MODEL", 
    "🤝 STRATEGIC ALLIANCE"
])

# === TAB 1: الرؤية العالمية (مع الرسم الجديد!) ===
with tab_vision:
    st.header("1. Strategic Vision: The Cloud Nation Ecosystem")
    
    col_v1, col_v2 = st.columns([1, 1])
    
    with col_v1:
        st.markdown("""
        ### **Who We Are:**
        **ITIS** is the **Alternative Digital Central Bank** for the global travel industry. We bridge the gap where legacy infrastructure ends and the sovereign digital future begins.

        ### **The Scope (Target Audience):**
        We utilize Starlink to serve the **'Cloud Nation'**:
        1.  🌍 **The Diaspora:** 10M+ Sudanese & Global Citizens.
        2.  🏢 **Corporate Giants (Amex GBT):** MNCS, UN, NGOs requiring OFAC compliance.
        3.  ✈️ **Global Travelers:** Seamless settlement for airline customers worldwide.
        """)
        
        st.info("ℹ️ **Mission:** Re-engineering the global economy by converting distressed assets into Gold Standards.")

    with col_v2:
        st.markdown("### 🌐 The Ecosystem Map (نطاق العمل)")
        
        # --- الرسم الجديد: يوضح نطاق الأمة السحابية ---
        scope = graphviz.Digraph()
        scope.attr(rankdir='TB', bgcolor='black')
        scope.attr('node', shape='rect', style='rounded,filled', fillcolor='#222', fontcolor='white', color='#D4AF37')
        scope.attr('edge', color='white')

        # القلب
        scope.node('CORE', '🦅 ITIS PROTOCOL\n(The Sovereign Hub)', fontsize='14', fillcolor='#D4AF37', fontcolor='black')

        # الأطراف الثلاثة
        scope.node('DIASPORA', '🌍 DIASPORA (B2C)\n(10M Users)', color='#00FFFF', fontcolor='#00FFFF')
        scope.node('CORP', '🏢 AMEX GBT (B2B)\n(UN / NGOs / MNCs)', color='#00FF00', fontcolor='#00FF00')
        scope.node('PAX', '✈️ GLOBAL TRAVELERS\n(Airlines)', color='#FF00FF', fontcolor='#FF00FF')

        # الاتصال
        scope.edge('DIASPORA', 'CORE', ' Remittance & Booking')
        scope.edge('CORP', 'CORE', ' Corporate Travel')
        scope.edge('PAX', 'CORE', ' Global Settlement')
        
        st.graphviz_chart(scope)

# === TAB 2: غرفة القيادة (Live Ops) ===
with tab_ops:
    st.header("2. Sovereign Command Center")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🥇 Gold Reserve (QNB)", "1,452.5 kg", "+2.1%")
    m2.metric("💎 AI-GD Token", "$ 68.82", "Pegged 1g Gold")
    m3.metric("✈️ IATA Debt Cleared", "$ 12.4M", "Liquidated")
    m4.metric("📡 Active Nodes", "10,420", "Global Online")

    st.markdown("---")
    st.subheader("🌍 Global Settlement Layer (Starlink Network)")
    
    fig_globe = go.Figure(go.Scattergeo(
        lon = [32.55, 51.51, -74.00, -0.12, 55.27, 139.69],
        lat = [15.50, 25.28, 40.71, 51.50, 25.20, 35.67],
        text = ['KHARTOUM', 'DOHA', 'NEW YORK', 'LONDON', 'DUBAI', 'TOKYO'],
        mode = 'markers+lines',
        line = dict(width=2, color='#D4AF37'),
        marker = dict(size=10, color='#00FFFF')
    ))
    fig_globe.update_layout(
        geo = dict(
            showland=True, landcolor="#111", showocean=True, oceancolor="#000",
            projection_type="orthographic", bgcolor="black"
        ),
        height=500, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="black", font_color="white"
    )
    st.plotly_chart(fig_globe, use_container_width=True)

# === TAB 3: المخطط الهندسي (Architecture) ===
with tab_arch:
    st.header("3. System Architecture (The Global Bridge)")
    
    sys = graphviz.Digraph()
    sys.attr(rankdir='LR', bgcolor='black')
    sys.attr('node', shape='rect', style='filled', fillcolor='#222', fontcolor='white', color='#D4AF37')
    sys.attr('edge', color='white')

    sys.node('USER', '📱 Global User\n(Cloud Nation)')
    sys.node('SAT', '🛰️ Starlink LEO\n(Space Layer)')
    sys.node('CORE', '🦅 ITIS AI Core\n(Logic & Ledger)')
    sys.node('AMEX', '🛡️ Amex Gateway\n(Global Compliance)')
    sys.node('QNB', '🏦 QNB Vault\n(Gold Assets)')
    sys.node('IATA', '✈️ Airlines\n(Worldwide)')

    sys.edge('USER', 'SAT', ' Request')
    sys.edge('SAT', 'CORE', ' Data')
    sys.edge('CORE', 'AMEX', ' KYC/OFAC')
    sys.edge('AMEX', 'QNB', ' Gold Lock')
    sys.edge('QNB', 'IATA', ' Pay AI-GD')
    sys.edge('IATA', 'USER', ' Ticket')

    st.graphviz_chart(sys)

# === TAB 4: نموذج العملة (AI-GD) ===
with tab_token:
    st.header("4. AI-GD: The Gold Standard 2.0")
    c_t1, c_t2 = st.columns([2, 1])
    
    with c_t1:
        money = graphviz.Digraph()
        money.attr(rankdir='TB', bgcolor='black')
        money.attr('node', shape='ellipse', style='filled', fillcolor='#111', fontcolor='#00FFFF', color='#00FFFF')
        money.attr('edge', color='white')

        money.node('DEBT', '❌ Distressed Assets', color='red')
        money.node('GOLD', '🥇 Physical Gold (QNB)', color='gold')
        money.node('TOKEN', '💎 AI-GD Digital Token', color='gold')
        money.node('PAY', '✅ Global Settlement', color='green')

        money.edge('DEBT', 'GOLD', ' Swap')
        money.edge('GOLD', 'TOKEN', ' Minting')
        money.edge('TOKEN', 'PAY', ' Payment')

        st.graphviz_chart(money)
    
    with c_t2:
        st.info("ℹ️ **Tokenomics:**")
        st.write("A stable digital currency backed 100% by allocated physical gold, used for instant cross-border settlement without SWIFT delays.")

# === TAB 5: التحالف الاستراتيجي (Alliance) ===
with tab_partners:
    st.header("5. The Strategic Alliance")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🛰️ STARLINK")
        st.write("**Infrastructure Backbone**")
        st.caption("Connecting the Cloud Nation.")
    with c2:
        st.markdown("### 🏦 QNB GROUP")
        st.write("**Sovereign Treasury**")
        st.caption("Gold Custodian & Fiat Gateway.")
    with c3:
        st.markdown("### 🛡️ AMEX GBT")
        st.write("**Compliance Shield**")
        st.caption("Global Corporate Access.")

# ---------------------------------------------------------
# التذييل
# ---------------------------------------------------------
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    CONFIDENTIAL SYSTEM | PROPERTY OF DAR AL KHARTOUM | EST. 1995<br>
    POWERED BY xAI & STARLINK INFRASTRUCTURE
</div>
""", unsafe_allow_html=True)
