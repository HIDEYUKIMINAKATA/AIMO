import csv
from collections import defaultdict
from pathlib import Path

def reverse_dependency_map(input_csv, output_csv):
    reverse_map = defaultdict(set)
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames or []
        
        # 列名の自動検出
        source_col = None
        target_col = None
        for f in fieldnames:
            low = f.lower()
            if 'source' in low and 'file' in low:
                source_col = f
            if ('imported' in low and 'module' in low) or ('depends' in low and 'on' in low):
                target_col = f
        
        # フォールバック：最初と2番目のカラムを使用
        if source_col is None and len(fieldnames) >= 1:
            source_col = fieldnames[0]
        if target_col is None and len(fieldnames) >= 2:
            target_col = fieldnames[1]
        
        if source_col is None or target_col is None:
            raise ValueError(f"Cannot detect source/target columns from: {fieldnames}")
        
        for row in reader:
            src = row[source_col].strip()
            tgt = row[target_col].strip()
            reverse_map[tgt].add(src)

    # 出力
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Imported Module', 'Dependent File'])
        writer.writeheader()
        for tgt, deps in reverse_map.items():
            for dep in sorted(deps):
                writer.writerow({'Imported Module': tgt, 'Dependent File': dep})

if __name__ == '__main__':
    base = Path(__file__).resolve().parents[2]
    in_csv = base / 'tools' / 'dependency_tools' / 'dependency_map.csv'
    out_csv = base / 'tools' / 'dependency_tools' / 'reverse_dependency_map.csv'
    try:
        reverse_dependency_map(in_csv, out_csv)
        print(f"[SUCCESS] Reverse dependency map saved to: {out_csv}")
    except Exception as e:
        print(f"[ERROR] {e}")