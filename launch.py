"""AIMO launcher (S1–S3 完全対応版 + 仮想環境制御・ログ整合版)"""

import os
from datetime import datetime
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from dispatcher import dispatch_from_input

# AIMOルート検出
ROOT = Path(find_aimo_root())

# 出力制御オプション（初回実行でもログとキャッシュをAIMO配下に固定）
os.environ["PYTHONPYCACHEPREFIX"] = str(ROOT / "__pycache__")
os.environ["MPLCONFIGDIR"] = str(ROOT / "__config__" / "matplotlib")
os.environ["HF_HOME"] = str(ROOT / "__cache__" / "hf")

# 入力ファイル指定
INPUT_DIR = ROOT / "input" / "cli"
INPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_FILE = INPUT_DIR / "test.txt"

def main():
    log_event("[INFO]", f"AIMO launched  : {datetime.now()}", category="system")
    log_event("[INFO]", f"Input file path: {INPUT_FILE}", category="system")

    result = dispatch_from_input(INPUT_FILE)
    print(f"[RESULT] {result}")

    if "[ERROR]" in result:
        log_event("[ERROR]", "Launch failed due to input error", category="system")
        exit(1)

if __name__ == "__main__":
    main()


