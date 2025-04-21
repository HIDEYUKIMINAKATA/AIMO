import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from pathlib import Path

here = Path(__file__).resolve()
print(f"\n🧭 スクリプトの場所: {here}")
for i, parent in enumerate(here.parents):
    print(f"[{i}] 🔎 チェック対象: {parent}")
    lp = parent / "launch.py"
    ak = parent / "api_keys"
    print(f"   └ launch.py 存在: {lp.exists()}")
    print(f"   └ api_keys 存在 : {ak.exists()}")
