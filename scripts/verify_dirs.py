import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
# scripts/verify_dirs.py
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

# 定義済みフォルダ一覧（dir_setup.py と完全一致させる）
REQUIRED_DIRS = [
    "logs/dispatcher", "logs/error", "logs/command",
    "logs/imports", "logs/aimobot_conversations",
    "memory", "api_keys", "input/cli", "output/ai_nodes",
    "tests", "scripts", "core", "ai_nodes"
]

def verify_directories():
    root = Path(find_aimo_root())
    all_ok = True

    for d in REQUIRED_DIRS:
        full_path = root / d
        if not full_path.exists():
            log_event("ERROR", f"Missing directory: {d}")
            all_ok = False
        else:
            log_event("SUCCESS", f"Exists: {d}")

    if all_ok:
        log_event("SUCCESS", "✅ すべてのディレクトリが存在します")
    else:
        log_event("WARN", "⚠ 一部のディレクトリが欠けています")

if __name__ == "__main__":
    verify_directories()
