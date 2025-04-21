import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import os, json
from datetime import datetime
from pathlib import Path

try:
    from core.find_aimo_root import find_aimo_root
except ModuleNotFoundError:
    # フォールバック：現在のファイルから2階層上をルートとみなす
    def find_aimo_root():
        return Path(__file__).resolve().parent.parent

try:
    from core.logger import log_event
except ModuleNotFoundError:
    def log_event(level, message):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ts} {level} {message}")

from scripts.conversation_filter import filter_conversations_by_id
from scripts.markdown_exporter import export_to_markdown

ROOT = Path(find_aimo_root())
IMPORT_PATH = ROOT / "logs" / "imports" / "conversations.json"
EXPORT_DIR = ROOT / "logs" / "aimobot_conversations"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_PATH = EXPORT_DIR / f"aimo_project_log_{datetime.now().date()}.md"

# 抽出対象 ID を settings などで管理しても良い
TARGET_IDS = ["67fe3e04-9a94-800f-8f05-55470099cef9"]

def main():
    log_event("[INFO]", "log_importer.py 起動")

    if not IMPORT_PATH.exists():
        log_event("[ERROR]", f"ファイルが見つかりません: {IMPORT_PATH}")
        return

    with IMPORT_PATH.open(encoding='utf-8') as f:
        data = json.load(f)

    filtered = filter_conversations_by_id(data, TARGET_IDS)
    if not filtered:
        log_event("[WARN]", "対象のスレッドが見つかりませんでした")
        return

    export_to_markdown(filtered, EXPORT_PATH)
    log_event("[SUCCESS]", f"抽出と保存完了: {EXPORT_PATH}")

if __name__ == "__main__":
    main()
