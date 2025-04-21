import os
import csv
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def visualize_dependencies(input_csv, output_png):
    G = nx.DiGraph()
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = [name.strip().lower() for name in reader.fieldnames]

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
            G.add_edge(src, tgt)

    # 可視化設定
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.15, iterations=30)
    nx.draw(G, pos, with_labels=True, node_size=300, font_size=6, arrows=True, edge_color='gray')
    plt.title("AIMO Dependency Graph", fontsize=14)
    plt.savefig(output_png, format="png", dpi=300)
    plt.close()

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2]
    input_path = base / "tools" / "dependency_tools" / "dependency_map.csv"
    output_path = base / "tools" / "dependency_tools" / "dependency_graph.png"
    try:
        visualize_dependencies(input_path, output_path)
        print(f"[SUCCESS] Dependency graph saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to visualize dependencies: {e}")