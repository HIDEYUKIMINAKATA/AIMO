from pathlib import Path
import sys
import os
import json
import csv
import networkx as nx

# AIMOルート検出
current_dir = Path(__file__).resolve()
aimo_root = current_dir.parents[2]
sys.path.insert(0, str(aimo_root))

from core.utils.logger import log_event

def load_dependencies(input_csv):
    edges = []
    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        src_col, tgt_col = reader.fieldnames[:2]
        for row in reader:
            src = row[src_col]
            tgt = row[tgt_col]
            src_mod = src[:-3].replace(os.sep, ".")
            edges.append((src_mod, tgt))
    return edges

def analyze_integrity(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    cycles = list(nx.simple_cycles(G))
    all_src = {s for s, _ in edges}
    all_tgt = {t for _, t in edges}
    orphans = [n for n in all_src if G.in_degree(n) == 0]
    leaves = [n for n in all_src if G.out_degree(n) == 0]
    missing = sorted(all_tgt - all_src)
    return {
        "cycle_count": len(cycles),
        "cycles": cycles,
        "orphan_count": len(orphans),
        "orphans": sorted(orphans),
        "leaf_count": len(leaves),
        "leaves": sorted(leaves),
        "missing_count": len(missing),
        "missing": missing,
    }

def check_dependency_integrity():
    in_csv = aimo_root / "tools" / "dependency_tools" / "dependency_map.csv"
    out_json = aimo_root / "tools" / "dependency_tools" / "dependency_integrity_report.json"

    log_event("=== Checking Dependency Integrity ===", "INFO")
    edges = load_dependencies(in_csv)
    report = analyze_integrity(edges)

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    log_event(f"Report saved to: {out_json}", "SUCCESS")

if __name__ == "__main__":
    check_dependency_integrity()
