# ============================================================
# ITIS — SOVEREIGN FINANCIAL SYSTEM (V4 EXECUTIVE BUILD)
# Full Professional Version — Black × Gold Edition
# Ready-to-drop app.py (English-only, production/demo-ready)
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
    .mono { font-family: monospace; color: #CFCFCF; }
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
and resilient satellite connectivity. The system routes value; it does not custody it.
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

BANK | GOLD | HYBRID | REVIEW

Design Principles:
- Deterministic fallback rule engine (local) always available.
- LLM (OpenAI) used for complex multi-dimensional reasoning with strict prompt engineering.
- Explainability: store prompt + context + decision.
- Governance: model monitoring, rate limits, and human-in-the-loop escalation for REVIEW outcomes.
"""
    )

    st.subheader("Test AI-GD Decision (Mock logic)")
    if st.button("Run sample AI-GD decision (demo)"):
        sample_payload = {
            "transaction_id": "TRX-0001",
            "amount": 1250.75,
            "currency": "USD",
            "context": {"cross_border": True, "currency_volatility": 0.12},
            "aml_risk_score": 10,
        }

        # Simple deterministic decision logic (demo)
        if sample_payload["aml_risk_score"] > 80:
            decision = {"route": "REVIEW", "reason": "High AML risk"}
        elif sample_payload["context"]["cross_border"] and sample_payload["context"]["currency_volatility"] > 0.1:
            decision = {"route": "GOLD", "reason": "Cross-border + volatility -> gold"}
        else:
            decision = {"route": "BANK", "reason": "Standard bank settlement"}

        st.json(decision)

# ----------------------------
# Tab: Space Layer (Starlink)
# ----------------------------
with tabs[5]:
    st.header("Space Layer (Starlink) — Resilient Connectivity")
    st.markdown(
        """
**Purpose:** Ensure continuous connectivity and operational resilience under degraded terrestrial conditions.

Operational patterns:
- Primary: Starlink LEO connectivity for core infrastructure
- Secondary: Terrestrial MPLS / LTE fallback (where available)
- Offline mode: local queuing and deferred settlement instruction push when link recovers

Notes on deployment: Starlink units are placed in data centers, mobile command units, and regional hubs to guarantee availability and to support high-throughput message exchange.
"""
    )

    st.subheader("Connectivity Health (Mock)")
    st.markdown("Simulated status for demonstration.")
    st.progress(100)
    st.success("Space connectivity: ONLINE (simulated)")

# ----------------------------
# Tab: Architecture Diagram
# ----------------------------
with tabs[6]:
    st.header("Architecture Diagram — Reference & Graphviz")
    st.markdown("The canonical reference image and a Graphviz rendering are shown below.")

    # Path to the exact image you uploaded earlier (per session)
    ARCH_REF_PATH = "/mnt/data/ChatGPT Image Nov 15, 2025, 08_50_16 AM.png"

    # show reference image if present
    try:
        if Path(ARCH_REF_PATH).exists():
            img = Image.open(ARCH_REF_PATH)
            st.image(img, caption="Reference Architecture (uploaded)", use_column_width=True)
        else:
            st.warning(f"Reference image not found at: {ARCH_REF_PATH}")
    except Exception as e:
        st.error(f"Failed to load reference image: {e}")

    st.subheader("Graphviz — Executive Layout")
    dot = """
digraph ITIS {
  rankdir=TB;
  bgcolor=black;
  node [shape=rect, style=filled, fontname=Helvetica, fontcolor=white, fillcolor="#111111", color="#D4AF37"];
  "END USER\\n(Mobile/Web)" -> "NDC OFFER\\n(Offer Engine)";
  "NDC OFFER\\n(Offer Engine)" -> "ORDER MGMT\\n(Order & OMS)";
  "ORDER MGMT\\n(Order & OMS)" -> "NDC DISTRIBUTION\\n(Messaging / ARNs)";
  "ORDER MGMT\\n(Order & OMS)" -> "GOPAY\\n(Movement Layer)";
  "GOPAY\\n(Movement Layer)" -> "SETTLEMENT\\n(Bank API)";
  "SETTLEMENT\\n(Bank API)" -> "GOLD WALLET\\n(Stability Layer)";
  "ORDER MGMT\\n(Order & OMS)" -> "AI-GD\\n(Decision Engine)";
  "GOPAY\\n(Movement Layer)" -> "AI-GD\\n(Decision Engine)";
  "AI-GD\\n(Decision Engine)" -> "ROUTING\\n(BANK/GOLD/HYBRID/REVIEW)";
  "STARLINK\\n(Space Layer)" -> "All Nodes\\n(Connectivity)";
  edge [color="#00FFFF"];
}
"""
    try:
        st.graphviz_chart(dot, use_container_width=True)
        # Attempt to render & provide PNG download
        try:
            src = graphviz.Source(dot)
            png_bytes = src.pipe(format="png")
            if png_bytes:
                st.download_button("Download Graphviz PNG (executive)", data=png_bytes, file_name="itis_graphviz_architecture.png", mime="image/png")
        except Exception:
            st.info("Graphviz export not available in this environment; diagram still renders.")
    except Exception as e:
        st.error(f"Graphviz render failed: {e}")

# ----------------------------
# Tab: End-to-End NDC Cycle
# ----------------------------
with tabs[7]:
    st.header("End-to-End NDC Payment Cycle — V4")
    st.markdown(
        """
**Cycle (concise):**

USER → NDC OFFER → ORDER MGMT → GOPAY (Payment Initiation) → AI-GD Decision
→ [BANK SETTLEMENT / GOLD CONVERSION / HYBRID] → Settlement Confirmation
→ NDC DISTRIBUTION → AIRLINE / MERCHANT → TICKET ISSUED / SERVICE DELIVERED

Operational notes:
- All settlement events are logged immutably.
- AI-GD stores decision context for explainability.
- Bank callbacks update transaction states and trigger NDC confirmations.
"""
    )

    st.subheader("Quick Demo — Simulate a Full Flow (Mock)")
    if st.button("Simulate Full Flow (demo)"):
        # Simple mocked execution of the flow with delays to demonstrate sequence
        st.info("1) Payment initiated at GoPay")
        time.sleep(0.6)
        st.info("2) Pre-checks (KYC, AML quick rules)")
        time.sleep(0.6)
        st.info("3) AI-GD decision: evaluating")
        time.sleep(0.8)
        # simple deterministic decision
        decision = "GOLD"
        st.success(f"4) AI-GD decision: {decision}")
        time.sleep(0.6)
        st.info("5) Create settlement instruction (bank)")
        time.sleep(0.6)
        st.success("6) Bank callback: settled")
        time.sleep(0.6)
        st.balloons()
        st.success("End-to-end simulation complete (mock).")

# ----------------------------
# Footer / Notes
# ----------------------------
st.divider()
st.markdown(
    """
**Executive Note:** This demo application is a non-custodial prototype and does not handle live funds.
All bank and custodian integrations are placeholders for integration with licensed partners.
For production deployment: implement secure microservices, vault-managed secrets, robust logging, and legal agreements with banks and custodians.
"""
)

