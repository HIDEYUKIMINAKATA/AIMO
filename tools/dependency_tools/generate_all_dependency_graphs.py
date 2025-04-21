import os
import csv
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def load_dependency_map(csv_path):
    edges = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        source_key = None
        target_key = None
        for name in reader.fieldnames:
            low = name.lower()
            if "source" in low and "file" in low:
                source_key = name
            elif "imported" in low and "module" in low or "depends on" in low:
                target_key = name
        if not source_key or not target_key:
            raise ValueError(f"Invalid column names: {reader.fieldnames}")
        for row in reader:
            src = row[source_key].strip()
            tgt = row[target_key].strip()
            edges.append((src, tgt))
    return edges

def generate_graphs(edges, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    modules = set([src for src, _ in edges])
    for module in modules:
        G = nx.DiGraph()
        sub_edges = [(src, tgt) for src, tgt in edges if src == module]
        if not sub_edges:
            continue
        G.add_edges_from(sub_edges)
        plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(G, k=0.5, iterations=20)
        nx.draw(G, pos, with_labels=True, node_size=600, font_size=7, arrows=True, edge_color='gray')
        plt.title(f"Dependency Graph: {module}", fontsize=10)
        sanitized = module.replace("/", "_").replace(":", "_").replace("\\", "_")
        filepath = os.path.join(output_dir, f"{sanitized}.png")
        plt.savefig(filepath, format="png", dpi=200)
        plt.close()
        print(f"Generated: {filepath}")

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2]
    csv_path = base / "tools" / "dependency_tools" / "dependency_map.csv"
    output_dir = base / "tools" / "dependency_tools" / "dependency_graphs"
    try:
        edges = load_dependency_map(csv_path)
        generate_graphs(edges, output_dir)
        print(f"[SUCCESS] All dependency graphs saved in: {output_dir}")
    except Exception as e:
        print(f"[ERROR] Failed to generate graphs: {e}")