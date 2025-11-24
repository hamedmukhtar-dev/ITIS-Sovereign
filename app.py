# ============================================================
# ITIS — SOVEREIGN FINANCIAL SYSTEM (V4 EXECUTIVE BUILD)
# Full Professional Version — Black × Gold Edition
# ============================================================

import os
import json
import time
import streamlit as st
import graphviz
from PIL import Image
from pathlib import Path
from io import BytesIO

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(
    page_title="ITIS — Sovereign NDC Financial System",
    page_icon="🦅",
    layout="wide",
)

# ----------------------------
# Theme / Styling
# ----------------------------
st.markdown(
    """
<style>
    body, .stApp { background-color: #000000 !important; color: #EDEDED; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; font-family: 'Segoe UI', sans-serif; }
    p, li, span, div { color: #E0E0E0 !important; font-size: 15px; }
    .stButton>button { background-color: #0b0b0b; border: 1px solid #D4AF37; color: #D4AF37; }
    .stTabs [data-baseweb="tab"] { background-color: #1b1b1b; color: #888; border: 1px solid #333; padding: 8px 12px; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; border: 1px solid #D4AF37; }
    .small { font-size:12px; color:#9A9A9A; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Header
# ----------------------------
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("🦅")
with col2:
    st.title("ITIS — The Sovereign NDC Financial System (V4)")
    st.markdown("**Space-native • Gold-stabilized • AI-directed**")

st.divider()

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(
    [
        "System Overview",
        "Movement Layer (GoPay)",
        "Settlement Layer (Bank)",
        "Stability Layer (Gold)",
        "AI-GD Intelligence",
        "Space Layer (Starlink)",
        "Architecture Diagram",
        "End-to-End NDC Cycle",
    ]
)

# ----------------------------
# Tab: System Overview
# ----------------------------
with tabs[0]:
    st.header("System Overview — Executive V4")
    st.markdown(
        """
ITIS is a sovereign-grade, non-custodial financial infrastructure engineered for the travel ecosystem.
It integrates native NDC flows with an AI decision engine (AI-GD), a gold stability layer, licensed bank settlement,
and resilient satellite connectivity. The system *routes value*; it does not custody it.
"""
    )
    st.subheader("Key Properties")
    st.markdown(
        """
- Non-custodial coordinator (routing & instructions only)
- AI-directed decisioning (OpenAI / custom models)
- Gold-backed stabilization (custodian-managed)
- NDC-native (Offer → Order → Pay → Settle → Confirm)
- Space-ready (Starlink backbone)
"""
    )

# ----------------------------
# Tab: Movement Layer (GoPay)
# ----------------------------
with tabs[1]:
    st.header("Movement Layer (GoPay) — The Circulatory System")
    st.markdown(
        """
**Purpose:** The Movement Layer is the entry point for all transactions. It accepts payment initiation,
performs immediate pre-checks, emits telemetry for AI-GD, and issues pre-settlement instructions to the Settlement Layer.

**Core Components (summary):**
- User Wallet (non-custodial view)
- Merchant Wallet & Onboarding
- Payment Gateway REST API + Webhooks
- Transaction Engine (state machine, idempotency)
- Behavior & Risk Pre-AI Module
- Integration Connectors (Bank, Telco, NDC/GDS)
- Pre-Settlement Processor (ISO-like payload)
"""
    )

    st.subheader("Example: Payment Initiation (JSON)")
    sample_payment = {
        "transaction_id": "TRX-0001",
        "user_id": "U-9001",
        "merchant_id": "M-203",
        "amount": 1250.75,
        "currency": "USD",
        "payment_method": {"type": "mobile_money", "provider": "MTN", "mobile_number": "+2499XXXX"},
        "context": {"travel_order": True, "airline": "SUD AIR", "cross_border": True},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    st.code(json.dumps(sample_payment, indent=2), language="json")

# ----------------------------
# Tab: Settlement Layer (Bank)
# ----------------------------
with tabs[2]:
    st.header("Settlement Layer (Bank) — Legal Finality & Execution")
    st.markdown(
        """
**Purpose:** Execute legally-binding settlement instructions via licensed banking rails. This layer is responsible for
authorization, posting, reconciliation, AML/KYC checks, and sending confirmation callbacks to ITIS.

**API Contract (Executive):**
1) POST /v1/settlement/instructions — create instruction
2) POST /v1/settlement/callbacks — bank callback to ITIS
3) GET /v1/settlement/instructions/{id} — query status
"""
    )

    st.subheader("Create Settlement Instruction (Mock UI)")
    with st.form("create_instruction"):
        inst_tx = st.text_input("Transaction ID", value="TRX-0001")
        inst_amount = st.number_input("Amount", value=1250.75, format="%.2f")
        inst_currency = st.selectbox("Currency", ["USD", "SDG", "EUR"])
        inst_bank_account = st.text_input("Beneficiary Account", value="QNB-ACC-123456")
        submitted = st.form_submit_button("Create Settlement Instruction")
        if submitted:
            # Mock create instruction response
            mocked_instruction = {
                "instruction_id": f"INST-{int(time.time())}",
                "transaction_id": inst_tx,
                "status": "accepted",
                "bank_reference": "QNB-REF-9922",
                "estimated_settlement_time": "5 seconds",
            }
            st.success("Instruction created (mock)")
            st.json(mocked_instruction)

    st.markdown(
        """
**Bank Callback Simulation (for Demo):**
Use the bank callback endpoint to mark instruction as `settled`. ITIS expects a callback with the instruction_id and settlement details.
"""
    )

# ----------------------------
# Tab: Stability Layer (Gold)
# ----------------------------
with tabs[3]:
    st.header("Stability Layer (Gold) — Value Anchor")
    st.markdown(
        """
**Purpose:** Convert designated settlement amounts into gold-backed holdings, via a licensed custodian.
This layer reduces currency, sanction and inflation exposures.

**Notes:**
- All gold custody is performed by a licensed custodian (e.g., QNB vault).
- ITIS issues custodial directives; custody and audit are the custodian's responsibility.
"""
    )

    st.subheader("Gold Instruction Example (JSON)")
    gold_instr = {
        "instruction_id": "GOLD-0001",
        "source_instruction": "INST-90001",
        "amount": 500.00,
        "currency": "USD",
        "grams_allocated": 12.34,
        "custodian": "QNB Vault",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    st.code(json.dumps(gold_instr, indent=2), language="json")

# ----------------------------
# Tab: AI-GD Intelligence
# ----------------------------
with tabs[4]:
    st.header("AI-GD — Sovereign Decision Engine (Placeholder)")
    st.markdown(
        """
AI-GD receives transaction telemetry and returns a route decision:

