"""cache_checker.py – 要約や出力のキャッシュ状態を確認・表示"""

import sys
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

def check_cache(conv_id: str):
    root = Path(find_aimo_root())
    summary_path = root / "logs" / "summaries" / f"summary_{conv_id}.txt"
    output_path = root / "output" / "ai_nodes" / f"last_output.txt"
    cache_path = root / "memory" / "cache" / f"{conv_id}.cache"

    log_event("[INFO]", f"キャッシュチェック開始: ID = {conv_id}", category="cache")

    if summary_path.exists():
        log_event("[SUCCESS]", f"要約ファイル存在: {summary_path}", category="cache")
    else:
        log_event("[WARN]", f"要約ファイル未生成: {summary_path}", category="cache")

    if output_path.exists():
        log_event("[SUCCESS]", f"最終出力ファイル存在: {output_path}", category="cache")
    else:
        log_event("[WARN]", f"最終出力ファイル未生成: {output_path}", category="cache")

    if cache_path.exists():
        log_event("[SUCCESS]", f"キャッシュファイル存在: {cache_path}", category="cache")
    else:
        log_event("[WARN]", f"キャッシュファイル未生成: {cache_path}", category="cache")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cache_checker.py <conversation_id>")
        sys.exit(1)
    check_cache(sys.argv[1])
