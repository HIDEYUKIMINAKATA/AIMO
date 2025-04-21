import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.find_aimo_root import find_aimo_root

root = Path(find_aimo_root())
print(f"[CHECK] AIMOルート検出成功: {root}")
print(f" - launch.py: {(root / 'launch.py').exists()}")
print(f" - api_keys/: {(root / 'api_keys').exists()}")
print(f" - .env 出力先: {root / '.env'}")
