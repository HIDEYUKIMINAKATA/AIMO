# memory/context/context_stacker.py

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.insert(0, AIMO_ROOT)

from core.path_utils import find_aimo_root
from core.logger import log_event
from memory.context.semantic_context_builder import get_relevant_contexts
from memory.context.prompt_builder import build_prompt

AIMO_ROOT = find_aimo_root()

def stack_context_for_prompt(input_text: str, top_k: int = 3, threshold: float = 0.4) -> dict:
    """
    現在の入力に対して、意味的に近い文脈を動的に抽出し、プロンプト形式に再構成する。
    """
    log_event("=== Context Stacker Start ===", "INFO")
    try:
        # 🧠 意味的に近い文脈の抽出
        context_segments = get_relevant_contexts(input_text, top_k=top_k, threshold=threshold)

        log_event(f"Context segments extracted: {len(context_segments)}", "INFO")

        # 🛠 プロンプトの再構成
        final_prompt = build_prompt(context_segments, input_text)

        log_event("Prompt constructed successfully", "SUCCESS")

        return {
            "context_segments": context_segments,
            "final_prompt": final_prompt
        }

    except Exception as e:
        log_event(f"Context stacking failed: {e}", "ERROR")
        return {
            "context_segments": [],
            "final_prompt": input_text
        }
