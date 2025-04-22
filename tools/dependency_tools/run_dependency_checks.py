
import sys
import os
import subprocess
from pathlib import Path

# ✅ AIMOルートパスを動的に追加
current_dir = Path(__file__).resolve()
aimo_root = current_dir.parents[2]
sys.path.insert(0, str(aimo_root))

from core.utils.logger import log_event

def run_step(name, cmd):
    log_event(f"▶ Running: {name}", "INFO")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        log_event(f"[ERROR] Step failed: {name}", "ERROR")
        sys.exit(1)
    log_event(f"[SUCCESS] Step succeeded: {name}", "SUCCESS")

if __name__ == '__main__':
    steps = [
        ("Extract Dependencies", "python tools/dependency_tools/extract_dependencies.py --root . --output tools/dependency_tools/dependency_map.csv --exclude venv,__pycache__,tests --log-warn"),
        ("Reverse Dependencies", "python tools/dependency_tools/reverse_dependencies.py"),
        ("Check Dependency Integrity", "python tools/dependency_tools/check_dependency_integrity.py"),
    ]

    log_event("=== AIMO Dependency Check Sequence Start ===", "INFO")
    for name, cmd in steps:
        run_step(name, cmd)
    log_event("=== All checks completed successfully ===", "SUCCESS")
