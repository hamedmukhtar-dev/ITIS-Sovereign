# app.py
# Fixed: unterminated string literal in ai_reply_stream mock; added CLI/test-mode improvements.
"""
Dara Investor Platform - Streamlit app with graceful fallback for non-Streamlit environments.

This file was rewritten to handle the case where the sandbox (or runtime) does not have
`streamlit` installed (ModuleNotFoundError). Behavior:

- If `streamlit` is available, the full interactive app runs as before.
- If `streamlit` is NOT available, the script runs in a CLI/test mode that exercises the
  important helper functions (get_signed_url, ai_reply_sync, ai_reply_stream mock) so you can
  validate logic in environments without Streamlit.

To deploy on share.streamlit.io, ensure `streamlit` is present in `requirements.txt` and push
this file to your GitHub repo under e.g. `streamlit_app/app.py`.

"""
import os
import time
import json
import requests
from typing import Optional

# Try to import Streamlit — if missing, we fall back to CLI/test mode.
try:
    import streamlit as st
    ST_AVAILABLE = True
except Exception:
    ST_AVAILABLE = False

# Optional: OpenAI streaming if OPENAI_API_KEY present
try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

# ---------- Configuration ----------
BACKEND_BASE = os.environ.get("REACT_APP_BACKEND_BASE", os.environ.get("BACKEND_BASE", ""))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if ST_AVAILABLE:
    # If running in Streamlit, secrets may contain the key
    OPENAI_API_KEY = OPENAI_API_KEY or st.secrets.get("OPENAI_API_KEY", None)

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

# ---------- Helpers ----------
def get_signed_url(key: str) -> Optional[str]:
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
            # network issues or backend unavailable — fall back to mock
            pass
    return MOCK_DATA["signedUrls"].get(key) or f"https://example.com/files/{key}"


def ai_reply_sync(message: str) -> str:
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
        except Exception as e:
            # Log to console in CLI mode; in Streamlit show error
            if ST_AVAILABLE:
                st.error("OpenAI request failed (check logs). Using mock reply.")
            else:
                print("OpenAI request failed:", e)
            return MOCK_DATA["replies"].get(message.lower(), MOCK_DATA["defaultReply"])
    else:
        return MOCK_DATA["replies"].get(message.lower(), MOCK_DATA["defaultReply"])


