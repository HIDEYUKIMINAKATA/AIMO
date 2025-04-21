"""
annotated_log.py - AIMO annotated モジュール（注釈付きAIログ）

目的：
- AIの出力に対して注釈・改善案・意図などを記録
- 学習・改善・人間レビュー用に活用
"""

import json
from datetime import datetime
from pathlib import Path
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

ANNOTATED_DIR = Path(find_aimo_root()) / "memory" / "annotated"
ANNOTATED_FILE = ANNOTATED_DIR / "annotated_logs.jsonl"
ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)

def annotate_response(prompt: str, response: str, annotation: str, reviewer: str = "human") -> None:
    """
    注釈付きのAI応答を保存
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response,
        "annotation": annotation,
        "reviewer": reviewer
    }

    try:
        with open(ANNOTATED_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log_event("[SUCCESS]", "注釈付きログ保存", category="annotated")
    except Exception as e:
        log_event("[ERROR]", f"注釈ログ保存失敗: {e}", category="annotated")

def load_annotated_logs() -> list:
    """
    注釈付きログを全件取得
    """
    if not ANNOTATED_FILE.exists():
        return []

    try:
        with open(ANNOTATED_FILE, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
        log_event("[INFO]", f"{len(lines)} 件の注釈ログ読み込み", category="annotated")
        return lines
    except Exception as e:
        log_event("[ERROR]", f"注釈ログ読み込み失敗: {e}", category="annotated")
        return []

# CLI確認用
if __name__ == "__main__":
    annotate_response(
        prompt="AIは月まで行けますか？",
        response="はい、AIは宇宙に行けます。",
        annotation="AIはソフトウェアなので、物理的に行くことはできない。誤答。",
        reviewer="annotator1"
    )
    logs = load_annotated_logs()
    for log in logs:
        print(log)
