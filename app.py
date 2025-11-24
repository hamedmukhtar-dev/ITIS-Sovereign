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
st.markdown(
    """
<style>
    body, .stApp { background-color: #000000 !important; col
