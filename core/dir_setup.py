# core/dir_setup.py – AIMOディレクトリ構成自動初期化スクリプト
import os
from pathlib import Path
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

def ensure_directories() -> None:
    """AIMO全体のフォルダ構成を初期化・検査する"""
    ROOT = Path(find_aimo_root())

    directories = [
        ROOT / "input" / "cli",
        ROOT / "input" / "audio",
        ROOT / "output" / "ai_nodes",
        ROOT / "output" / "audio",
        ROOT / "logs",
        ROOT / "memory",
        ROOT / "api_keys",
        ROOT / "ai_nodes",
        ROOT / "core",
    ]

    for dir_path in directories:
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            log_event("[SUCCESS]", f"Directory ready: {dir_path}", category="setup")
        except Exception as e:
            log_event("[ERROR]", f"Directory creation failed: {dir_path} | {e}", category="setup")

if __name__ == "__main__":
    log_event("[INFO]", "AIMOディレクトリセットアップ開始", category="setup")
    ensure_directories()
    log_event("[SUCCESS]", "AIMOディレクトリセットアップ完了", category="setup")
