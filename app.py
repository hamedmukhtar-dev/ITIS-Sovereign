# app.py
import os
import time
import json
from typing import Dict, Optional
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS

# Optional: requests is used for proxying streaming to OpenAI if you prefer raw HTTP.
# You can instead use the openai-python library (pip install openai) — example below uses requests.
import requests

app = Flask(__name__)
CORS(app)

# Configuration: set these in your environment (or .env) in production.
PORT = int(os.environ.get("PORT", 4000))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # keep secret, server-side only
BACKEND_BASE = os.environ.get("BACKEND_BASE", "")  # unused in this file, for frontend config

# Mock fixtures (simple). Replace or extend with a JSON file if you like.
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


@app.route("/api/signed-url")
def signed_url():
    """
    Return a signed URL for a given file key.
    In production, replace this logic to call your cloud provider (e.g., boto3.generate_presigned_url).
    """
    key = request.args.get("key", "")
    if not key:
        return jsonify({"error": "missing key parameter"}), 400

    url = MOCK_DATA["signedUrls"].get(key)
    if url:
        return jsonify({"url": url})

    # Default fallback (non-signed placeholder)
    fallback = f"https://example.com/files/{key}"
    return jsonify({"url": fallback})


@app.route("/api/ai-chat", methods=["POST"])
def ai_chat():
    """
    Non-streaming chat endpoint. Body: { "message": "..." }
    If OPENAI_API_KEY is set, will call OpenAI (non-streaming). Otherwise uses mock replies.
    """
    body = request.get_json(silent=True) or {}
    message = (body.get("message") or "").strip()

    if not message:
        return jsonify({"error": "message required"}), 400

    # If no OpenAI key, return deterministic mock reply if available.
    if not OPENAI_API_KEY:
        reply = MOCK_DATA["replies"].get(message.lower(), MOCK_DATA["defaultReply"])
        return jsonify({"reply": reply})

    # If OpenAI key present, proxy request to OpenAI Chat Completions (non-streaming)
    # NOTE: choose model according to your subscription/compatibility.
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4o-mini",  # change as appropriate; ensure model available to your key
            "messages": [{"role": "user", "content": message}],
            "temperature": 0.2,
            "max_tokens": 800,
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # extract reply safely:
        reply = None
        if isinstance(data, dict):
            # standard Chat Completions shape:
            choices = data.get("choices") or []
            if choices:
                msg = choices[0].get("message") or {}
                reply = msg.get("content")
            # Sometimes 'choices[0].text' for older endpoints:
            if not reply and choices and "text" in choices[0]:
                reply = choices[0]["text"]
        if not reply:
            reply = MOCK_DATA["defaultReply"]
        return jsonify({"reply": reply})
    except Exception as e:
        app.logger.exception("OpenAI request failed")
        return jsonify({"error": "AI service error", "detail": str(e)}), 500


def sse_pack(event: Optional[str], data: Dict):
    """
    Pack a Python object (data) into an SSE message.
    """
    payload = json.dumps(data, ensure_ascii=False)
    if event:
        return f"event: {event}\ndata: {payload}\n\n"
    return f"data: {payload}\n\n"


@app.route("/api/ai-chat-stream")
def ai_chat_stream():
    """
    SSE streaming endpoint. If OPENAI_API_KEY present, attempt to stream from OpenAI and re-emit as SSE.
    Otherwise emit a mock sequence of messages (useful for local dev).
    Client receives text/event-stream SSE events with JSON payloads: { "text": "..." }
    """

    # For local/dev: if no message param, fallback to a default demo.
    user_message = request.args.get("message", "stream demo")

    def generate_mock():
        lines = [
            "مرحبًا — هذا مثال للبث المباشر.",
            "أعمل على تلخيص العرض...",
            "النقطة الأولى: جاهزية تقنية.",
            "النقطة الثانية: التكامل مع البنوك المحلية.",
            "انتهى البث."
        ]
        for line in lines:
            yield sse_pack(None, {"text": line})
            time.sleep(0.3)
        # final event
        yield sse_pack("done", {"done": True})

    if not OPENAI_API_KEY:
        # Return mocked SSE stream for local dev
        return Response(stream_with_context(generate_mock()), content_type="text/event-stream")

    # If OpenAI configured, create a streaming request and re-emit chunks.
    # WARNING: this is a simple proxy implementation. For production you may want to:
    #  - Use websockets for two-way comms.
    #  - Add auth, rate limiting, batching, and robust error handling.
    def stream_from_openai():
        # Using the Chat Completions streaming endpoint
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4o-mini",  # change to a model available to your key
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.2,
            "stream": True,
        }

        try:
            with requests.post(url, headers=headers, json=payload, stream=True, timeout=60) as r:
                r.raise_for_status()
                buffer = ""
                # OpenAI stream sends lines prefixed with "data: "
                for raw in r.iter_lines(decode_unicode=True):
                    if raw is None:
                        continue
                    if not raw:
                        continue
                    line = raw.strip()
                    # skip keep-alive
                    if line == "" or line == "data: [DONE]":
                        continue
                    if line.startswith("data:"):
                        data_str = line[len("data:"):].strip()
                    else:
                        data_str = line
                    # try to parse JSON chunk
                    try:
                        chunk = json.loads(data_str)
                    except Exception:
                        # not JSON — send raw as text
                        yield sse_pack(None, {"text": data_str})
                        continue

                    # typical structure: { "choices": [ { "delta": { "content": "..." } } ] }
                    choices = chunk.get("choices") or []
                    if choices:
                        delta = choices[0].get("delta", {})
                        content_piece = delta.get("content")
                        if content_piece:
                            yield sse_pack(None, {"text": content_piece})
                    # handle finalization
                    if chunk.get("id") and chunk.get("object") == "chat.completion":
                        # optional additional handling
                        pass
                # final event
                yield sse_pack("done", {"done": True})
        except Exception as exc:
            app.logger.exception("Error streaming from OpenAI")
            # Inform client of error
            yield sse_pack("error", {"error": str(exc)})
            # close stream
            yield sse_pack("done", {"done": True})

    return Response(stream_with_context(stream_from_openai()), content_type="text/event-stream")


if __name__ == "__main__":
    print(f"Starting mock/production-capable server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
