
import sys
import os
import ast
import csv
import argparse
from collections import defaultdict
from pathlib import Path

# ✅ AIMOルート補完
current_file = Path(__file__).resolve()
aimo_root = current_file.parents[2]
sys.path.insert(0, str(aimo_root))

from core.utils.logger import log_event

EXCLUDE_DIRS = {'venv', '__pycache__', '.git', 'tests', 'node_modules'}
TARGET_EXT = ".py"

def should_exclude(path, exclude_dirs):
    return any(part in exclude_dirs for part in Path(path).parts)

def extract_imports_from_file(filepath, base_path=None):
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=filepath)
    except Exception as e:
        raise RuntimeError(f"Parse error: {filepath} ({e})")

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                full_name = resolve_relative_import(filepath, node.level, node.module, base_path)
                if full_name:
                    imports.append(full_name)
    return imports

def resolve_relative_import(filepath, level, module, base_path):
    if level == 0:
        return module

    current = Path(filepath).parent
    for _ in range(level):
        current = current.parent
    rel_module_path = current.relative_to(base_path).as_posix().replace('/', '.')
    return f"{rel_module_path}.{module}" if module else rel_module_path

def scan_project_dependencies(root_dir, exclude_dirs, log_warn):
    dep_map = defaultdict(list)
    root_dir = os.path.abspath(root_dir)
    for subdir, _, files in os.walk(root_dir):
        if should_exclude(subdir, exclude_dirs):
            continue
        for file in files:
            if file.endswith(TARGET_EXT):
                abs_path = os.path.join(subdir, file)
                rel_path = os.path.relpath(abs_path, root_dir).replace(os.sep, '/')
                try:
                    imports = extract_imports_from_file(abs_path, base_path=root_dir)
                    dep_map[rel_path] = imports
                except Exception as e:
                    if log_warn:
                        log_event(f"[WARN] {e}", "WARN")
    return dep_map

def save_dependencies_to_csv(dep_map, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Source File", "Imported Module"])
        for file, imports in dep_map.items():
            for imp in imports:
                writer.writerow([file, imp])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Python import dependencies into CSV.")
    parser.add_argument("--root", default=".", help="Root directory to scan.")
    parser.add_argument("--output", default="dependency_map.csv", help="Output CSV file path.")
    parser.add_argument("--exclude", default=",".join(EXCLUDE_DIRS), help="Comma-separated list of directories to exclude.")
    parser.add_argument("--log-warn", action="store_true", help="Enable warning logs for parse failures.")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    output_csv = os.path.abspath(args.output)
    exclude_dirs = set(args.exclude.split(","))

    log_event("=== AIMO Dependency Extraction Start ===", "INFO")
    dep_map = scan_project_dependencies(root, exclude_dirs, args.log_warn)
    save_dependencies_to_csv(dep_map, output_csv)
    log_event(f"Dependency map saved to {output_csv}", "SUCCESS")
