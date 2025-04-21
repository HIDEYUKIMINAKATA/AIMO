
import os
from pathlib import Path

REQUIRED_DIRS = [
    "ai_nodes", "core", "input", "input/cli", "input/audio",
    "output", "logs", "memory", "scripts", "tests", "api_keys"
]

REQUIRED_FILES = [
    ".env", "launch.py", "dispatcher.py", "route_ai.py",
    "env_autogen.py", "requirements.txt", "requirements_310.txt"
]

def check_structure():
    root = Path(__file__).resolve().parent
    missing_dirs = [d for d in REQUIRED_DIRS if not (root / d).is_dir()]
    missing_files = [f for f in REQUIRED_FILES if not (root / f).is_file()]

    print("\n=== ✅ AIMO構成チェック ===")
    print(f"[INFO] ルートパス: {root}")
    if missing_dirs:
        print(f"[ERROR] 欠損ディレクトリ: {missing_dirs}")
    else:
        print("[SUCCESS] 必須ディレクトリは全て存在")

    if missing_files:
        print(f"[ERROR] 欠損ファイル: {missing_files}")
    else:
        print("[SUCCESS] 必須ファイルは全て存在")

    if not missing_dirs and not missing_files:
        print("[✅] AIMO構成は完全です")

if __name__ == "__main__":
    check_structure()
