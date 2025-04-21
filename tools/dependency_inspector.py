import os
import ast
from collections import defaultdict
import pandas as pd

def find_python_files(root_dir):
    py_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                py_files.append(full_path)
    return py_files

def extract_dependencies(py_file):
    try:
        with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
            node = ast.parse(f.read(), filename=py_file)
        imports = []
        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    imports.append(alias.name)
            elif isinstance(n, ast.ImportFrom):
                if n.module:
                    imports.append(n.module)
        return imports
    except Exception:
        return []

def build_dependency_map(aimo_root="."):
    dependency_map = defaultdict(list)
    py_files = find_python_files(aimo_root)

    for path in py_files:
        rel_path = os.path.relpath(path, aimo_root)
        dependencies = extract_dependencies(path)
        for dep in dependencies:
            if dep.startswith("core") or dep.startswith("memory") or dep.startswith("ai_nodes") or dep.startswith("scripts"):
                dependency_map[rel_path].append(dep)

    return dependency_map

def export_dependency_report(dependency_map, output_csv="dependency_map.csv"):
    df = pd.DataFrame([
        {"File": k, "Depends On": dep}
        for k, deps in dependency_map.items()
        for dep in deps
    ])
    df.to_csv(output_csv, index=False)
    print(f"[SUCCESS] 依存マップを {output_csv} に保存しました。")

if __name__ == "__main__":
    aimo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dep_map = build_dependency_map(aimo_root)
    export_dependency_report(dep_map)
