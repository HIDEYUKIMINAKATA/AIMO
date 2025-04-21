"""summary_saver.py – 要約結果をJSONL形式で保存するモジュール"""

import os
import json
from datetime import datetime
from pathlib import Path

try:
    from core.find_aimo_root import find_aimo_root
    from core.logger import log_event
except ImportError:
    def find_aimo_root() -> str:
        return str(Path(__file__).resolve().parents[2])

    def log_event(level, message, category=None):
        print(f"{level} {category or 'general'} | {message}")

def save_summary(prompt_id: str, ai_model: str, summary_text: str, timestamp: str = None) -> str:
    """
    要約結果を JSONL 形式で memory/summary/saved/ に保存する
    :param prompt_id: 対話やプロンプトの一意識別子
    :param ai_model: 使用AIモデル名（例: Claude, Zephyr）
    :param summary_text: 要約されたテキスト
    :param timestamp: タイムスタンプ（省略時は現在時刻）
    :return: 保存先パスまたはエラーメッセージ
    """
    try:
        root = Path(find_aimo_root())
        save_dir = root / "memory" / "summary" / "saved"
        save_dir.mkdir(parents=True, exist_ok=True)

        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = save_dir / f"{date_str}_{ai_model.lower()}_summary.jsonl"

        record = {
            "id": prompt_id,
            "model": ai_model,
            "text": summary_text,
            "ts": timestamp
        }

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        log_event("[INFO]", f"要約保存先パス: {file_path}", category="summary")
        log_event("[SUCCESS]", f"{ai_model} の要約を保存しました", category="summary")
        return str(file_path)

    except Exception as e:
        log_event("[ERROR]", f"要約保存に失敗: {e}", category="summary")
        return f"[ERROR] {e}"
