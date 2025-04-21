# scripts/checks/check_logs_consistency.py
import json
from pathlib import Path

from core.find_aimo_root import find_aimo_root
from core.logger import log_event

def check_logs_consistency():
    root = Path(find_aimo_root())
    logs_dir = root / "logs" / "imports"

    log_event("INFO", f"ログディレクトリ確認: {logs_dir}")

    if not logs_dir.exists():
        log_event("ERROR", f"ログディレクトリが存在しません: {logs_dir}")
        return

    jsonl_files = list(logs_dir.glob("*.jsonl"))
    if not jsonl_files:
        log_event("WARN", "JSONLログファイルが1件も見つかりませんでした")
        return

    for file_path in jsonl_files:
        log_event("INFO", f"検査中ファイル: {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [json.loads(line) for line in f if line.strip()]
            log_event("SUCCESS", f"{file_path.name} の読み込みに成功 | 行数: {len(lines)}")
        except Exception as e:
            log_event("ERROR", f"{file_path.name} の読み込み失敗: {e}")

if __name__ == "__main__":
    log_event("INFO", "=== AIMO ログ整合性チェック 開始 ===")
    check_logs_consistency()
    log_event("INFO", "=== チェック完了 ===")
