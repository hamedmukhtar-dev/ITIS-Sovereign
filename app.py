# app.py
"""
ITIS — NDC-INTEGRATED SOVEREIGN LAYER (Streamlit)
English only — Executive presentation + Graphviz + AI-GD placeholder
Place this file at: itis-sovereign/main/app.py
Requirements (example): streamlit, graphviz, pillow, openai, python-dotenv
"""

import os
import io
import json
import time
from pathlib import Path

import streamlit as st
from PIL import Image
import graphviz

# Optional: OpenAI integration (if you install openai and set OPENAI_API_KEY)
try:
    import openai
except Exception:
    openai = None

# ----------------------------
# Configuration
# ----------------------------
st.set_page_config(page_title="ITIS — NDC Sovereign Layer", layout="wide", initial_sidebar_state="expanded")

# Customize paths — adjust if needed
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"  # optional
REFERENCE_IMG = BASE_DIR / "assets" / "architecture_reference.png"  # your uploaded PNG

# Theme CSS (simple corporate black/gold)
st.markdown(
    """
    <style>
    .stApp { background-color: #000000; color: #EDEDED; }
    .title { color: #D4AF37; font-size:30px; font-weight:700; }
    .subtitle { color: #00FFFF; font-size:14px; margin-bottom:8px; }
    .card { background: linear-gradient(180deg,#0b0b0b,#111); border:1px solid #222; padding:14px; border-radius:8px; }
    .gold { color: #D4AF37; font-weight:700; }
    .mono { font-family: monospace; color: #CFCFCF; }
    .small { font-size:12px; color:#9A9A9A; }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Helper: AI-GD decision (placeholder)
# ----------------------------
def ai_gd_decision(transaction_payload: dict) -> dict:
    """
    Example decision wrapper for AI-GD.
    If OPENAI_API_KEY is set and openai is installed, will call a simple prompt.
    Otherwise uses a deterministic fallback rule set.

    Return:
        {"route": "BANK"|"GOLD"|"HYBRID"|"REVIEW", "reason": "..."}
    """
    # Basic rules fallback
    try:
        # Try OpenAI if available and configured
        api_key = os.getenv("OPENAI_API_KEY")
        if openai is not None and api_key:
            openai.api_key = api_key
            prompt = (
                "You are ITIS AI-GD. Decide route for a transaction. "
                "Return JSON with fields: route (BANK|GOLD|HYBRID|REVIEW), reason.\n\n"
                f"Transaction: {json.dumps(transaction_payload)}\n"
            )
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # you may change model name to available one
                messages=[{"role": "system", "content": "You are a concise decision engine."},
                          {"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.0,
            )
            text = resp.choices[0].message.content.strip()
            # Attempt JSON parse
            try:
                parsed = json.loads(text)
                return {"route": parsed.get("route", "REVIEW"), "reason": parsed.get("reason", text)}
            except Exception:
                # fallback: parse naive
                if "GOLD" in text.upper():
                    return {"route": "GOLD", "reason": text}
                if "HYBRID" in text.upper():
                    return {"route": "HYBRID", "reason": text}
                if "BANK" in text.upper():
                    return {"route": "BANK", "reason": text}
                return {"route": "REVIEW", "reason": text}
    except Exception as e:
        # ignore OpenAI failures and continue to rule-based
        pass

    # Deterministic rule-based fallback
    amount = float(transaction_payload.get("amount", 0))
    currency = transaction_payload.get("currency", "USD").upper()
    cross_border = transaction_payload.get("context", {}).get("cross_border", False)
    volatility = transaction_payload.get("context", {}).get("currency_volatility", 0.0)

    # Simple rules:
    if transaction_payload.get("aml_risk_score", 0) > 80:
        return {"route": "REVIEW", "reason": "High AML risk score"}
    if cross_border and (volatility > 0.1 or amount > 1000):
        return {"route": "GOLD", "reason": "Cross-border + volatility/large amount -> gold candidate"}
    if amount <= 1000:
        return {"route": "BANK", "reason": "Standard bank settlement preferred"}
    return {"route": "HYBRID", "reason": "Mixed routing due to size/conditions"}

# ----------------------------
# Sidebar / Header
# ----------------------------
with st.sidebar:
    st.image(str(LOGO_PATH)) if LOGO_PATH.exists() else st.markdown("<div class='title'>ITIS</div>", unsafe_allow_html=True)
    st.markdown("**ITIS — NDC Integrated Sovereign Layer (English only)**")
    st.markdown("---")
    st.markdown("Quick actions:")
    st.write("- Export architecture PNG (use button on page)")
    st.write("- Configure OPENAI_API_KEY for AI-GD testing")
    st.markdown("---")
    st.markdown("Status:")
    openai_state = "configured" if (openai is not None and os.getenv("OPENAI_API_KEY")) else "not configured"
    st.markdown(f"- OpenAI: **{openai_state}**")
    st.markdown("---")
    st.markdown("Contact: Hamed Mukhtar — Dar Al Khartoum Alliance")

# ----------------------------
# Page Header
# ----------------------------
col1, col2 = st.columns([1, 6])
with col1:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=84)
with col2:
    st.markdown('<div class="title">ITIS — NDC-Integrated Sovereign Layer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">NDC: OFFER • ORDER • MESSAGING • DISTRIBUTION — Integrated with AI-GD and Gold Settlement</div>', unsafe_allow_html=True)

st.divider()

# ----------------------------
# Architecture Graphviz (English only)
# ----------------------------
st.subheader("Architecture Diagram — Executive (English)")

dot = """
digraph ITIS_NDC {
  rankdir=TB;
  node [shape=rect, style=filled, fontname=Helvetica, fontcolor=white, fillcolor="#111111", color="#D4AF37"];
  "END USER\\n(Mobile / Web)" -> "NDC OFFER\\n(Offer Engine)";
  "NDC OFFER\\n(Offer Engine)" -> "ORDER MANAGEMENT\\n(Order & OMS)";
  "ORDER MANAGEMENT\\n(Order & OMS)" -> "NDC DISTRIBUTION\\n(Messaging / ARNs)";
  "ORDER MANAGEMENT\\n(Order & OMS)" -> "GOPAY\\n(Movement Layer)";
  "GOPAY\\n(Movement Layer)" -> "SETTLEMENT LAYER\\n(Bank APIs)";
  "SETTLEMENT LAYER\\n(Bank APIs)" -> "GOLD WALLET\\n(Stability Layer)";
  "ORDER MANAGEMENT\\n(Order & OMS)" -> "AI-GD\\n(OpenAI Decision Engine)";
  "GOPAY\\n(Movement Layer)" -> "AI-GD\\n(OpenAI Decision Engine)";
  "AI-GD\\n(OpenAI Decision Engine)" -> "ROUTING ENGINE\\n(Bank / Gold / Hybrid / Review)";
  "STARLINK\\n(Space Layer)" -> "All Nodes\\n(Connectivity)";
  edge [color=\"#00FFFF\", fontsize=10];
}
"""

# Display Graphviz
st.graphviz_chart(dot, use_container_width=True)

# Attempt to export Graphviz as PNG and make downloadable
st.write("")
col_a, col_b = st.columns([1, 1])
with col_a:
    try:
        gv = graphviz.Source(dot)
        png_bytes = gv.pipe(format='png')
        if png_bytes:
            st.download_button("Download Architecture PNG", data=png_bytes, file_name="itis_architecture_graphviz.png", mime="image/png")
    except Exception as e:
        st.warning("Graphviz PNG export unavailable in this environment. You can still view the diagram above.")
        # no raise

with col_b:
    # Show uploaded reference image if present
    if REFERENCE_IMG.exists():
        try:
            img = Image.open(REFERENCE_IMG)
            st.image(img, caption="Reference architecture (original PNG)", use_column_width=True)
        except Exception:
            st.error("Failed to load reference image.")

st.markdown("---")

# ----------------------------
# Executive sections for 5 layers (English only)
# ----------------------------
st.header("Executive Layer Summaries")

# Movement Layer (GoPay)
with st.expander("Layer 1 — Movement Layer (GoPay) — Executive Detail", expanded=True):
    st.markdown("**Purpose:** GoPay is the Movement Layer — entry point for value and the primary data sensor for AI-GD.")
    st.markdown("- **User Wallet (non-custodial):** payment initiation, tokenized QR, transaction history.")
    st.markdown("- **Merchant Wallet:** invoice, settlement request, reporting.")
    st.markdown("- **Payment Gateway (API):** REST endpoints, webhooks, merchant keys.")
    st.markdown("- **Transaction Engine:** validation, anti-dup, routing to settlement.")
    st.markdown("- **Behavior & Risk Module:** pre-AI anomaly detection and scoring.")
    st.markdown("- **Integration Layer:** bank APIs, telco/mobile money, travel systems (NDC/GDS).")
    st.markdown("- **Pre-settlement Processor:** prepares ISO-like payload for bank settlement.")
    st.markdown("")
    st.markdown("**Non-custodial legal position:** GoPay coordinates movement and sends settlement instructions. It does not hold or custody client funds.")

# Settlement Layer (Bank)
with st.expander("Layer 2 — Settlement Layer (Bank) — Executive Detail", expanded=False):
    st.markdown("**Purpose:** Institutional trust anchor that executes financial finality through licensed bank rails.")
    st.markdown("- Receive structured settlement instructions and authorize reservations.")
    st.markdown("- Reconciliation, exception handling, and audit trail.")
    st.markdown("- AML/KYC enforcement and regulatory reporting.")
    st.markdown("- Interface with custodians for asset-conversion directives (e.g., gold).")
    st.markdown("")
    st.markdown("**Why banks:** Banks provide legal finality, ledger authority, and regulatory accountability. ITIS sends instructions; banks execute.")

# Stability Layer (Gold Wallet)
with st.expander("Layer 3 — Stability Layer (Gold Wallet) — Executive Detail", expanded=False):
    st.markdown("**Purpose:** Anchor value by converting designated settlement amounts into gold-backed holdings (via custodian).")
    st.markdown("- Gold conversion directives are sent as custodial instructions to licensed custodians.")
    st.markdown("- This layer reduces volatility and provides a stable reference value (AI-GD uses this in decisioning).")
    st.markdown("- ITIS coordinates conversion instructions but does not custody the gold.")

# Intelligence Layer (AI-GD)
with st.expander("Layer 4 — Intelligence Layer (AI-GD) — Executive Detail", expanded=False):
    st.markdown("**Purpose:** Real-time decisioning and stabilization engine. Integrates LLMs/ML with rules engines.")
    st.markdown("- Routing logic: Bank / Gold / Hybrid / Review.")
    st.markdown("- Fraud detection, behavior scoring, liquidity forecasting.")
    st.markdown("- Explainability, audit logs, and governance are mandatory.")
    st.markdown("- Integration pattern: microservice (FastAPI) with secure logs and fallback rule engine.")

# Space Layer (Starlink)
with st.expander("Layer 5 — Space Layer (Starlink) — Executive Detail", expanded=False):
    st.markdown("**Purpose:** Resilient connectivity to ensure uptime in degraded environments.")
    st.markdown("- Satellite connectivity provides continuity during terrestrial network failures.")
    st.markdown("- Supports remote operations, over-the-horizon liquidity coordination, and global availability.")

st.markdown("---")

# ----------------------------
# Quick demo: sample payload & AI decision
# ----------------------------
st.header("Demo: Sample Transaction & AI-GD Routing (Example)")

sample_payload = {
    "transaction_id": "TRX-0001",
    "amount": 1250.75,
    "currency": "USD",
    "merchant_id": "M-203",
    "user_id": "U-9001",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "context": {"travel_order": True, "cross_border": True, "currency_volatility": 0.12},
    "aml_risk_score": 10
}

st.subheader("Sample payload (JSON)")
st.code(json.dumps(sample_payload, indent=2), language="json")

if st.button("Run AI-GD Decision (example)"):
    with st.spinner("AI-GD evaluating..."):
        decision = ai_gd_decision(sample_payload)
        st.success(f"Route: {decision['route']}")
        st.write("Reason:", decision["reason"])

st.markdown("---")

# ----------------------------
# Next steps & developer notes
# ----------------------------
st.header("Developer Notes & Next Steps")
st.markdown("""
- Add real OpenAI API key as environment variable `OPENAI_API_KEY` for AI-GD integration.
- Implement ai_gd_decision as a secure microservice (recommended FastAPI) for production.
- Wire GoPay payment gateway endpoints to a Bank Sandbox for end-to-end testing.
- Implement immutable logging (append-only) for all settlement instructions.
- After testing, integrate custodial Gold Wallet APIs and finalize SLA and legal agreements.
- Add monitoring, alerting, and stress tests using Starlink connectivity scenarios.
""")

st.success("App page loaded. Export the Graphviz PNG above, or replace reference architecture image in /assets and redeploy.")
