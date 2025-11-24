# ============================================================
# ITIS — SOVEREIGN FINANCIAL SYSTEM (V4 EXECUTIVE BUILD)
# Full Professional Version — Black × Gold Edition
# ============================================================

import streamlit as st
import graphviz
from PIL import Image
from pathlib import Path

# ------------------------------------------------------------
# PAGE SETUP
# ------------------------------------------------------------
st.set_page_config(
    page_title="ITIS — Sovereign NDC Financial System",
    page_icon="🦅",
    layout="wide",
)

# ------------------------------------------------------------
# THEME STYLING
# ------------------------------------------------------------
st.markdown("""
<style>
    body, .stApp {
        background-color: black !important;
    }
    h1, h2, h3, h4, h5 {
        color: #D4AF37 !important;
        font-family: 'Segoe UI', sans-serif;
    }
    p, li, span, div {
        color: #E0E0E0 !important;
        font-size: 16px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1b1b1b;
        color: #888;
        border: 1px solid #333;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37 !important;
        color: black !important;
        border: 1px solid #D4AF37;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.title("🦅 ITIS — The Sovereign NDC Financial System (V4)")
st.markdown("### The First Space-Native, Gold-Stabilized, AI-Directed Financial Infrastructure")

st.divider()

# ============================================================
# TABS
# ============================================================

tabs = st.tabs([
    "🌐 SYSTEM OVERVIEW",
    "🟦 Movement Layer (GoPay)",
    "🟣 Settlement Layer (Bank)",
    "🟡 Stability Layer (Gold)",
    "🟠 AI-GD Intelligence Layer",
    "🛰️ Space Layer (Starlink)",
    "📊 Architecture Diagram (PNG + Graphviz)",
    "🔁 End-to-End NDC Cycle"
])

# ------------------------------------------------------------
# 1) SYSTEM OVERVIEW
# ------------------------------------------------------------
with tabs[0]:
    st.header("System Overview — V4 Executive Description")

    st.markdown("""
    ITIS is a **sovereign-grade financial system** built above terrestrial infrastructure.  
    It integrates **NDC**, **AI decisioning**, **gold settlement**, and **Starlink connectivity**  
    into a unified, intelligent value-routing engine.

    ### ITIS is:
    - Non-custodial  
    - AI-directed  
    - Gold-stabilized  
    - Space-native  
    - Fully NDC-integrated  
    """)

    st.subheader("The 5 Core Layers")
    st.markdown("""
    1. 🟦 **Movement Layer (GoPay)** — Transaction intake & routing  
    2. 🟣 **Settlement Layer (Bank)** — Legal trust & final posting  
    3. 🟡 **Stability Layer (Gold)** — Value preservation & conversion  
    4. 🟠 **AI-GD Intelligence** — Decision engine & risk orchestration  
    5. 🛰️ **Space Layer (Starlink)** — Always-on connectivity  
    """)

# ------------------------------------------------------------
# 2) Movement Layer
# ------------------------------------------------------------
with tabs[1]:
    st.header("🟦 Movement Layer (GoPay) — The Circulatory System")

    st.markdown("""
    The Movement Layer is where every ITIS transaction **enters** the ecosystem.

    ### Responsibilities:
    - User initiates payment  
    - Merchant receives request  
    - Transaction envelope created  
    - Risk pre-check (velocity, AML, device)  
    - Telemetry forwarded to AI-GD  
    - Pre-settlement formatting  
    """)

    st.info("This layer does NOT hold funds — it ONLY routes value.")

# ------------------------------------------------------------
# 3) Settlement Layer
# ------------------------------------------------------------
with tabs[2]:
    st.header("🟣 Settlement Layer (Bank) — The Legal Trust Layer")

    st.markdown("""
    ITIS sends structured settlement instructions to a licensed bank.  
    Banks execute, reconcile, confirm, and ensure AML compliance.

    **ITIS does not perform settlement — it instructs settlement.**
    """)

# ------------------------------------------------------------
# 4) Gold Stability Layer
# ------------------------------------------------------------
with tabs[3]:
    st.header("🟡 Stability Layer (Gold) — The Value Anchor")

    st.markdown("""
    A portion of a payment may be routed to gold.  
    Gold acts as a sovereign, neutral, globally accepted store of value.

    Used for:
    - Cross-border protection  
    - Sanction-immune value  
    - Inflation hedging  
    """)

# ------------------------------------------------------------
# 5) AI-GD Intelligence Layer
# ------------------------------------------------------------
with tabs[4]:
    st.header("🟠 AI-GD Intelligence Layer — The Brain")

    st.markdown("""
    AI-GD analyzes the full transaction context and selects one of four routes:

    ```
    BANK
    GOLD
    HYBRID
    REVIEW
    ```

    ### Responsibilities:
    - Fraud detection  
    - Risk scoring  
    - Volatility analysis  
    - Liquidity prediction  
    - Real-time routing  
    """)

# ------------------------------------------------------------
# 6) Space Layer
# -----------------------------------
