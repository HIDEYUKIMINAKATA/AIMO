#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path

# ── AIMO ルート検出・設定 ─────────────────────────────────────────
from core.utils.path_utils import find_aimo_root
root = Path(find_aimo_root())
sys.path.insert(0, str(root))

from core.utils.logger import log_event

def run_step(name: str, cmd: str):
    log_event("INFO", f"▶ Running: {name}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        log_event("SUCCESS", f"Step succeeded: {name}")
    except subprocess.CalledProcessError:
        log_event("ERROR", f"Step failed: {name}")
        sys.exit(1)

if __name__ == "__main__":
    log_event("INFO", "=== AIMO Dependency Check Sequence Start ===")

    # 各ステップを順に実行
    steps = [
        (
            "Extract Dependencies",
            f"python {root / 'tools' / 'dependency_tools' / 'extract_dependencies.py'}"
        ),
        (
            "Reverse Dependencies",
            f"python {root / 'tools' / 'dependency_tools' / 'reverse_dependencies.py'}"
        ),
        (
            "Check Dependency Integrity",
            f"python {root / 'tools' / 'dependency_tools' / 'check_dependency_integrity.py'}"
        ),
    ]

    for name, cmd in steps:
        run_step(name, cmd)

    log_event("SUCCESS", "=== All checks completed successfully ===")
