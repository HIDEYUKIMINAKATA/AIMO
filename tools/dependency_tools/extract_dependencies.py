import os
import sys
import ast
import csv
from collections import defaultdict

# ✅ AIMOルート検出
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.insert(0, AIMO_ROOT)

from core.utils.path_utils import find_aimo_root
from core.utils.logger import log_event

AIMO_ROOT = find_aimo_root()

OUTPUT_CSV = os.path.join(AIMO_ROOT, "tools", "dependency_tools", "dependency_map.csv")
TARGET_EXT = ".py"


def extract_imports_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except Exception:
            return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def scan_project_dependencies(root_dir):
    dep_map = defaultdict(list)
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(TARGET_EXT):
                abs_path = os.path.join(subdir, file)
                rel_path = os.path.relpath(abs_path, AIMO_ROOT)
                imports = extract_imports_from_file(abs_path)
                dep_map[rel_path] = imports
    return dep_map


def save_dependencies_to_csv(dep_map, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Source File", "Imported Module"])
        for file, imports in dep_map.items():
            for imp in imports:
                writer.writerow([file, imp])


if __name__ == "__main__":
    log_event("=== AIMO Dependency Extraction Start ===", "INFO")
    dep_map = scan_project_dependencies(AIMO_ROOT)
    save_dependencies_to_csv(dep_map, OUTPUT_CSV)
    log_event(f"Dependency map saved to {OUTPUT_CSV}", "SUCCESS")
