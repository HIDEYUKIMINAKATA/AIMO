from pathlib import Path
import sys
import csv
from collections import defaultdict

# AIMOルート検出
current_dir = Path(__file__).resolve()
aimo_root = current_dir.parents[2]
sys.path.insert(0, str(aimo_root))

from core.utils.logger import log_event

def reverse_dependencies():
    """
    dependency_map.csv を読み込み、逆依存マップを生成する
    """
    in_csv = aimo_root / "tools" / "dependency_tools" / "dependency_map.csv"
    out_csv = aimo_root / "tools" / "dependency_tools" / "reverse_dependency_map.csv"

    log_event("=== Building Reverse Dependency Map ===", "INFO")
    reverse_map = defaultdict(set)
    with open(in_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        src_col, tgt_col = reader.fieldnames[:2]
        for row in reader:
            reverse_map[row[tgt_col]].add(row[src_col])

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Imported Module", "Dependent File"])
        for tgt, deps in sorted(reverse_map.items()):
            for dep in sorted(deps):
                writer.writerow([tgt, dep])

    log_event(f"Reverse dependency map saved to: {out_csv}", "SUCCESS")

if __name__ == "__main__":
    reverse_dependencies()
