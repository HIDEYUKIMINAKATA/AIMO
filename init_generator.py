"""
init_generator.py – AIMO全体に __init__.py を一括生成
"""

import os
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

TARGET_DIRS = [
    "ai_nodes",
    "core",
    "memory",
    "scripts",
    "tests",
]

def ensure_init_files(base_dir: Path):
    for dirpath, _, _ in os.walk(base_dir):
        dir_path = Path(dirpath)
        init_file = dir_path / "__init__.py"
        if not init_file.exists():
            try:
                init_file.write_text("# auto-generated __init__.py\n", encoding="utf-8")
                log_event("[SUCCESS]", f"__init__.py created in: {dir_path}", category="init_generator")
            except Exception as e:
                log_event("[ERROR]", f"Failed to create __init__.py in {dir_path}: {e}", category="init_generator")
        else:
            log_event("[INFO]", f"__init__.py already exists in: {dir_path}", category="init_generator")

def main():
    root = Path(find_aimo_root())
    log_event("[INFO]", f"Scanning base path: {root}", category="init_generator")
    for relative_dir in TARGET_DIRS:
        full_path = root / relative_dir
        if full_path.exists():
            log_event("[INFO]", f"Processing: {full_path}", category="init_generator")
            ensure_init_files(full_path)
        else:
            log_event("[WARN]", f"Directory not found: {full_path}", category="init_generator")
    log_event("[SUCCESS]", "All __init__.py generation completed", category="init_generator")

if __name__ == "__main__":
    main()
