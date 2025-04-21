import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# === 設定 ===
SAFE_FILES = {".env", "cache_store.jsonl", "index_store.faiss", "id_map.json"}
SAFE_DIRS = {"api_keys", ".venv", "venv", "env", "logs", "vector_index", "memory/cache/data"}
TARGET_EXTENSIONS = {".pyc", ".log", ".tmp", ".bak"}
TARGET_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ipynb_checkpoints", ".cache", ".huggingface"}

# === ログ関数 ===
def log(msg):
    print(f"[CLEAN] {msg}")

def should_delete_file(file_path, safe_mode):
    if safe_mode:
        if file_path.name in SAFE_FILES or any(part in SAFE_DIRS for part in file_path.parts):
            return False
    return file_path.suffix in TARGET_EXTENSIONS

def should_delete_dir(dir_path, safe_mode):
    if safe_mode:
        if dir_path.name in SAFE_DIRS or any(part in SAFE_DIRS for part in dir_path.parts):
            return False
    return dir_path.name in TARGET_DIRS

def clean_workspace(root_path, dry_run=False, safe_mode=False, keep_logs=False):
    deleted = []
    for path in Path(root_path).rglob("*"):
        try:
            if path.is_file():
                if should_delete_file(path, safe_mode):
                    if not keep_logs or path.suffix != ".log":
                        log(f"Delete file: {path}" + (" [dry-run]" if dry_run else ""))
                        if not dry_run:
                            path.unlink()
                            deleted.append(str(path))
            elif path.is_dir():
                if should_delete_dir(path, safe_mode):
                    log(f"Delete dir: {path}" + (" [dry-run]" if dry_run else ""))
                    if not dry_run:
                        for child in path.rglob("*"):
                            try:
                                if child.is_file():
                                    child.unlink()
                                else:
                                    child.rmdir()
                            except:
                                pass
                        path.rmdir()
                        deleted.append(str(path))
        except Exception as e:
            log(f"ERROR: {path} -> {e}")

    if not dry_run and deleted:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Path("logs") / f"clean_workspace_{timestamp}.log"
        os.makedirs(log_file.parent, exist_ok=True)
        with open(log_file, "w", encoding="utf-8") as f:
            for line in deleted:
                f.write(line + "\n")
        log(f"Saved clean log to {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Safe Clean AIMO Workspace")
    parser.add_argument("--dry-run", action="store_true", help="List files to be deleted but do not delete")
    parser.add_argument("--safe-mode", action="store_true", help="Protect important AIMO files")
    parser.add_argument("--keep-logs", action="store_true", help="Preserve .log files even if deletable")
    args = parser.parse_args()

    log(f"=== AIMO Clean Start (safe_mode={args.safe_mode}, dry_run={args.dry_run}) ===")
    clean_workspace(".", dry_run=args.dry_run, safe_mode=args.safe_mode, keep_logs=args.keep_logs)
    log("=== Clean End ===")