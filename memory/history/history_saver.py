# memory/history/history_saver.py

"""
history_saver.py – 会話履歴を日付単位で保存
AIMO v2.2.10 – memory/history 用サブモジュール
"""

import json
from datetime import datetime
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

# 保存先ディレクトリの初期化
AIMO_ROOT = find_aimo_root()
HISTORY_DIR = AIMO_ROOT / "memory" / "history"
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

def save_conversation(conversation: dict, filename: str = None) -> Path:
    """
    対話データを memory/history に保存
    - conversation: {"id": ..., "timestamp": ..., "messages": [...]}
    - filename: 任意の保存ファイル名。未指定なら日付ベースで決定
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = filename or f"conv_{timestamp}.json"
        path = HISTORY_DIR / fname

        with path.open("w", encoding="utf-8") as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)

        log_event("[SUCCESS]", f"会話履歴を保存しました: {path}", category="history")
        return path

    except Exception as e:
        log_event("[ERROR]", f"会話履歴の保存に失敗: {e}", category="history")
        return None
