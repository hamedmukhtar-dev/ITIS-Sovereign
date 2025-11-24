"""
app.py — ITIS Executive Streamlit Frontend (Production-ready demo)

Features:
- Clean black × gold UI
- Configurable backend base URL via env var BACKEND_URL
- Robust API client (httpx) with retry/backoff
- Create settlement instruction (form)
- Simulate bank callback
- Call AI-GD decision endpoint and show stored decision
- Render Graphviz diagram and offer PNG download (if graphviz installed)
- Load reference architecture image from /mnt/data if present
- Clear error handling and user feedback
- Lightweight logging (prints) for local debugging

Environment:
- BACKEND_URL (default: http://localhost:8000)
- ARCH_REF_PATH (optional path to architecture image)
- STREAMLIT settings as needed

Run:
streamlit run app.py --server.port 8501 --server.headless true
"""

import os
import json
import time
import logging
from io import BytesIO
from pathlib import Path
from typing import Optional

import streamlit as st
import graphviz
from PIL import Image
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# ----------------------------
# Basic logging
# ----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("itis_frontend")

# ----------------------------
# Configuration
# ----------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
ARCH_REF_PATH = os.getenv("ARCH_REF_PATH", "/mnt/data/ChatGPT Image Nov 15, 2025, 08_50_16 AM.png")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "8.0"))

# HTTP client factory with timeouts & retry
def get_client():
    return httpx.Client(timeout=REQUEST_TIMEOUT)

# Retry policy for flaky network calls (tenacity)
@retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=4), stop=stop_after_attempt(3),
       retry=retry_if_exception_type(httpx.RequestError))
def http_post(path: str, json_payload: dict):
    url = f"{BACKEND_URL}{path}"
    logger.info("POST %s -> %s", url, json_payload.get("transaction_id", "no-tx"))
    with get_client() as c:
        r = c.post(url, json=json_payload)
        r.raise_for_status()
        return r.json()

@retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=4), stop=stop_after_attempt(3),
       retry=retry_if_exception_type(httpx.RequestError))
def http_get(path: str):
    url = f"{BACKEND_URL}{path}"
    logger.info("GET %s", url)
    with get_client() as c:
        r = c.get(url)
        r.raise_for_status()
        return r.json()

