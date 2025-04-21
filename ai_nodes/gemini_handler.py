"""
gemini_handler.py - Gemini Free API (via Google AI Studio) 本格版ハンドラー

- 認証：.env の GEMINI_API_KEY を使用
- タイムアウト：60秒
- ログ：log_event による [INFO], [SUCCESS], [ERROR] 出力
"""

import os
import requests
from dotenv import load_dotenv
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

ROOT = find_aimo_root()
ENV_PATH = os.path.join(ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

def generate_text(prompt: str) -> str:
    log_event("INFO", f"Gemini API呼び出し中... | prompt head: {prompt[:30]}", category="gemini")

    if not API_KEY:
        log_event("ERROR", ".envファイルに GEMINI_API_KEY が定義されていません", category="gemini")
        return "[ERROR] Gemini APIキーが未定義です"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if not content:
            log_event("ERROR", "Gemini応答に有効なテキストが含まれていません", category="gemini")
            return "[ERROR] Gemini応答が不完全です"

        log_event("SUCCESS", "Gemini 応答受信", category="gemini")
        return content

    except requests.exceptions.Timeout:
        log_event("ERROR", "Geminiリクエストがタイムアウトしました（60秒）", category="gemini")
        return "[ERROR] Geminiリクエストがタイムアウトしました"

    except Exception as e:
        log_event("ERROR", f"Gemini呼び出し失敗: {e}", category="gemini")
        return f"[ERROR] Gemini失敗: {e}"