def ai_reply_stream(message: str, consumer) -> str:
    """
    Stream reply from OpenAI if available. 'consumer' is a callable receiving the growing text.
    If streaming isn't possible, we simulate streaming using mock lines and call consumer progressively.
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
            # fixed: ensure newline is concatenated correctly
            full += ln + "
"
            try:
                consumer(full)
            except Exception:
                pass
            time.sleep(0.25)
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
            choices = chunk.get("choices", [])
            if choices:
                delta = choices[0].get("delta", {})
                content = delta.get("content")
                if content:
                    full += content
                    try:
                        consumer(full)
                    except Exception:
                        pass
        return full
    except Exception as e:
        if ST_AVAILABLE:
            st.error("Stream from OpenAI failed — falling back to sync.")
        else:
            print("Stream from OpenAI failed:", e)
        return ai_reply_sync(message)


# ---------- Streamlit App (only if available) ----------
if ST_AVAILABLE:
    st.set_page_config(page_title="Dara Investor Platform", layout="wide")

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

    # UI Layout
    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(f"{BRAND['name']} — Investor Platform")
        st.write("حزمة العرض الاستثمارية • جاهزة للمستثمرين" if st.session_state.lang == "ar" else "Investor package • ready for meetings")

        # Search + tags
        q = st.text_input("ابحث عن مشروع أو وصف..." if st.session_state.lang == "ar" else "Search project or description...", value=st.session_state.query)
        st.session_state.query = q

        # tags
        all_tags = sorted({t for p in st.session_state.projects for t in p["tags"]})
        tag_cols = st.columns(len(all_tags) or 1)
        for i, tag in enumerate(all_tags):
            pressed = tag in st.session_state.active_tags
            if tag_cols[i].button(tag if not pressed else f"✓ {tag}"):
                if pressed:
                    st.session_state.active_tags.remove(tag)
                else:
                    st.session_state.active_tags.append(tag)

        # Filtered projects
        def matches(p):
            q = st.session_state.query.strip().lower()
            if q and not (q in p["title"].lower() or q in p["description"].lower()):
                return False
            if st.session_state.active_tags and not all(t in p["tags"] for t in st.session_state.active_tags):
                return False
            return True

        filtered = [p for p in st.session_state.projects if matches(p)]

        # Projects grid
        for p in filtered:
            with st.container():
                st.subheader(p["title"])
                st.caption(" • ".join(p["tags"]))
                st.write(p["tagline"])
                st.write(p["description"])
                file_buttons = []
                for f in p["files"]:
                    url = get_signed_url(f.get("key") or f.get("url") or "")
                    file_buttons.append((f["name"], url))
                cols = st.columns(len(file_buttons) or 1)
                for i, (fname, furl) in enumerate(file_buttons):
                    if cols[i].button("تحميل" if st.session_state.lang == "ar" else "Download", key=f"{p['id']}-{fname}"):
                        if furl:
                            st.write(f"[فتح الملف]({furl})")
                            st.experimental_set_query_params()
                        else:
                            st.error("File URL not available.")

    with col2:
        # Language toggle + quick links + AI panel
        lang_col1, lang_col2 = st.columns(2)
        if lang_col1.button("العربية"):
            st.session_state.lang = "ar"
        if lang_col2.button("English"):
            st.session_state.lang = "en"

        st.markdown("---")
        st.subheader("AI Assistant" if st.session_state.lang == "en" else "مساعد الذكاء الاصطناعي")
        chat_box = st.empty()
        # Render chat lines
        with chat_box.container():
            for c in st.session_state.chat_lines:
                if c["from"] == "system":
                    st.markdown(f"<div style='color:gray;font-size:12px'>{c['text']}</div>", unsafe_allow_html=True)
                elif c["from"] == "user":
                    st.markdown(f"<div style='text-align:right;background-color:#e6f2ff;padding:6px;border-radius:6px'>{c['text']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align:left;background-color:#f7f7f7;padding:6px;border-radius:6px'>{c['text']}</div>", unsafe_allow_html=True)

        user_message = st.text_input("اسأل المساعد..." if st.session_state.lang == "ar" else "Ask the assistant...")

        col_send1, col_send2 = st.columns([3, 1])
        with col_send2:
            if st.button("أرسل" if st.session_state.lang == "ar" else "Send"):
                if user_message.strip():
                    st.session_state.chat_lines.append({"from": "user", "text": user_message})
                    placeholder = st.empty()
                    st.session_state.chat_lines.append({"from": "assistant", "text": "..."})
                    # update display immediately
                    # streaming experience:
                    final = ai_reply_stream(user_message, lambda txt: placeholder.markdown(txt))
                    # replace the assistant placeholder (last) with final
                    if st.session_state.chat_lines and st.session_state.chat_lines[-1].get("text") == "...":
                        st.session_state.chat_lines[-1] = {"from": "assistant", "text": final}
                    else:
                        st.session_state.chat_lines.append({"from": "assistant", "text": final})
                    # re-render chat box
                    chat_box.empty()
                    with chat_box.container():
                        for c in st.session_state.chat_lines:
                            if c["from"] == "system":
                                st.markdown(f"<div style='color:gray;font-size:12px'>{c['text']}</div>", unsafe_allow_html=True)
                            elif c["from"] == "user":
                                st.markdown(f"<div style='text-align:right;background-color:#e6f2ff;padding:6px;border-radius:6px'>{c['text']}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div style='text-align:left;background-color:#f7f7f7;padding:6px;border-radius:6px'>{c['text']}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.write("روابط سريعة" if st.session_state.lang == "ar" else "Quick links")
        if st.button("تحميل الحزمة الكاملة (ZIP)" if st.session_state.lang == "ar" else "Download full package"):
            url = get_signed_url("Dara_Investment_Files.zip")
            st.write(f"[فتح الحزمة]({url})")
        if st.button("تحميل Master Deck" if st.session_state.lang == "ar" else "Download Master Deck"):
            url = get_signed_url("Master_Investor_Deck.pptx")
            st.write(f"[فتح الملف]({url})")

    st.markdown("---")
    st.caption(f"Prepared with AI • Last updated: {time.strftime('%Y-%m-%d')}")


# ---------- CLI / Test mode (when Streamlit is not available) ----------
else:
    def _print_header():
        print("Dara Investor Platform - CLI test mode")
        print("Streamlit not found in the environment. To run the interactive app, install streamlit and run:")
        print("  pip install streamlit")
        print("  streamlit run app.py")
        print()

    def _cli_consumer(text: str):
        # simple consumer for ai_reply_stream in CLI test mode
        # clear the terminal-ish by printing separators
        print("---- partial reply ----")
        print(text)
        print("-----------------------")

    def _run_tests():
        _print_header()
        # Test 1: signed URL resolution
        print("Test: get_signed_url('Master_Investor_Deck.pptx') ->")
        print(get_signed_url('Master_Investor_Deck.pptx'))
        print()

        # Test 2: ai_reply_sync with known and unknown prompts
        print("Test: ai_reply_sync('hello') ->")
        print(ai_reply_sync('hello'))
        print()
        print("Test: ai_reply_sync('something else') ->")
        print(ai_reply_sync('something else'))
        print()

        # Test 3: ai_reply_stream (mock streaming)
        print("Test: ai_reply_stream('summarize master') streaming ->")
        res = ai_reply_stream('summarize master', _cli_consumer)
        print("FINAL STREAM RESULT:
", res)
        print()

        # Sanity test: ensure projects list exists and is iterable
        print("Projects loaded:")
        for p in initial_projects:
            print(f" - {p['id']}: {p['title']}")

    if __name__ == '__main__':
        _run_tests()
