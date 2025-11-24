# app.py
import os
import time
import json
import requests
import streamlit as st

# Optional: OpenAI streaming if OPENAI_API_KEY present
try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

st.set_page_config(page_title="Dara Investor Platform", layout="wide")

# ---------- Configuration ----------
BACKEND_BASE = os.environ.get("REACT_APP_BACKEND_BASE", os.environ.get("BACKEND_BASE", ""))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)

if OPENAI_API_KEY and OPENAI_AVAILABLE:
    openai.api_key = OPENAI_API_KEY

# Mock fixtures (fallback)
MOCK_DATA = {
    "signedUrls": {
        "Master_Investor_Deck.pptx": "https://example.com/files/Master_Investor_Deck.pptx",
        "Dara_Investment_Files.zip": "https://example.com/files/Dara_Investment_Files.zip",
        "KYC_Initiative.pdf": "https://example.com/files/KYC_Initiative.pdf"
    },
    "replies": {
        "hello": "أهلًا! كيف أستطيع مساعدتك بخصوص المشروعات؟",
        "summarize master": "الملف الرئيسي يتضمن خطة نمو 3 سنوات، توافق مع IATA، وخطة دمج محفظة دفع محلية."
    },
    "defaultReply": "مرحبًا — هذه إجابة تجريبية من الخادم المحلي."
}

BRAND = {"name": "Dara"}

initial_projects = [
    {
        "id": "kyc",
        "title": "KYC Initiative",
        "tagline": "AI-Enhanced Sudan Digital Identity",
        "description": "نظام KYC رقمي مدعوم بالذكاء الاصطناعي للتحقق البيومتري، تحليل المخاطر، وربط المستخدمين بالمؤسسات المالية.",
        "files": [{"name": "KYC_Initiative.pdf", "key": "KYC_Initiative.pdf"}],
        "tags": ["KYC", "AI", "Compliance"],
    },
    {
        "id": "dara-plan",
        "title": "Dara Business Plan",
        "tagline": "TravelTech + AI Business Plan",
        "description": "خطة عمل كاملة لشركة دارا تتضمن الرؤية، السوق، نموذج الإيرادات، وخطة التوسع 2025-2027.",
        "files": [{"name": "Dara_BusinessPlan.pdf", "key": "Dara_BusinessPlan.pdf"}],
        "tags": ["Business Plan", "Strategy"],
    },
    {
        "id": "master",
        "title": "Master Investor Deck",
        "tagline": "All Projects - One Investor Package",
        "description": "الحزمة الاستثمارية الكاملة: كل المشاريع + ملخص الاستثمار وAI Integration.",
        "files": [{"name": "Master_Investor_Deck.pptx", "key": "Master_Investor_Deck.pptx"}],
        "tags": ["Master", "All"],
    },
]

# ---------- Session state ----------
if "chat_lines" not in st.session_state:
    st.session_state.chat_lines = [{"from": "system", "text": "مرحبًا بك في منصة المستثمر — اسألني عن أي مشروع."}]
if "lang" not in st.session_state:
    st.session_state.lang = "ar"
if "query" not in st.session_state:
    st.session_state.query = ""
if "active_tags" not in st.session_state:
    st.session_state.active_tags = []
if "projects" not in st.session_state:
    st.session_state.projects = initial_projects

# ---------- Helpers ----------
def get_signed_url(key: str):
    """Resolve a file key to a URL using BACKEND_BASE or MOCK_DATA fallback."""
    if not key:
        return None
    # Try backend first
    if BACKEND_BASE:
        try:
            resp = requests.get(f"{BACKEND_BASE.rstrip('/')}/api/signed-url", params={"key": key}, timeout=6)
            if resp.ok:
                j = resp.json()
                return j.get("url")
        except Exception:
            pass
    return MOCK_DATA["signedUrls"].get(key) or f"https://example.com/files/{key}"


def ai_reply_sync(message: str):
    """Non-streaming reply: use OpenAI if available, otherwise mock."""
    if OPENAI_API_KEY and OPENAI_AVAILABLE:
        try:
            # Using chat completion (non-streaming)
            res = openai.ChatCompletion.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role":"user", "content": message}],
                temperature=0.2,
                max_tokens=800,
            )
            # Extract text safely
            choices = res.get("choices", [])
            if choices:
                msg = choices[0].get("message") or {}
                return msg.get("content") or choices[0].get("text") or MOCK_DATA["defaultReply"]
            return MOCK_DATA["defaultReply"]
        except Exception:
            st.error("OpenAI request failed (check logs). Using mock reply.")
            return MOCK_DATA["replies"].get(message.lower(), MOCK_DATA["defaultReply"])
    else:
        return MOCK_DATA["replies"].get(message.lower(), MOCK_DATA["defaultReply"])


def ai_reply_stream(message: str, placeholder):
    """
    Stream reply from OpenAI if available. Updates 'placeholder' with progressive text.
    Returns the full final string.
    """
    if not (OPENAI_API_KEY and OPENAI_AVAILABLE):
        # simulate streaming with mock lines
        lines = [
            "مرحبًا — هذا مثال للبث المباشر.",
            "أعمل على تلخيص العرض...",
            "النقطة الأولى: جاهزية تقنية.",
            "النقطة الثانية: التكامل مع البنوك المحلية.",
            "انتهى البث."
        ]
        full = ""
        for ln in lines:
            full += ln + "\n"
            placeholder.markdown(full)
            time.sleep(0.3)
        return full

    # Real OpenAI streaming
    try:
        stream = openai.ChatCompletion.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role":"user","content":message}],
            temperature=0.2,
            stream=True,
        )
        full = ""
        for chunk in stream:
            # chunk may contain choices with delta
            choices = chunk.get("choices", [])
            if choices:
                delta = choices[0].get("delta", {})
                content = delta.get("content")
                if content:
                    full += content
                    placeholder.markdown(full)
        return full
    except Exception:
        st.error("Stream from OpenAI failed — falling back to sync.")
        return ai_reply_sync(message)

# ---------- UI Layout ----------
col1, col2 =