# ----------------------------
# Streamlit page config & CSS
# ----------------------------
st.set_page_config(page_title="ITIS — Sovereign NDC Financial System", page_icon="🦅", layout="wide")
st.markdown(
    """
    <style>
        body, .stApp { background-color: #000000; color: #EDEDED; }
        h1, h2, h3, h4, h5 { color: #D4AF37 !important; font-family: 'Segoe UI', sans-serif; }
        .stButton>button { background-color: #0b0b0b; border: 1px solid #D4AF37; color: #D4AF37; }
        .small { font-size:12px; color:#9A9A9A; }
        .mono { font-family: monospace; color: #CFCFCF; }
        .stDownloadButton>button { background-color:#D4AF37; color:black; }
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
    st.title("ITIS — The Sovereign NDC Financial System (Executive)")
    st.markdown("**Space-native • Gold-stabilized • AI-directed**")

st.divider()

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(
    [
        "Overview",
        "Create Instruction",
        "Bank Callback",
        "AI-GD / Decision",
        "Architecture",
        "Simulate Flow",
    ]
)

# ----------------------------
# Tab: Overview
# ----------------------------
with tabs[0]:
    st.header("Executive Overview")
    st.markdown(
        """
ITIS is a sovereign-grade, non-custodial financial coordinator for travel payments.
This UI is a demo/prototype to interact with the backend mock (FastAPI).
"""
    )
    st.subheader("Environment")
    st.markdown(f"- Backend base URL: `{BACKEND_URL}`")
    st.markdown(f"- Architecture image path: `{ARCH_REF_PATH}`")
    st.markdown("Use the tabs to create instructions, simulate bank callbacks, call AI-GD, and view the architecture diagram.")

# ----------------------------
# Helper UI functions
# ----------------------------
def show_api_error(e: Exception):
    st.error(f"API error: {str(e)}")
    logger.exception("API error occurred")

# ----------------------------
# Tab: Create Settlement Instruction
# ----------------------------
with tabs[1]:
    st.header("Create Settlement Instruction")
    st.markdown("Create a settlement instruction that the backend will persist and (optionally) forward to the bank connector.")
    with st.form("form_create_instruction"):
        tx_id = st.text_input("Transaction ID", value=f"TRX-{int(time.time())}")
        amount = st.number_input("Amount", value=1250.75, format="%.2f", step=0.01)
        currency = st.selectbox("Currency", ["USD", "SDG", "EUR"], index=0)
        beneficiary_account = st.text_input("Beneficiary account", value="QNB-ACC-123456")
        metadata_raw = st.text_area("Metadata (JSON, optional)", value='{"context":{"travel_order": true}}', height=80)
        submitted = st.form_submit_button("Create Instruction")
        if submitted:
            try:
                metadata = json.loads(metadata_raw) if metadata_raw.strip() else {}
            except Exception as e:
                st.error("Invalid JSON in metadata field.")
                metadata = {}
            payload = {
                "transaction_id": tx_id,
                "amount": float(amount),
                "currency": currency,
                "beneficiary_account": beneficiary_account,
                "metadata": metadata,
            }
            try:
                with st.spinner("Creating instruction..."):
                    resp = http_post("/v1/settlement/instructions", payload)
                    st.success("Instruction created.")
                    st.json(resp)
            except Exception as e:
                show_api_error(e)

# ----------------------------
# Tab: Bank Callback
# ----------------------------
with tabs[2]:
    st.header("Simulate Bank Callback")
    st.markdown("Send a bank callback to the backend to mark an instruction as `settled` (demo).")
    with st.form("form_callback"):
        instruction_id = st.text_input("Instruction ID (from create response)")
        status = st.selectbox("Status", ["settled", "failed", "rejected"], index=0)
        bank_ref = st.text_input("Bank reference", value=f"QNB-REF-{int(time.time())}")
        settled_at = st.text_input("Settled at (ISO 8601)", value=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        details_raw = st.text_area("Details (JSON, optional)", value='{"note":"demo callback"}', height=80)
        cb_submit = st.form_submit_button("Send Callback")
        if cb_submit:
            try:
                details = json.loads(details_raw) if details_raw.strip() else {}
            except Exception:
                st.error("Invalid JSON in details.")
                details = {}
            payload = {
                "instruction_id": instruction_id,
                "status": status,
                "bank_reference": bank_ref,
                "settled_at": settled_at,
                "details": details,
            }
            try:
                with st.spinner("Sending callback..."):
                    resp = http_post("/v1/settlement/callbacks", payload)
                    st.success("Callback accepted.")
                    st.json(resp)
            except Exception as e:
                show_api_error(e)

    st.markdown("---")
    st.markdown("Lookup instruction (show latest state):")
    instr_lookup = st.text_input("Instruction ID to lookup (GET)", value="")
    if st.button("Get instruction"):
        if not instr_lookup:
            st.warning("Please enter an instruction_id to lookup.")
        else:
            try:
                resp = http_get(f"/v1/settlement/instructions/{instr_lookup}")
                st.json(resp)
            except Exception as e:
                show_api_error(e)

# ----------------------------
# Tab: AI-GD / Decision
# ----------------------------
with tabs[3]:
    st.header("AI-GD Decision Engine")
    st.markdown("Send a payload to the backend AI-GD endpoint and store/inspect the decision.")
    with st.form("form_ai"):
        tx = st.text_input("Transaction ID", value=f"TRX-{int(time.time())}")
        aml = st.number_input("AML risk score", value=10, min_value=0, max_value=100, step=1)
        cross_border = st.checkbox("Cross-border", value=True)
        volatility = st.number_input("Currency volatility (0.0-1.0)", value=0.12, min_value=0.0, max_value=10.0, step=0.01)
        ctx_meta = st.text_area("Context extra (JSON) optional", value='{"airline":"SUD AIR"}', height=80)
        ai_submit = st.form_submit_button("Run AI-GD decision")
        if ai_submit:
            try:
                extra = json.loads(ctx_meta) if ctx_meta.strip() else {}
            except Exception:
                st.error("Invalid JSON in context extra.")
                extra = {}
            payload = {
                "transaction_id": tx,
                "aml_risk_score": int(aml),
                "context": {"cross_border": bool(cross_border), "currency_volatility": float(volatility), **extra},
            }
            try:
                with st.spinner("Calling AI-GD..."):
                    resp = http_post("/v1/ai/decide", payload)
                    st.success("Decision stored.")
                    st.json(resp)
            except Exception as e:
                show_api_error(e)
    st.markdown("---")
    st.markdown("If your backend persists decisions, you can query them via its API (not implemented by default in demo).")

# ----------------------------
# Tab: Architecture Diagram
# ----------------------------
with tabs[4]:
    st.header("Architecture — Diagram & Reference")
    st.markdown("Reference image (if uploaded) and a Graphviz rendering. Graphviz PNG export requires `graphviz` system package.")
    # Show uploaded reference image if exists
    try:
        p = Path(ARCH_REF_PATH)
        if p.exists():
            try:
                img = Image.open(p)
                st.image(img, caption="Reference Architecture (uploaded)", use_column_width=True)
            except Exception as e:
                st.warning(f"Found image but failed to open: {e}")
        else:
            st.info("No reference architecture image found at configured path.")
    except Exception as e:
        st.error(f"Error checking architecture image: {e}")

    st.subheader("Graphviz — ITIS Executive Layout")
    dot = r'''
digraph ITIS {
  rankdir=TB;
  bgcolor=black;
  node [shape=rect, style=filled, fontname=Helvetica, fontcolor=white, fillcolor="#111111", color="#D4AF37"];
  "END USER\n(Mobile/Web)" -> "NDC OFFER\n(Offer Engine)";
  "NDC OFFER\n(Offer Engine)" -> "ORDER MGMT\n(Order & OMS)";
  "ORDER MGMT\n(Order & OMS)" -> "NDC DISTRIBUTION\n(Messaging / ARNs)";
  "ORDER MGMT\n(Order & OMS)" -> "GOPAY\n(Movement Layer)";
  "GOPAY\n(Movement Layer)" -> "SETTLEMENT\n(Bank API)";
  "SETTLEMENT\n(Bank API)" -> "GOLD WALLET\n(Stability Layer)";
  "ORDER MGMT\n(Order & OMS)" -> "AI-GD\n(Decision Engine)";
  "GOPAY\n(Movement Layer)" -> "AI-GD\n(Decision Engine)";
  "AI-GD\n(Decision Engine)" -> "ROUTING\n(BANK/GOLD/HYBRID/REVIEW)";
  "STARLINK\n(Space Layer)" -> "All Nodes\n(Connectivity)";
  edge [color="#00FFFF"];
}
'''
    try:
        st.graphviz_chart(dot, use_container_width=True)
        # Attempt to produce PNG for download
        try:
            src = graphviz.Source(dot)
            png_bytes = src.pipe(format="png")
            if png_bytes:
                st.download_button("Download Graphviz PNG", data=png_bytes, file_name="itis_graphviz.png", mime="image/png")
        except Exception:
            st.info("Graphviz PNG export not available in this environment (system 'dot' may be missing). The diagram still renders.")
    except Exception as e:
        st.error(f"Failed to render graphviz: {e}")

# ----------------------------
# Tab: Simulate Full Flow (Demo)
# ----------------------------
with tabs[5]:
    st.header("Simulate Full NDC Flow (Demo)")
    st.markdown("This runs a mocked sequence: create instruction -> AI decision -> send to bank -> callback. All via backend endpoints.")
    if st.button("Run full mock flow"):
        try:
            # 1 - create instruction
            txid = f"TRX-{int(time.time())}"
            payload_instr = {
                "transaction_id": txid,
                "amount": 250.00,
                "currency": "USD",
                "beneficiary_account": "QNB-ACC-0001",
                "metadata": {"context": {"travel_order": True, "airline": "SUD AIR"}}
            }
            with st.spinner("1) Creating settlement instruction..."):
                inst_resp = http_post("/v1/settlement/instructions", payload_instr)
                st.success("Instruction created.")
                st.json(inst_resp)

            # 2 - AI decision
            payload_decide = {"transaction_id": txid, "aml_risk_score": 5, "context": {"cross_border": True, "currency_volatility": 0.12}}
            with st.spinner("2) Running AI-GD decision..."):
                dec_resp = http_post("/v1/ai/decide", payload_decide)
                st.success("AI-GD decision recorded.")
                st.json(dec_resp)

            # 3 - simulate bank connector (optional - backend might auto-handle)
            # For demo: call bank connector flow by posting a callback
            inst_id = inst_resp.get("instruction_id")
            cb_payload = {
                "instruction_id": inst_id,
                "status": "settled",
                "bank_reference": f"QNB-REF-{int(time.time())}",
                "settled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "details": {"note": "auto-demo"}
            }
            with st.spinner("3) Sending bank callback..."):
                cb_resp = http_post("/v1/settlement/callbacks", cb_payload)
                st.success("Bank callback accepted.")
                st.json(cb_resp)

            st.balloons()
            st.success("Full demo flow complete.")
        except Exception as e:
            show_api_error(e)

# ----------------------------
# Footer
# ----------------------------
st.divider()
st.markdown(
    """
**Note:** This UI is a demo coordinator and does not custody funds. For production:
- Use secure secrets management for API keys and DB credentials.
- Protect backend endpoints with authentication & TLS.
- Replace demo flows with robust queues and idempotent processing.
"""
)
