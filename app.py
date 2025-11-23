import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import graphviz

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
# 2. تصميم الهيبة الملكية (Royal Dark & Gold)
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #000000; }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Segoe UI', sans-serif; }
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
    .stTabs [data-baseweb="tab"] { background-color: #1a1a1a; color: #888; border: 1px solid #333; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; font-weight: bold; border: 1px solid #D4AF37; }
    
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
    st.info("📡 **Connectivity:** Starlink Global")
    st.warning("🏦 **Treasury:** QNB Group")
    st.success("🛡️ **Compliance:** Amex GBT / OFAC")
    st.markdown("---")
    st.write("Commander: **Hamed Mukhtar**")
    st.write("Version: **6.0 (Color-Coded Master)**")

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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📜 GLOBAL VISION", 
    "🚀 LIVE OPERATIONS", 
    "🏗️ THE MASTER BLUEPRINT", 
    "💎 AI-GD MODEL", 
    "🤝 ALLIANCE"
])

# === TAB 1: الرؤية العالمية ===
with tab1:
    st.header("1. Strategic Vision: The Cloud Nation")
    col_v1, col_v2 = st.columns([1, 1])
    with col_v1:
        st.markdown("""
        ### **Who We Are:**
        **ITIS** is the **Alternative Digital Central Bank** for the global travel industry. We operate where legacy systems end.

        ### **The Scope (Target Audience):**
        We serve the **'Cloud Nation'** ecosystem:
        * 🌍 **The Diaspora:** 10M+ Global Citizens via Starlink.
        * 🏢 **Corporate Giants (Amex GBT):** MNCS, UN, NGOs.
        * ✈️ **Global Travelers:** Seamless settlement worldwide.
        """)
    with col_v2:
        st.info("ℹ️ **Mission:** Re-engineering the global economy by converting distressed assets into Gold Standards.")
        # رسم مبسط للنطاق
        scope = graphviz.Digraph()
        scope.attr(rankdir='TB', bgcolor='black')
        scope.attr('node', shape='rect', style='filled', fillcolor='#222', fontcolor='white', color='#D4AF37')
        scope.edge('DIASPORA', 'ITIS CORE'); scope.edge('AMEX CORP', 'ITIS CORE'); scope.edge('TRAVELERS', 'ITIS CORE')
        st.graphviz_chart(scope)

# === TAB 2: غرفة القيادة (Live Ops) ===
with tab2:
    st.header("2. Sovereign Command Center")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🥇 Gold Reserve", "1,452.5 kg", "+2.1%")
    m2.metric("💎 AI-GD Token", "$ 68.82", "Pegged")
    m3.metric("✈️ Debt Cleared", "$ 12.4M", "Paid")
    m4.metric("📡 Active Nodes", "10,420", "Online")
    
    st.markdown("---")
    st.subheader("🌍 Global Settlement Layer")
    fig_globe = go.Figure(go.Scattergeo(
        lon = [32.55, 51.51, -74.00, -0.12, 55.27],
        lat = [15.50, 25.28, 40.71, 51.50, 25.20],
        mode = 'markers+lines', line = dict(width=2, color='#D4AF37'), marker = dict(size=10, color='#00FFFF')
    ))
    fig_globe.update_layout(geo=dict(showland=True, landcolor="#111", bgcolor="black"), height=500, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="black")
    st.plotly_chart(fig_globe, use_container_width=True)

# === TAB 3: المخطط الهندسي المتكامل (الملون بالألوان الصحيحة) ===
with tab3:
    st.header("3. The Master Process Flow (دورة العمليات)")
    st.markdown("### من الطلب إلى التذكرة: رحلة عبر الفضاء والذهب")
    
    # الرسمة بالألوان الصحيحة (حسب طلبك)
    flow = graphviz.Digraph()
    flow.attr(rankdir='LR', bgcolor='#050505', splines='ortho')
    flow.attr('node', shape='rect', style='filled', fontname='Arial', fontcolor='black')
    flow.attr('edge', color='white', arrowsize='0.8')

    # العقد بالألوان المحددة
    flow.node('User', '👤 1. العميل / User\n[طلب حجز + دفع]', fillcolor='#00FFFF') # سماوي
    flow.node('Space', '🛰️ 2. الفضاء / Starlink\n[تشفير ونقل]', fillcolor='#333333', fontcolor='white') # أسود
    flow.node('Brain', '🧠 3. الدماغ / ITIS AI\n[تحليل المخاطر]', fillcolor='#8e44ad', fontcolor='white') # بنفسجي
    flow.node('Amex', '🛡️ 4. الامتثال / Amex\n[فحص أمني OFAC]', fillcolor='#27ae60', fontcolor='white') # أخضر
    flow.node('QNB', '🏦 5. الخزينة / QNB\n[حجز الذهب]', fillcolor='#FFD700') # ذهبي
    flow.node('Token', '💎 6. العملة / AI-GD\n[إصدار التوكن]', fillcolor='#F1C40F') # ذهبي فاتح
    flow.node('Airline', '✈️ 7. الطيران / Airline\n[استلام الكاش]', fillcolor='#c0392b', fontcolor='white') # أحمر

    # التوصيلات
    flow.edge('User', 'Space', label=' 1')
    flow.edge('Space', 'Brain', label=' 2')
    flow.edge('Brain', 'Amex', label=' 3')
    flow.edge('Amex', 'QNB', label=' 4')
    flow.edge('QNB', 'Token', label=' 5')
    flow.edge('Token', 'Airline', label=' 6')
    
    # العودة (تذكرة)
    flow.edge('Airline', 'User', label=' تذكرة (e-Ticket)', style='dashed', color='#00FFFF')

    st.graphviz_chart(flow, use_container_width=True)
    st.info("ℹ️ **دليل الألوان:** 👤 العميل (سماوي) -> 🛰️ الفضاء (أسود) -> 🧠 الذكاء (بنفسجي) -> 🛡️ الأمان (أخضر) -> 🏦 الذهب (ذهبي) -> ✈️ الطيران (أحمر).")

# === TAB 4: نموذج العملة ===
with tab4:
    st.header("4. AI-GD Tokenomics")
    c1, c2 = st.columns(2)
    with c1:
        token = graphviz.Digraph()
        token.attr(rankdir='TB', bgcolor='black')
        token.attr('node', shape='ellipse', style='filled', fillcolor='#111', color='#00FFFF', fontcolor='#00FFFF')
        token.edge('Debt (SDG)', 'Gold (Raw)'); token.edge('Gold (Raw)', 'QNB Vault'); token.edge('QNB Vault', 'AI-GD Token'); token.edge('AI-GD Token', 'Payment')
        st.graphviz_chart(token)
    with c2:
        st.write("**Mechanism:** Debt-to-Asset Swap (Blocked Funds -> Gold -> Token)")

# === TAB 5: التحالف ===
with tab5:
    st.header("5. Strategic Partners")
    c1, c2, c3 = st.columns(3)
    c1.success("🛰️ **STARLINK:** Backbone"); c2.warning("🏦 **QNB:** Treasury"); c3.info("🛡️ **AMEX:** Compliance")

# ---------------------------------------------------------
# التذييل
# ---------------------------------------------------------
st.divider()
st.caption("CONFIDENTIAL | PROPERTY OF DAR AL KHARTOUM | EST. 1995")
