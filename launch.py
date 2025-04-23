#!/usr/bin/env python3
import sys
from pathlib import Path

# ── AIMO プロジェクトルートを自動で sys.path に追加 ──
def find_aimo_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "core").exists() and (parent / "tools").exists():
            return parent
    raise RuntimeError("AIMOルートが見つかりません")

AIMO_ROOT = find_aimo_root()
sys.path.insert(0, str(AIMO_ROOT))

# ── ログとルート確認 ──
from core.utils.logger import log_event

def main():
    log_event("INFO", f"AIMOルート特定成功: {AIMO_ROOT}")
    log_event("INFO", "AIMO launch.py が起動されました")
    # 実行フロー開始（例: run_main_system()）

if __name__ == "__main__":
    main()
