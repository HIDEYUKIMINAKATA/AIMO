# scripts/diagnose_env.py


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.find_aimo_root import find_aimo_root

root = Path(find_aimo_root())
key_file = root / "api_keys" / "claude_key.txt"

print(f"\n🧭 AIMOルート: {root}")
print(f"📁 api_keys ディレクトリ存在: { (root / 'api_keys').exists() }")
print(f"📄 claude_key.txt 存在: { key_file.exists() }")

if key_file.exists():
    content = key_file.read_text(encoding="utf-8").strip()
    print(f"📄 中身の長さ: {len(content)} 文字")
    print(f"📄 内容（先頭20字）: {content[:20]}")
else:
    print("❌ claude_key.txt が見つかりません")
