"""
annotator.py - AIMO memory/annotated モジュール
対話ログやAI応答に対する注釈情報を付加して記録保存する

注釈対象:
- ユーザー発話・AI応答
- ラベル（正誤・意図分類など）
- コメント（メモ・補足など）
"""

import json
from datetime import datetime
from pathlib import Path
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

ANNOTATED_DIR = Path(find_aimo_root()) / "memory" / "annotated"
ANNOTATED_FILE = ANNOTATED_DIR / "annotated_log.jsonl"
ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)

def annotate_conversation(conv_id: str, user_input: str, ai_output: str, label: str, comment: str = "") -> None:
    """
    対話に対して注釈を記録する
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "conv_id": conv_id,
        "user_input": user_input,
        "ai_output": ai_output,
        "label": label,
        "comment": comment
    }

    try:
        with open(ANNOTATED_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log_event("[SUCCESS]", f"注釈ログ追加: {conv_id} ({label})", category="annotated")
    except Exception as e:
        log_event("[ERROR]", f"注釈ログ保存失敗: {e}", category="annotated")

def read_annotations() -> list:
    """
    すべての注釈をリスト形式で読み込む
    """
    if not ANNOTATED_FILE.exists():
        return []

    try:
        with open(ANNOTATED_FILE, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
        log_event("[INFO]", f"注釈ログ {len(lines)} 件を読み込み", category="annotated")
        return lines
    except Exception as e:
        log_event("[ERROR]", f"注釈ログ読込失敗: {e}", category="annotated")
        return []

# テスト用CLI実行例
if __name__ == "__main__":
    annotate_conversation(
        conv_id="conv001",
        user_input="今の結果はどういう意味？",
        ai_output="これは過去の記録を要約したものです。",
        label="正確",
        comment="簡潔で明瞭"
    )
    data = read_annotations()
    print(json.dumps(data, indent=2, ensure_ascii=False))
