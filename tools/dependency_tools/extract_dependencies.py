from pathlib import Path
import sys
import os
import ast
import csv
from collections import defaultdict

# AIMOルート検出
current_dir = Path(__file__).resolve()
aimo_root = current_dir.parents[2]
sys.path.insert(0, str(aimo_root))

from core.utils.logger import log_event

OUTPUT_CSV = aimo_root / "tools" / "dependency_tools" / "dependency_map.csv"
TARGET_EXT = ".py"

def extract_dependencies(root_dir=None, output_path=None, exclude_dirs=None):
    """
    プロジェクト内の .py ファイルをスキャンし、import 関係を CSV に保存する
    exclude_dirs: リスト of str, 除外するディレクトリ名
    """
    root = Path(root_dir or aimo_root)
    exclude = set(exclude_dirs or ["venv", "__pycache__", "tests"])
    dep_map = defaultdict(list)

    log_event("=== AIMO Dependency Extraction Start ===", "INFO")
    for subdir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith(TARGET_EXT):
                abs_path = Path(subdir) / file
                rel_path = abs_path.relative_to(aimo_root).as_posix()
                try:
                    tree = ast.parse(abs_path.read_text(encoding="utf-8"), filename=str(abs_path))
                except Exception as e:
                    log_event(f"Failed parse {rel_path}: {e}", "WARN")
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            dep_map[rel_path].append(alias.name)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        dep_map[rel_path].append(node.module)

    out_csv = Path(output_path or OUTPUT_CSV)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Source File", "Imported Module"])
        for src, imps in sorted(dep_map.items()):
            for imp in sorted(imps):
                writer.writerow([src, imp])

    log_event(f"Dependency map saved to {out_csv}", "SUCCESS")

if __name__ == "__main__":
    extract_dependencies()
"# dummy comment for CI trigger" 
