"""
eval_logger.py - AIMO memory/eval モジュール
AI出力に対する評価記録（手動または自動）をログとして蓄積

評価内容:
- モデル名 / プロンプト / 応答
- 評価スコア（手動/自動）
- 評価コメント（任意）
"""

import json
from pathlib import Path
from datetime import datetime
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

EVAL_DIR = Path(find_aimo_root()) / "memory" / "eval"
EVAL_FILE = EVAL_DIR / "evaluation_log.jsonl"
EVAL_DIR.mkdir(parents=True, exist_ok=True)

def log_evaluation(model: str, prompt: str, response: str, score: float, comment: str = "") -> None:
    """
    指定された評価内容をJSONLでログに保存
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "prompt": prompt,
        "response": response,
        "score": score,
        "comment": comment
    }

    try:
        with open(EVAL_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log_event("[SUCCESS]", f"評価ログ追加: {model} ({score})", category="eval")
    except Exception as e:
        log_event("[ERROR]", f"評価ログ保存失敗: {e}", category="eval")

def read_evaluations() -> list:
    """
    評価ログをすべて読み込んで返す（リスト形式）
    """
    if not EVAL_FILE.exists():
        return []

    try:
        with open(EVAL_FILE, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
        log_event("[INFO]", f"評価ログ {len(lines)} 件を読み込み", category="eval")
        return lines
    except Exception as e:
        log_event("[ERROR]", f"評価ログ読込失敗: {e}", category="eval")
        return []

# CLI用テスト
if __name__ == "__main__":
    log_evaluation("Zephyr", "テストプロンプト", "これはAIの応答です", 4.5, "自然で分かりやすい")
    logs = read_evaluations()
    print(json.dumps(logs, indent=2, ensure_ascii=False))
