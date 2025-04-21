# ai_nodes/zephyr_handler.py

import os
import json
import time
import requests
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

ROOT = find_aimo_root()
KEY_PATH = os.path.join(ROOT, "api_keys", "imagegen_key.txt")
ZEPHYR_ENDPOINT = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

def _load_key():
    try:
        with open(KEY_PATH, encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) < 2:
                log_event("ERROR", "Zephyr key must be in second line of imagegen_key.txt")
                return None
            return lines[1]
    except FileNotFoundError:
        log_event("ERROR", f"Key file not found: {KEY_PATH}")
        return None

ZEPHYR_KEY = _load_key()

def generate_text(prompt: str, max_tokens: int = 512, temperature: float = 0.7, timeout: int = 60) -> str:
    if ZEPHYR_KEY is None:
        return "[ERROR] Zephyr API key is missing."

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
        start_time = time.time()
        response = requests.post(ZEPHYR_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=timeout)
        elapsed = time.time() - start_time

        if response.status_code != 200:
            log_event("ERROR", f"Zephyr failed: {response.status_code} - {response.text[:200]}")
            return f"[ERROR] Zephyr HTTP {response.status_code}"

        result = response.json()
        text = result[0]["generated_text"] if isinstance(result, list) else str(result)
        log_event("SUCCESS", f"Zephyr response received in {elapsed:.2f}s")
        return text
    except requests.exceptions.Timeout:
        log_event("ERROR", "Zephyr request timed out.")
        return "[ERROR] Zephyr timeout"
    except Exception as e:
        log_event("ERROR", f"Zephyr request exception: {e}")
        return f"[ERROR] Zephyr {e}"
