
import os
import csv
import json
import sys
from pathlib import Path

# ✅ AIMOルート補完
current_file = Path(__file__).resolve()
aimo_root = current_file.parents[2]
sys.path.insert(0, str(aimo_root))

try:
    import networkx as nx
except ImportError:
    raise ImportError("networkx is required. Install via 'pip install networkx'")

from core.utils.logger import log_event

def load_dependencies(input_csv):
    edges = []
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src_file = row['Source File']
            imp_mod = row['Imported Module']
            src_module = src_file[:-3].replace(os.sep, '.')
            edges.append((src_module, imp_mod))
    return edges

def analyze_integrity(edges):
    G = nx.DiGraph()
    for src, tgt in edges:
        G.add_edge(src, tgt)

    cycles = list(nx.simple_cycles(G))
    all_src = {src for src, _ in edges}
    all_tgt = {tgt for _, tgt in edges}

    orphans = [n for n in all_src if G.in_degree(n) == 0]
    leaves = [n for n in all_src if G.out_degree(n) == 0]
    missing = sorted(list(all_tgt - all_src))

    score = 1.0
    if cycles:
        score -= 0.3
    if missing:
        score -= 0.2
    if len(orphans) > 3:
        score -= 0.1
    score = max(0.0, round(score, 3))

    return {
        'cycle_count': len(cycles),
        'cycles': cycles,
        'orphan_count': len(orphans),
        'orphans': sorted(orphans),
        'leaf_count': len(leaves),
        'leaves': sorted(leaves),
        'missing_count': len(missing),
        'missing': missing,
        'health_score': score
    }

def check_violation(report):
    return report['cycle_count'] > 0 or report['missing_count'] > 0

if __name__ == '__main__':
    base = Path(__file__).resolve().parents[2]
    input_csv = base / 'tools' / 'dependency_tools' / 'dependency_map.csv'
    output_json = base / 'tools' / 'dependency_tools' / 'dependency_integrity_report.json'

    log_event("=== Checking Dependency Integrity ===", "INFO")
    edges = load_dependencies(input_csv)
    report = analyze_integrity(edges)

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    log_event(f"Report saved to: {output_json}", "SUCCESS")
    log_event(f"Cycles: {report['cycle_count']}, Missing: {report['missing_count']}, Score: {report['health_score']}", "INFO")

    if check_violation(report):
        log_event("Dependency integrity check failed. CI will stop.", "ERROR")
        sys.exit(1)
    else:
        log_event("Dependency integrity check passed.", "SUCCESS")
