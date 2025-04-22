
import csv
from collections import defaultdict
from pathlib import Path
import sys

# ✅ AIMOルート補完
current_file = Path(__file__).resolve()
aimo_root = current_file.parents[2]
sys.path.insert(0, str(aimo_root))

from core.utils.logger import log_event

def build_reverse_map(input_csv):
    reverse_map = defaultdict(list)
    try:
        with open(input_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames or []

            source_col = None
            target_col = None
            for f in fieldnames:
                low = f.lower()
                if 'source' in low and 'file' in low:
                    source_col = f
                if ('imported' in low and 'module' in low) or ('depends' in low and 'on' in low):
                    target_col = f

            if source_col is None or target_col is None:
                raise ValueError(f"Cannot detect source/target columns from: {fieldnames}")

            for row in reader:
                src = row[source_col].strip()
                tgt = row[target_col].strip()
                reverse_map[tgt].append(src)

        return reverse_map
    except Exception as e:
        log_event(f"[ERROR] Failed to build reverse map: {e}", "ERROR")
        raise

def save_reverse_map_to_csv(reverse_map, output_csv):
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Imported Module', 'Dependent File', 'Reference Count'])
            writer.writeheader()
            for tgt, src_list in reverse_map.items():
                count = len(src_list)
                for src in sorted(src_list):
                    writer.writerow({'Imported Module': tgt, 'Dependent File': src, 'Reference Count': count})
        log_event(f"Reverse dependency map saved to: {output_csv}", "SUCCESS")
    except Exception as e:
        log_event(f"[ERROR] Failed to save reverse dependency CSV: {e}", "ERROR")
        raise

if __name__ == '__main__':
    try:
        base = Path(__file__).resolve().parents[2]
        in_csv = base / 'tools' / 'dependency_tools' / 'dependency_map.csv'
        out_csv = base / 'tools' / 'dependency_tools' / 'reverse_dependency_map.csv'

        log_event("=== Building Reverse Dependency Map ===", "INFO")
        rev_map = build_reverse_map(in_csv)
        save_reverse_map_to_csv(rev_map, out_csv)
    except Exception as e:
        log_event(f"Reverse dependency processing failed: {e}", "ERROR")
