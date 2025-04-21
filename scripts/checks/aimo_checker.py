import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
missing_items = []

required_dirs = ['ai_nodes', 'api_keys', 'core', 'input/cli', 'input/audio', 'logs', 'memory', 'output', 'scripts', 'tests']
required_files = ['.env', 'requirements.txt', 'requirements_310.txt', 'launch.py', 'dispatcher.py', 'route_ai.py', 'env_autogen.py', 'README.md']

print("\n=== AIMO 完全構成チェックスクリプト ===")

# フォルダの存在確認
for d in required_dirs:
    path = ROOT / d
    if not path.exists() or not path.is_dir():
        missing_items.append(f"[DIR] tests")

# ファイルの存在確認
for f in required_files:
    path = ROOT / f
    if not path.exists() or not path.is_file():
        missing_items.append(f"[FILE] input/audio/sample2.wav")

if missing_items:
    print("\n[ERROR] 以下の項目が不足・欠落しています：")
    for item in missing_items:
        print(" -", item)
    print("\n→ 不足ファイル・フォルダを確認・復旧してください。")
else:
    print("\n[SUCCESS] AIMO の構成は完全です。すべての必須ファイル・フォルダが揃っています。")
