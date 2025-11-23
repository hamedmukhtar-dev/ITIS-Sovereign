import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import graphviz

# ---------------------------------------------------------
# 1. إعدادات النظام (System Config)
# ---------------------------------------------------------
st.set_page_config(
    page_title="ITIS | Sovereign Economy",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. تصميم "الهيبة الملكية" (Royal Dark & Gold Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* الخلفية */
    .stApp { background-color: #000000; }
    
    /* النصوص */
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Helvetica Neue', sans-serif; }
    p, li, span { color: #E0E0E0; font-size: 16px; }
    
    /* الصناديق والعدادات */
    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, #111 0%, #1a1a1a 100%);
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 8px;
    }
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.3); }
    div[data-testid="stMetricLabel"] { color: #FFF !important; font-weight: bold; }
    
    /* التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border: 1px solid #333; color: white; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; font-weight: bold; border: 1px solid #D4AF37; }
    
    /* الأزرار */
    .stButton>button {
        border: 1px solid #D4AF37;
        color: #D4AF37;
        background-color: black;
        border-radius: 5px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. القائمة الجانبية (الهوية)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9326/9326394.png", width=100)
    st.title("🦅 ITIS CONTROL")
    st.caption("The Sovereign Travel Economy")
    st.markdown("---")
    st.info("📡 **Connectivity:** Starlink (SpaceX)")
    st.warning("🏦 **Treasury:** QNB Group (Qatar)")
    st.success("🛡️ **Compliance:** Amex GBT / OFAC")
    st.markdown("---")
    st.write("Commander: **Hamed Mukhtar**")
    st.write("Version: **3.0 (Master Class)**")

# ---------------------------------------------------------
# 4. الرأس (The Header)
# ---------------------------------------------------------
c1, c2 = st.columns([1, 5])
with c2:
    st.title("ITIS: THE AFRICA PROTOCOL")
    st.markdown("### 🌍 First Sovereign Economy Run on Space Infrastructure")
    st.markdown("**Status:** `LIVE PROTOTYPE` | **Ledger:** `IMMUTABLE` | **Asset:** `GOLD (RWA)`")
st.divider()

# ---------------------------------------------------------
# 5. الأقسام الرئيسية (5 Tabs كاملة)
# ---------------------------------------------------------
tab_vision, tab_ops, tab_arch, tab_token, tab_partners = st.tabs([
    "📜 VISION & STRATEGY", 
    "🚀 LIVE OPERATIONS", 
    "🏗️ SYSTEM ARCHITECTURE", 
    "💎 AI-GD MODEL", 
    "🤝 STRATEGIC ALLIANCE"
])

# =========================================================
# TAB 1: الرؤية والنبذة (Vision) - النص الاحترافي
# =========================================================
with tab_vision:
    st.header("1. Executive Summary (الملخص التنفيذي)")
    col_text, col_kpi = st.columns([2, 1])
    
    with col_text:
        st.markdown("""
        **ITIS (Integrated Travel Intelligence System)** is a sovereign financial infrastructure designed to replace broken legacy banking in conflict zones (Sudan Pilot).
        
        **The Problem (المشكلة):**
        * 🔴 **Blocked Funds:** Millions of IATA/Airline dollars trapped in local currency.
        * 🔴 **Broken Infra:** Ground internet/banking fails during crises.
        * 🔴 **Compliance Risk:** Cash-heavy economy isolates the market.

        **The Solution (الحل السيادي):**
        * ✅ **Space-Native:** 100% Reliance on **Starlink** (No ground cables).
        * ✅ **Gold-Standard:** Converting debt to **Gold Assets** held at **QNB**.
        * ✅ **Digital Settlement:** Issuing **AI-GD** (Gold-Backed Token) for instant payments.
        """)
        
    with col_kpi:
        st.markdown("### 🎯 Targets")
        st.metric("Market Size", "10 Million Users", "Diaspora")
        st.metric("Debt to Clear", "$ 450 Million", "IATA Funds")
        st.metric("Infrastructure", "Zero Capex", "Space-Based")

# =========================================================
# TAB 2: غرفة القيادة (Live Ops) + الكرة الأرضية 3D
# =========================================================
with tab_ops:
    st.header("2. Sovereign Command Center (العمليات الحية)")
    
    # صف العدادات
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🥇 Gold Reserve (QNB Vault)", "1,452.5 kg", "+2.1% Today")
    m2.metric("💎 AI-GD Token Price", "$ 68.82", "Pegged 1g Gold")
    m3.metric("✈️ IATA Debt Cleared", "$ 12.4M", "Liquidated")
    m4.metric("📡 Active Starlink Nodes", "10,420", "Online")

    st.markdown("---")
    
    # الكرة الأرضية (3D Globe) - Plotly
    st.subheader("🌍 Global Settlement Layer (Starlink Network)")
    
    fig_globe = go.Figure()
    
    # الخطوط الذهبية (مسارات المال)
    fig_globe.add_trace(go.Scattergeo(
        lon = [32.55, 51.51, 32.55, -74.00, 32.55, -0.12],
        lat = [15.50, 25.28, 15.50, 40.71, 15.50, 51.50],
        mode = 'lines',
        line = dict(width = 2, color = '#D4AF37'),
        name = 'Gold/Data Flow'
    ))
    
    # النقاط (المراكز)
    fig_globe.add_trace(go.Scattergeo(
        lon = [32.55, 51.51, -74.00, -0.12],
        lat = [15.50, 25.28, 40.71, 51.50],
        text = ['KHARTOUM (HQ)', 'DOHA (QNB VAULT)', 'NEW YORK (AMEX)', 'LONDON (IATA)'],
        mode = 'markers+text',
        marker = dict(size = 15, color = '#00FFFF', line=dict(width=2, color='white')),
        textposition="top center",
        textfont=dict(color="white", size=14),
        name = 'Sovereign Nodes'
    ))

    fig_globe.update_layout(
        geo = dict(
            projection_type = "orthographic",
            showland = True, landcolor = "#111",
            showocean = True, oceancolor = "#000",
            showcountries = True, countrycolor = "#333",
            bgcolor = "black"
        ),
        height=600, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="black"
    )
    st.plotly_chart(fig_globe, use_container_width=True)

# =========================================================
# TAB 3: المخطط الهندسي (Architecture) - الرسمة رقم 1
# =========================================================
with tab_arch:
    st.header("3. System Architecture (المخطط الهندسي)")
    st.write("كيف يربط النظام الفضاء بالأرض لحل أزمة السيولة:")
    
    sys = graphviz.Digraph()
    sys.attr(rankdir='LR', bgcolor='black')
    sys.attr('node', shape='rect', style='filled', fillcolor='#222', fontcolor='white', color='#D4AF37', fontname='Helvetica')
    sys.attr('edge', color='white')

    # العقد
    sys.node('USER', '📱 Diaspora User\n(Starlink App)')
    sys.node('SAT', '🛰️ Starlink LEO\n(Space Layer)')
    sys.node('CORE', '🦅 ITIS AI Core\n(Logic & Ledger)')
    sys.node('AMEX', '🛡️ Amex Gateway\n(Compliance)')
    sys.node('QNB', '🏦 QNB Vault\n(Gold Assets)')
    sys.node('IATA', '✈️ IATA / Airlines\n(Settlement)')

    # المسار
    sys.edge('USER', 'SAT', ' 1. Request')
    sys.edge('SAT', 'CORE', ' 2. Uplink')
    sys.edge('CORE', 'AMEX', ' 3. KYC/OFAC')
    sys.edge('AMEX', 'QNB', ' 4. Gold Lock')
    sys.edge('QNB', 'IATA', ' 5. Pay AI-GD')
    sys.edge('IATA', 'USER', ' 6. Ticket')

    st.graphviz_chart(sys)

# =========================================================
# TAB 4: نموذج العملة (AI-GD Model) - الرسمة رقم 2
# =========================================================
with tab_token:
    st.header("4. AI-GD: Liquidity Mining Model")
    st.write("دورة تسييل الديون إلى ذهب (Debt-to-Asset Swap):")
    
    c_t1, c_t2 = st.columns([3, 2])
    
    with c_t1:
        money = graphviz.Digraph()
        money.attr(rankdir='TB', bgcolor='black')
        money.attr('node', shape='box', style='rounded,filled', fillcolor='#111', fontcolor='white', color='#00FFFF')
        money.attr('edge', color='#00FFFF')

        money.node('DEBT', '❌ Blocked Funds (SDG)', color='red')
        money.node('MINING', '⛏️ Gold Sourcing (Local)')
        money.node('VAULT', '🔒 QNB Vault (Assets)', color='gold', fontcolor='gold')
        money.node('TOKEN', '💎 AI-GD Token (Digital)', color='gold')
        money.node('SETTLE', '✅ IATA Settlement (USD)', color='green')

        money.edge('DEBT', 'MINING', ' Financing')
        money.edge('MINING', 'VAULT', ' Physical Supply')
        money.edge('VAULT', 'TOKEN', ' Minting')
        money.edge('TOKEN', 'SETTLE', ' Payment')

        st.graphviz_chart(money)
        
    with c_t2:
        st.info("ℹ️ **Mechanism:**")
        st.write("1. QNB uses blocked funds to buy local gold.")
        st.write("2. Gold is stored as a sovereign asset.")
        st.write("3. AI-GD tokens are issued against this gold.")
        st.write("4. Airlines accept AI-GD for instant settlement.")

# =========================================================
# TAB 5: التحالف (Alliance) - الرسمة رقم 3 (الامتثال)
# =========================================================
with tab_partners:
    st.header("5. The Strategic Alliance & Compliance")
    
    # الرسمة الثالثة: الامتثال
    st.subheader("🛡️ The Compliance Shield (جدار الحماية)")
    comp = graphviz.Digraph()
    comp.attr(rankdir='LR', bgcolor='black')
    comp.attr('node', shape='ellipse', style='filled', fillcolor='#333', fontcolor='white', color='#00FF00')
    
    comp.node('TX', 'Transaction')
    comp.node('OFAC', 'OFAC Check')
    comp.node('KYC', 'KYC Verify')
    comp.node('AI', 'AI Risk Score')
    comp.node('OK', 'APPROVED ✅', color='green', fontcolor='green')
    comp.node('NO', 'REJECTED ❌', color='red', fontcolor='red')
    
    comp.edge('TX', 'OFAC')
    comp.edge('OFAC', 'KYC')
    comp.edge('KYC', 'AI')
    comp.edge('AI', 'OK', ' Low Risk')
    comp.edge('AI', 'NO', ' High Risk')
    
    st.graphviz_chart(comp)
    
    st.markdown("---")
    c_p1, c_p2, c_p3 = st.columns(3)
    c_p1.success("🛰️ **STARLINK:** Infrastructure")
    c_p2.warning("🏦 **QNB GROUP:** Treasury")
    c_p3.info("🛡️ **AMEX GBT:** Compliance")

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
