
"""
route_ai.py
AIMO v2.2.10 – S2: AIルーティング構成（最新版）

優先順位: Mixtral → Zephyr → Claude → GPT → Gemini → Summarizer
画像プロンプト → image_handler に、音声プロンプト → voice_handler に、
マルチモーダルプロンプト（画像+テキスト） → cogvlm_handler にルーティング
"""

import importlib
import os
import time
from datetime import datetime
from typing import Callable, Dict, Optional

# 特別ルーティング（直接 import）
from ai_nodes.image_handler import generate_image as imagegen
from ai_nodes.voice_handler import generate_voice as voicegen
from ai_nodes.cogvlm_handler import generate_multimodal as multimodalgen

from core.find_aimo_root import find_aimo_root
from core.logger import log_event

ROOT = find_aimo_root()

PRIORITY = [
    ("Mixtral",     "ai_nodes.mixtral_handler",     "generate_text"),
    ("Zephyr",      "ai_nodes.zephyr_handler",      "generate_text"),
    ("Claude",      "ai_nodes.claude_handler",      "generate_text"),
    ("GPT",         "ai_nodes.gpt_handler",         "generate_text"),
    ("Gemini",      "ai_nodes.gemini_handler",      "generate_text"),
    ("Summarizer",  "ai_nodes.summarizer_hub",      "summarize_text"),
]

TIMEOUT_SEC = 60

class HandlerWrapper:
    def __init__(self, name: str, fn: Callable[[str], str]):
        self.name = name
        self.fn = fn

    def __call__(self, prompt: str) -> str:
        start = time.time()
        try:
            resp = self.fn(prompt)
            elapsed = time.time() - start
            log_event("[SUCCESS]", f"{self.name} responded in {elapsed:.2f}s", category="route")
            return resp
        except Exception as e:
            log_event("[ERROR]", f"{self.name} failed: {e}", category="route")
            raise

def _load_handlers() -> Dict[str, HandlerWrapper]:
    handlers = {}
    for name, module_path, attr in PRIORITY:
        try:
            module = importlib.import_module(module_path)
            fn = getattr(module, attr)
            handlers[name] = HandlerWrapper(name, fn)
            log_event("[INFO]", f"Handler loaded: {name} ({module_path}.{attr})", category="route")
        except Exception as e:
            log_event("[WARN]", f"Handler unavailable: {name} ({e})", category="route")
    return handlers

_HANDLERS = _load_handlers()

def route(prompt: str) -> str:
    prompt = prompt.strip()
    if prompt.startswith("画像"):
        log_event("[INFO]", "画像プロンプト検出 → imagegen にルーティング", category="route")
        return imagegen(prompt.replace("画像", "").strip())
    elif prompt.startswith("音声"):
        log_event("[INFO]", "音声プロンプト検出 → voicegen にルーティング", category="route")
        return voicegen(prompt.replace("音声", "").strip())
    elif prompt.startswith("統合") or prompt.startswith("画像理解"):
        log_event("[INFO]", "マルチモーダルプロンプト検出 → multimodalgen にルーティング", category="route")
        return multimodalgen(prompt.replace("統合", "").replace("画像理解", "").strip())

    log_event("[INFO]", f"Routing started | prompt head: {prompt[:30]}", category="route")
    last_err: Optional[Exception] = None
    for name, _mod, _attr in PRIORITY:
        if name not in _HANDLERS:
            continue
        handler = _HANDLERS[name]
        try:
            return handler(prompt)
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"All handlers failed: {last_err}") from last_err

if __name__ == "__main__":
    import sys
    test_prompt = sys.argv[1] if len(sys.argv) > 1 else "画像 サングラスをかけた猫"
    try:
        out = route(test_prompt)
        print(out)
    except Exception as exc:
        print("[FATAL]", exc)
