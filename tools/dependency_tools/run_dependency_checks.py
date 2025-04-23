#!/usr/bin/env python3
import sys
from pathlib import Path
import subprocess

# ── プロジェクトルート（AIMO）を sys.path に追加 ────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from core.utils.path_utils import find_aimo_root
from core.utils.logger import log_event

def main():
    # ルート検出（CI／ローカル共通）
    root = find_aimo_root()
    # sys.path[0] を確実にルートに設定
    sys.path[0] = root
    log_event("INFO", f"AIMO root detected: {root}")
    log_event("INFO", "=== AIMO Dependency Check Sequence Start ===")

    steps = [
        ("Extract Dependencies",
         "python tools/dependency_tools/extract_dependencies.py --root . "
         "--output tools/dependency_tools/dependency_map.csv "
         "--exclude venv,__pycache__,tests --log-warn"
        ),
        ("Reverse Dependencies",
         "python tools/dependency_tools/reverse_dependencies.py"
        ),
        ("Check Dependency Integrity",
         "python tools/dependency_tools/check_dependency_integrity.py"
        ),
    ]

    for name, cmd in steps:
        log_event("INFO", f"▶ Running: {name}")
        try:
            subprocess.run(cmd, shell=True, check=True)
            log_event("SUCCESS", f"Step succeeded: {name}")
        except subprocess.CalledProcessError:
            log_event("ERROR", f"Step failed: {name}")
            sys.exit(1)

    log_event("SUCCESS", "=== All checks completed successfully ===")

if __name__ == "__main__":
    main()
