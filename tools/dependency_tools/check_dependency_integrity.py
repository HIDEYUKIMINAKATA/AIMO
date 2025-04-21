import os
import csv
import json
from pathlib import Path

try:
    import networkx as nx
except ImportError:
    raise ImportError("networkx is required. Install via 'pip install networkx'")

def load_dependencies(input_csv):
    edges = []
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src_file = row['Source File']
            imp_mod = row['Imported Module']
            # モジュール名に変換（拡張子除去 + セパレータ置換）
            src_module = src_file[:-3].replace(os.sep, '.')
            edges.append((src_module, imp_mod))
    return edges

def analyze_integrity(edges):
    G = nx.DiGraph()
    for src, tgt in edges:
        G.add_edge(src, tgt)

    # サイクル検出
    cycles = list(nx.simple_cycles(G))

    # モジュール集合
    all_src = {src for src, _ in edges}
    all_tgt = {tgt for _, tgt in edges}

    # 依存されないモジュール（in-degree=0）
    orphans = [n for n in all_src if G.in_degree(n) == 0]

    # 何もimportしていないモジュール（out-degree=0）
    leaves = [n for n in all_src if G.out_degree(n) == 0]

    # missing: imported but no source definition
    missing = sorted(list(all_tgt - all_src))

    return {
        'cycle_count': len(cycles),
        'cycles': cycles,
        'orphan_count': len(orphans),
        'orphans': sorted(orphans),
        'leaf_count': len(leaves),
        'leaves': sorted(leaves),
        'missing_count': len(missing),
        'missing': missing
    }

if __name__ == '__main__':
    base = Path(__file__).resolve().parents[2]
    input_csv = base / 'tools' / 'dependency_tools' / 'dependency_map.csv'
    output_json = base / 'tools' / 'dependency_tools' / 'dependency_integrity_report.json'

    print("=== Checking Dependency Integrity ===")
    edges = load_dependencies(input_csv)
    report = analyze_integrity(edges)

    # レポート保存
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # サマリー出力
    print(f"[SUCCESS] Report saved to: {output_json}")
    print(f"- Cycles detected: {report['cycle_count']}")
    print(f"- Orphans (no inbound): {report['orphan_count']}")
    print(f"- Leaves (no outbound): {report['leaf_count']}")
    print(f"- Missing modules: {report['missing_count']}")