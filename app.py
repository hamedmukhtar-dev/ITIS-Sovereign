# app.py — Streamlit frontend using JWT auth from backend
import os
import json
import time
import logging
from typing import Optional

import streamlit as st
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("itis_frontend_jwt")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

# session init
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user" not in st.session_state:
    st.session_state.user = None

st.set_page_config(page_title="ITIS — JWT Auth Demo", page_icon="🦅", layout="wide")

st.title("ITIS — Login (JWT)")

def api_post(path: str, payload: dict):
    url = f"{BACKEND_URL}{path}"
    headers = {}
    if st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    with httpx.Client(timeout=8.0) as c:
        r = c.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()

def api_get(path: str):
    url = f"{BACKEND_URL}{path}"
    headers = {}
    if st.session_state.access_token:
        headers["Authorization"] = f"Bearer {st.session_state.access_token}"
    with httpx.Client(timeout=8.0) as c:
        r = c.get(url, headers=headers)
        r.raise_for_status()
        return r.json()

# Login form
with st.form("login"):
    st.subheader("Sign in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Sign in")
    if submitted:
        try:
            # backend expects form or JSON; here we send JSON
            resp = api_post("/auth/token", {"username": username, "password": password})
            token = resp.get("access_token")
            if token:
                st.session_state.access_token = token
                st.success("Signed in successfully.")
                # fetch current user
                me = api_get("/auth/me")
                st.session_state.user = me.get("user")
                st.experimental_rerun()
            else:
                st.error("Login failed: no token returned.")
        except Exception as e:
            st.error(f"Login error: {e}")
            logger.exception("Login failed")

if st.session_state.user:
    st.markdown(f"**Signed in as:** `{st.session_state.user.get('username')}` — role: `{st.session_state.user.get('role')}`")
    if st.button("Sign out"):
        st.session_state.access_token = None
        st.session_state.user = None
        st.experimental_rerun()

# Example protected action
st.header("Demo: Create instruction (requires auth)")
if st.session_state.access_token:
    txid = st.text_input("Transaction ID", value=f"TRX-{int(time.time())}")
    amount = st.number_input("Amount", value=1250.75, format="%.2f")
    if st.button("Create instruction"):
        try:
            payload = {"transaction_id": txid, "amount": float(amount), "currency": "USD", "beneficiary_account": "QNB-ACC-0001"}
            resp = api_post("/v1/settlement/instructions", payload)
            st.success("Instruction created.")
            st.json(resp)
        except Exception as e:
            st.error(f"API error: {e}")
else:
    st.info("Sign in to perform actions.")

st.markdown("---")
st.markdown("Backend URL: " + BACKEND_URL)
