"""
restore_backup.py
-----------------
AIMO v2.2.10 – Step S9: backup & restore utility.

• Generates timestamped ZIP backups of the entire AIMO root (excluding the `logs/` directory by default).
• Restores a given backup ZIP to the AIMO root, after backing‑up the *current* state as a safety measure.
• Uses `find_aimo_root()` for path resolution and `log_event()` for structured logging.

Usage:
    python restore_backup.py              # create backup ZIP
    python restore_backup.py --restore <zip_path>   # restore from ZIP
"""

import argparse
import os
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

try:
    from core.find_aimo_root import find_aimo_root
    from core.logger import log_event
except ImportError as e:
    print(f"[ERROR] 必要モジュールのインポートに失敗しました: {e}")
    raise

ROOT = Path(find_aimo_root())
BACKUP_DIR = ROOT / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

EXCLUDE_DIRS = {"logs", "backups", ".git", "__pycache__"}

def create_backup() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"aimo_backup_{timestamp}.zip"
    zip_path = BACKUP_DIR / zip_name

    log_event("[INFO]", f"バックアップ開始: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in ROOT.rglob("*"):
            rel_path = path.relative_to(ROOT)
            if any(part in EXCLUDE_DIRS for part in rel_path.parts):
                continue
            zf.write(path, rel_path)

    log_event("[SUCCESS]", f"バックアップ完了: {zip_path}")
    return zip_path

def restore_from_zip(zip_path: Path):
    if not zip_path.exists():
        log_event("[ERROR]", f"指定ZIPが見つかりません: {zip_path}")
        return

    # safety backup of current state
    safety_zip = create_backup()
    log_event("[INFO]", f"復元前の安全バックアップを作成: {safety_zip}")

    log_event("[INFO]", f"復元開始: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(ROOT)

    log_event("[SUCCESS]", f"復元完了: {zip_path}")

def main():
    parser = argparse.ArgumentParser(description="AIMO backup & restore utility")
    parser.add_argument("--restore", type=str, help="ZIP path to restore from")
    args = parser.parse_args()

    if args.restore:
        restore_from_zip(Path(args.restore))
    else:
        create_backup()

if __name__ == "__main__":
    main()
