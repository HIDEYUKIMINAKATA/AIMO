import os
import json
from pathlib import Path
from typing import List, Dict
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

def load_summaries() -> List[Dict[str, str]]:
    root = find_aimo_root()
    summary_dir = Path(root) / "memory" / "summary" / "saved"
    log_event("[INFO]", f"要約ディレクトリ確認: {summary_dir}")

    if not summary_dir.exists():
        log_event("[WARN]", f"要約ディレクトリが存在しません: {summary_dir}")
        return []

    summaries = []
    count = 0

    for file in summary_dir.glob("*.jsonl"):
        try:
            with open(file, encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        summaries.append({
                            "source": entry.get("source", "不明"),
                            "summary": entry.get("summary", "（要約なし）")
                        })
                        count += 1
                    except json.JSONDecodeError:
                        log_event("[WARN]", f"JSONパース失敗: {line.strip()}")
        except Exception as e:
            log_event("[ERROR]", f"要約ファイル読み込み失敗: {file} | {e}")

    log_event("[SUCCESS]", f"要約ファイル読み込み完了（{count}件）")
    return summaries
