"""
gpt_handler.py – OpenAI GPT-3.5/4 テキスト生成ハンドラ

要件:
- OpenAI API key を api_keys/openai_key.txt の1行目から読み取る
- モデル選択: "gpt-4" または "gpt-3.5-turbo"
- タイムアウト: 60秒
- log_event() による全ログ出力
"""

import os, openai, pathlib, time
from typing import Optional

try:
    from core.logger import log_event, find_aimo_root
except ImportError:
    def log_event(level, message): print(f"[{level}] {message}")
    def find_aimo_root(): return pathlib.Path(__file__).resolve().parent

# 初期化
ROOT = find_aimo_root()
KEY_PATH = os.path.join(ROOT, 'api_keys', 'openai_key.txt')

# 🔑 APIキーの読み取り
def _load_key() -> Optional[str]:
    if not os.path.exists(KEY_PATH):
        log_event("ERROR", f"OpenAI key file not found: {KEY_PATH}")
        return None
    with open(KEY_PATH, encoding="utf-8") as f:
        key = f.readline().strip()
    if not key:
        log_event("ERROR", "OpenAI key is empty")
        return None
    return key

API_KEY = _load_key()
if API_KEY:
    openai.api_key = API_KEY
else:
    log_event("ERROR", "OpenAI APIキーの設定に失敗しました。")

# モデル指定（必要に応じて切替可能）
MODEL_NAME = "gpt-4"  # または "gpt-3.5-turbo"

# 🔁 メイン関数
def generate_text(prompt: str, model: str = MODEL_NAME, timeout: int = 60) -> str:
    if API_KEY is None:
        return "[ERROR] OpenAI APIキーが未定義です。"

    log_event("INFO", f"GPTリクエスト開始 | モデル: {model} | プロンプト長: {len(prompt)}")
    try:
        start = time.time()
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
            timeout=timeout,
        )
        elapsed = time.time() - start
        text = response.choices[0].message['content'].strip()
        log_event("SUCCESS", f"GPT応答受信 | 所要時間: {elapsed:.2f}s")
        return text
    except openai.error.Timeout:
        log_event("ERROR", "GPTリクエストがタイムアウトしました。")
        return "[ERROR] GPTタイムアウト"
    except Exception as e:
        log_event("ERROR", f"GPTリクエスト失敗: {e}")
        return f"[ERROR] GPTリクエスト失敗: {e}"

# 🔧 テスト実行（単体で実行時）
if __name__ == "__main__":
    test_prompt = "こんにちは。あなたは誰ですか？"
    print(generate_text(test_prompt))
