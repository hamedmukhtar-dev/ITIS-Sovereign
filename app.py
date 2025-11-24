# ============================================================
# ITIS — SOVEREIGN FINANCIAL SYSTEM (V4 EXECUTIVE BUILD)
# Full Professional Version — Black × Gold Edition
# Ready-to-drop app.py (English-only, production/demo-ready)
# + Integrated: GoLite Agency Dashboard (Streamlit)
# + Passenger details & PNR generator
# + Bank Callback (Webhook) simulator
# ============================================================

import os
import json
import time
import uuid
import random
import string
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
css = """
<style>
    body, .stApp { background-color: #000000 !important; color: #EDEDED; }
    h1, h2, h3, h4, h5 { color: #D4AF37 !important; font-family: 'Segoe UI', sans-serif; }
    p, li, span, div { color: #E0E0E0 !important; font-size: 15px; }
    .stButton>button { background-color: #0b0b0b; border: 1px solid #D4AF37; color: #D4AF37; }
    .stTabs [data-baseweb="tab"] { background-color: #1b1b1b; color: #888; border: 1px solid #333; padding: 8px 12px; }
    .stTabs [aria-selected="true"] { background-color: #D4AF37 !important; color: black !important; border: 1px solid #D4AF37; }
    .small { font-size:12px; color:#9A9A9A; }
    .mono { font-family: monospace; color: #CFCFCF; }
    .gl-card { background-color: #0f1724; border: 1px solid #1f2937; padding: 12px; border-radius: 12px; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

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
# Tabs (added: Agency Dashboard (GoLite))
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
        "Agency Dashboard (GoLite)",
    ]
)

# ----------------------------
# Tab: System Overview
# ----------------------------
with tabs[0]:
    st.header("System Overview — Executive V4")
    st.markdown(
        "ITIS is a sovereign-grade, non-custodial financial infrastructure engineered for the travel ecosystem. "
        "It integrates native NDC flows with an AI decision engine (AI-GD), a gold stability layer, licensed bank settlement, "
        "and resilient satellite connectivity. The system routes value; it does not custody it."
    )
    st.subheader("Key Properties")
    st.markdown(
        "- Non-custodial coordinator (routing & instructions only)\n"
        "- AI-directed decisioning (OpenAI / custom models)\n"
        "- Gold-backed stabilization (custodian-managed)\n"
        "- NDC-native (Offer → Order → Pay → Settle → Confirm)\n"
        "- Space-ready (Starlink backbone)"
    )

# ----------------------------
# Tab: Movement Layer (GoPay)
# ----------------------------
with tabs[1]:
    st.header("Movement Layer (GoPay) — The Circulatory System")
    st.markdown(
        "Purpose: The Movement Layer is the entry point for all transactions. It accepts payment initiation, "
        "performs immediate pre-checks, emits telemetry for AI-GD, and issues pre-settlement instructions to the Settlement Layer."
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
        "Purpose: Execute legally-binding settlement instructions via licensed banking rails. This layer is responsible for "
        "authorization, posting, reconciliation, AML/KYC checks, and sending confirmation callbacks to ITIS."
    )
    st.subheader("Create Settlement Instruction (Mock UI)")
    with st.form("create_instruction"):
        inst_tx = st.text_input("Transaction ID", value="TRX-0001")
        inst_amount = st.number_input("Amount", value=1250.75, format="%.2f")
        inst_currency = st.selectbox("Currency", ["USD", "SDG", "EUR"])
        inst_bank_account = st.text_input("Beneficiary Account", value="QNB-ACC-123456")
        submitted = st.form_submit_button("Create Settlement Instruction")
        if submitted:
            mocked_instruction = {
                "instruction_id": f"INST-{int(time.time())}",
                "transaction_id": inst_tx,
                "status": "accepted",
                "bank_reference": "QNB-REF-9922",
                "estimated_settlement_time": "5 seconds",
            }
            if "mock_instructions" not in st.session_state:
                st.session_state.mock_instructions = {}
            st.session_state.mock_instructions[mocked_instruction["instruction_id"]] = mocked_instruction
            st.success("Instruction created (mock)")
            st.json(mocked_instruction)

    st.markdown(
        "Bank Callback Simulation (for Demo): Use the form below to simulate a bank callback that changes an instruction's state."
    )

    # Callback simulator
    st.subheader("Simulate Bank Callback (Webhook)")
    with st.form("bank_callback_sim"):
        cb_inst_id = st.text_input("Instruction ID (e.g., INST-163...)")
        cb_status = st.selectbox("Status", ["settled", "rejected", "processing"])
        cb_bank_ref = st.text_input("Bank Reference", value=f"QNB-REF-{random.randint(1000,9999)}")
        cb_settled_at = st.text_input("Settled Timestamp (ISO)", value=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        submit_cb = st.form_submit_button("Send Callback (simulate)")
        if submit_cb:
            payload = {
                "instruction_id": cb_inst_id,
                "status": cb_status,
                "bank_reference": cb_bank_ref,
                "settled_at": cb_settled_at,
            }
            if "mock_instructions" in st.session_state and cb_inst_id in st.session_state.mock_instructions:
                st.session_state.mock_instructions[cb_inst_id]["status"] = cb_status
                st.session_state.mock_instructions[cb_inst_id]["bank_reference"] = cb_bank_ref
                st.session_state.mock_instructions[cb_inst_id]["settled_at"] = cb_settled_at
                st.success(f"Callback applied locally to {cb_inst_id} (mock).")
                st.json(payload)
            else:
                st.warning("Instruction not found in local mock store — still showing simulated callback payload.")
                st.json(payload)

    st.markdown("Sample curl (simulate external bank POST):")
    sample_payload = {
        "instruction_id": "INST-XXXXX",
        "status": "settled",
        "bank_reference": "QNB-REF-1234",
        "settled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    payload_str = json.dumps(sample_payload)
    curl_cmd = "curl -X POST https://your-itis-endpoint.example/v1/settlement/callbacks -H \"Content-Type: application/json\" -d '{}'".format(payload_str)
    st.code(curl_cmd, language="bash")

    if "mock_instructions" in st.session_state and st.session_state.mock_instructions:
        st.markdown("### Mock Instructions (local store)")
        st.json(st.session_state.mock_instructions)

    st.markdown(
        "Note: This callback simulator is for demo/testing. For production, implement a secure endpoint with HMAC verification and TLS."
    )

# ----------------------------
# Tab: Stability Layer (Gold)
# ----------------------------
with tabs[3]:
    st.header("Stability Layer (Gold) — Value Anchor")
    st.markdown(
        "Purpose: Convert designated settlement amounts into gold-backed holdings, via a licensed custodian."
    )
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
    st.markdown("AI-GD receives transaction telemetry and returns a route decision: BANK | GOLD | HYBRID | REVIEW")
    if st.button("Run sample AI-GD decision (demo)"):
        sample_payload = {
            "transaction_id": "TRX-0001",
            "amount": 1250.75,
            "currency": "USD",
            "context": {"cross_border": True, "currency_volatility": 0.12},
            "aml_risk_score": 10,
        }
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
    st.markdown("Primary: Starlink LEO connectivity for core infrastructure; Secondary: terrestrial fallback.")
    st.progress(100)
    st.success("Space connectivity: ONLINE (simulated)")

# ----------------------------
# Tab: Architecture Diagram
# ----------------------------
with tabs[6]:
    st.header("Architecture Diagram — Reference & Graphviz")
    st.markdown("The canonical reference image and a Graphviz rendering are shown below.")
    ARCH_REF_PATH = "/mnt/data/ChatGPT Image Nov 15, 2025, 08_50_16 AM.png"
    try:
        if Path(ARCH_REF_PATH).exists():
            img = Image.open(ARCH_REF_PATH)
            st.image(img, caption="Reference Architecture (uploaded)", use_column_width=True)
        else:
            st.warning(f"Reference image not found at: {ARCH_REF_PATH}")
    except Exception as e:
        st.error(f"Failed to load reference image: {e}")

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
        "USER → NDC OFFER → ORDER MGMT → GOPAY (Payment Initiation) → AI-GD Decision "
        "→ [BANK SETTLEMENT / GOLD CONVERSION / HYBRID] → Settlement Confirmation → NDC DISTRIBUTION"
    )
    if st.button("Simulate Full Flow (demo)"):
        st.info("1) Payment initiated at GoPay")
        time.sleep(0.6)
        st.info("2) Pre-checks (KYC, AML quick rules)")
        time.sleep(0.6)
        st.info("3) AI-GD decision: evaluating")
        time.sleep(0.8)
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
# Tab: Agency Dashboard (GoLite)
# ----------------------------
with tabs[8]:
    st.header("Agency Dashboard — GoLite NDC (Demo UI)")
    st.markdown("حنّا دمجنا واجهة الحجز: بحث، نتائج، Passenger info، توليد PNR، عربة الحجز، ودفع تجريبي.")

    # ensure session keys exist
    if "gl_cart" not in st.session_state:
        st.session_state.gl_cart = []
    if "gl_selected" not in st.session_state:
        st.session_state.gl_selected = None
    if "gl_query" not in st.session_state:
        st.session_state.gl_query = {"from": "Khartoum (KRT)", "to": "Cairo (CAI)", "date": time.strftime("%Y-%m-%d", time.gmtime(time.time()+86400)), "passengers": 1}
    if "bookings" not in st.session_state:
        st.session_state.bookings = {}
    if "mock_instructions" not in st.session_state:
        st.session_state.mock_instructions = {}

    sample_flights = [
        {"id": "FL001", "airline": "SudanAir", "depart": "06:30", "arrive": "08:45", "duration": "2h 15m", "price": "$120", "stops": 0, "fareClass": "Economy"},
        {"id": "FL002", "airline": "Blue Nile", "depart": "09:20", "arrive": "11:40", "duration": "2h 20m", "price": "$135", "stops": 0, "fareClass": "Economy Plus"},
        {"id": "FL003", "airline": "NileConnect", "depart": "14:10", "arrive": "16:35", "duration": "2h 25m", "price": "$99", "stops": 1, "fareClass": "Promo"},
    ]

    left_col, right_col = st.columns([2, 1])

    with left_col:
        with st.form("gl_search_form"):
            st.markdown("### بحث الرحلات")
            col_a, col_b, col_c, col_d = st.columns([4, 4, 2, 1])
            with col_a:
                q_from = st.text_input("من", value=st.session_state.gl_query["from"])
            with col_b:
                q_to = st.text_input("إلى", value=st.session_state.gl_query["to"])
            with col_c:
                q_date = st.date_input("تاريخ", value=st.session_state.gl_query["date"])
            with col_d:
                q_pax = st.number_input("ركاب", min_value=1, value=st.session_state.gl_query["passengers"], step=1)
            submitted = st.form_submit_button("بحث")
            if submitted:
                st.session_state.gl_query = {"from": q_from, "to": q_to, "date": str(q_date), "passengers": int(q_pax)}
                st.success("تم تحديث معايير البحث (محاكاة).")

        st.markdown("### نتائج البحث")
        st.markdown(f"عرض {len(sample_flights)} رحلات — من {st.session_state.gl_query['from']} إلى {st.session_state.gl_query['to']} بتاريخ {st.session_state.gl_query['date']}")

        for f in sample_flights:
            st.markdown("---")
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{f['airline']} — {f['id']}**")
                st.markdown(f"{f['depart']} → {f['arrive']} • {f['duration']} • Class: {f['fareClass']} • Stops: {f['stops']}")
            with c2:
                st.markdown(f"**{f['price']}**")
                if st.button(f"أضف للحجز — {f['id']}", key=f"add_{f['id']}"):
                    st.session_state.gl_cart.append(f)
                    st.success(f"أضيفت الرحلة {f['id']} للعربة (محاكاة).")
                if st.button(f"تفاصيل — {f['id']}", key=f"det_{f['id']}"):
                    st.session_state.gl_selected = f

        if st.session_state.gl_selected:
            st.markdown("### تفاصيل الرحلة المحددة")
            s = st.session_state.gl_selected
            st.json(s)
            if st.button("أضف الرحلة المحددة للعربة"):
                st.session_state.gl_cart.append(s)
                st.success("أضيفت الرحلة للعربة (محاكاة).")
            if st.button("إغلاق التفاصيل"):
                st.session_state.gl_selected = None

        st.markdown("---")
        st.markdown("### تفاصيل الراكب (Passenger Info) — لإنشاء PNR وحجز")
        with st.form("passenger_form"):
            pax_count = st.number_input("عدد الراكبين في الحجز", min_value=1, max_value=9, value=1)
            pax_list = []
            st.write("املأ بيانات كل راكب ثم اضغط 'حفظ ركّاب' — سيتم توليد PNR عند الحجز.")
            for i in range(pax_count):
                st.markdown(f"**راكب #{i+1}**")
                p_cols = st.columns([2, 2, 2])
                with p_cols[0]:
                    name = st.text_input(f"الاسم الكامل #{i+1}", key=f"pax_name_{i}")
                with p_cols[1]:
                    passport = st.text_input(f"رقم الجواز #{i+1}", key=f"pax_pass_{i}")
                with p_cols[2]:
                    dob = st.date_input(f"تاريخ الميلاد #{i+1}", key=f"pax_dob_{i}")
                contact_cols = st.columns([2, 1])
                with contact_cols[0]:
                    email = st.text_input(f"البريد الإلكتروني #{i+1}", key=f"pax_email_{i}")
                with contact_cols[1]:
                    phone = st.text_input(f"هاتف #{i+1}", key=f"pax_phone_{i}")
                pax_list.append({"name": name, "passport": passport, "dob": str(dob), "email": email, "phone": phone})
            save_pax = st.form_submit_button("حفظ الركاب")
            if save_pax:
                st.session_state.current_passengers = pax_list
                st.success("تم حفظ بيانات الركاب (محاكاة).")

    with right_col:
        st.markdown("### عربة الحجوزات")
        if len(st.session_state.gl_cart) == 0:
            st.info("لم تضف أي رحلة بعد. اضغط 'أضف للحجز' لإضافة رحلة هنا.")
        else:
            total = 0.0
            for c in st.session_state.gl_cart:
                st.markdown(f"- **{c['airline']} {c['id']}** — {c['depart']} → {c['arrive']}  • {c['fareClass']}  • {c['price']}")
                try:
                    total += float(c["price"].replace("$", ""))
                except Exception:
                    pass
            st.markdown(f"**الإجمالي (تقريبي): {total:.2f}$**")

            if st.button("انشاء حجز & توليد PNR (محاكاة)"):
                pax = st.session_state.get("current_passengers", None)
                if not pax:
                    st.error("يجب ملء بيانات الركاب قبل إنشاء الحجز.")
                else:
                    booking_id = f"BK-{int(time.time())}-{random.randint(100,999)}"
                    pnr = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    booking = {
                        "booking_id": booking_id,
                        "pnr": pnr,
                        "flights": st.session_state.gl_cart.copy(),
                        "passengers": pax,
                        "total": total,
                        "status": "pending_payment",
                        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    }
                    st.session_state.bookings[booking_id] = booking
                    inst_id = f"INST-{int(time.time())}"
                    st.session_state.mock_instructions[inst_id] = {
                        "instruction_id": inst_id,
                        "transaction_id": booking_id,
                        "status": "created",
                        "bank_reference": None,
                        "estimated_settlement_time": "n/a",
                    }
                    st.session_state.gl_cart = []
                    st.success(f"تم إنشاء الحجز (محاكاة). PNR: **{pnr}** — Booking ID: {booking_id}")
                    st.json(booking)

            if st.button("دفع عبر eWallet (محاكاة)"):
                st.info("بدء عملية الدفع — محاكاة eWallet")
                time.sleep(0.6)
                st.info("التحقق السريع: KYC/AML")
                time.sleep(0.6)
                decision = "BANK"
                st.success(f"AI-GD routing decision: {decision} (محاكاة)")
                time.sleep(0.6)
                for b_id, b in st.session_state.bookings.items():
                    if b["status"] == "pending_payment":
                        b["status"] = "paid_pending_settlement"
                st.success("تمت المحاكاة: الدفع مقبول وسيتم إرسال تأكيد بعد التسوية (محاكاة).")
                st.balloons()

        st.markdown("---")
        st.markdown("### عناصر سريعة")
        st.button("جداول الرحلات")
        st.button("إدارة التذاكر")
        st.button("مزودي NDC")
        st.button("تواصل الدعم")

        st.markdown("---")
        st.markdown("### مساعدة GoLite — AI (تجريبي)")
        st.write("أحتاج إلى مساعدة في إيجاد أرخص رحلة صباح الغد.")
        if st.button("اعرض الخيارات (AI)"):
            st.info("يجري تجهيز اقتراحات... (محاكاة)")
            time.sleep(0.6)
            st.success("أقترح NileConnect FL003 كأرخص خيار صباحي (محاكاة).")

    if st.session_state.bookings:
        st.markdown("### الحجوزات (محاكاة)")
        for bk_id, bk in st.session_state.bookings.items():
            st.markdown(f"- **{bk_id}** PNR: **{bk['pnr']}** — status: {bk['status']} — total: {bk['total']}$")
            if st.button(f"عرض تفاصيل {bk_id}", key=f"view_{bk_id}"):
                st.json(bk)

# ----------------------------
# Footer / Notes
# ----------------------------
st.divider()
st.markdown(
    "Executive Note: This demo application is a non-custodial prototype and does not handle live funds. "
    "All bank and custodian integrations are placeholders for integration with licensed partners."
)
