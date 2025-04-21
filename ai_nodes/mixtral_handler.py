"""
mixtral_handler.py - OpenRouter 経由で Mixtral API を呼び出す本格版ハンドラー（拡張対応版）
"""

import os, requests, json, time
from typing import Optional

from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from dotenv import load_dotenv

# ✅ .env 読み込み（明示ログ付き）
ROOT = find_aimo_root()
ENV_PATH = os.path.join(ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH)
log_event("[INFO]", f".env 読み込み完了（path: {ENV_PATH}）", category="mixtral")

# ✅ APIキーとエンドポイント
API_KEY = os.getenv("MIXTRAL_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_text(prompt: str, max_tokens: int = 512, temperature: float = 0.7, timeout: int = 60) -> str:
    """OpenRouter 経由で Mixtral モデルを実行し応答を返す"""
    if API_KEY is None:
        log_event("[ERROR]", "Mixtral APIキーが未定義です", category="mixtral")
        return "[ERROR] Mixtral APIキーが未定義です"

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    log_event("[INFO]", f"Mixtral request | len(prompt)={len(prompt)}", category="mixtral")

    try:
        start = time.time()
        resp = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload), timeout=timeout)
        elapsed = time.time() - start
        resp.raise_for_status()

        result = resp.json()
        content = result["choices"][0]["message"]["content"]
        log_event("[SUCCESS]", f"Mixtral response received in {elapsed:.2f}s", category="mixtral")
        return content

    except requests.exceptions.Timeout:
        log_event("[ERROR]", f"Mixtralタイムアウト発生（{timeout}s）", category="mixtral")
        return f"[ERROR] Mixtralタイムアウト発生（{timeout}s）"

    except Exception as e:
        log_event("[ERROR]", f"Mixtral呼び出し失敗: {e}", category="mixtral")
        return f"[ERROR] Mixtral呼び出し失敗: {e}"
