"""hf_text_handler.py – Zephyr (HuggingFace) text generation handler.

Requirements:
- Reads Zephyr API key from second line of api_keys/imagegen_key.txt
- 60‑second timeout
- log_event() instrumentation
"""
import os
import json
import time
import requests
import pathlib
from typing import Optional

try:
    from core.logger import log_event
    from core.find_aimo_root import find_aimo_root
except ImportError:
    def log_event(level, message): print(f'[{level}] {message}')
    def find_aimo_root(): return pathlib.Path(__file__).resolve().parent

# === 初期設定 ===
ROOT = find_aimo_root()
KEY_PATH = os.path.join(ROOT, 'api_keys', 'imagegen_key.txt')
MODEL_ENDPOINT = 'https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta'

# === APIキー読み込み ===
def _load_key() -> Optional[str]:
    if not os.path.exists(KEY_PATH):
        log_event("ERROR", f"Zephyr key file not found: {KEY_PATH}")
        return None
    with open(KEY_PATH, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) < 2:
        log_event("ERROR", "Zephyr key expected on second line but not present")
        return None
    return lines[1]

ZEPHYR_KEY = _load_key()

# === メイン関数 ===
def generate_text(prompt: str, max_tokens: int = 512, temperature: float = 0.7, timeout: int = 60) -> str:
    """Send prompt to Zephyr via HuggingFace Inference API"""
    if ZEPHYR_KEY is None:
        return "[ERROR] Zephyr key missing."

    headers = {
        "Authorization": f"Bearer {ZEPHYR_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature
        }
    }

    log_event("INFO", f"Zephyr request | len(prompt)={len(prompt)}")
    try:
        start = time.time()
        response = requests.post(MODEL_ENDPOINT, headers=headers, json=payload, timeout=timeout)
        elapsed = time.time() - start

        if response.status_code != 200:
            log_event("ERROR", f"Zephyr HTTP {response.status_code}: {response.text[:200]}")
            return f"[ERROR] Zephyr HTTP {response.status_code}"

        data = response.json()
        text = data[0].get("generated_text", "") if isinstance(data, list) else str(data)
        log_event("SUCCESS", f"Zephyr response ok | {elapsed:.2f}s")
        return text

    except requests.exceptions.Timeout:
        log_event("ERROR", "Zephyr request timed out after 60s")
        return "[ERROR] Zephyr timeout (60s)"
    except Exception as e:
        log_event("ERROR", f"Zephyr request failed: {e}")
        return f"[ERROR] Zephyr {e}"
