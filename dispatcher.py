"""Dispatcher (S1) – AIMO 起動応答・ログ保存処理"""

import os
from datetime import datetime
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from route_ai import route  # ✅ 追加

# ルートおよび出力先の初期化
ROOT = Path(find_aimo_root())
OUTPUT_DIR = ROOT / "output" / "ai_nodes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def dispatch_from_input(input_path: str | Path) -> str:
    input_path = Path(input_path)

    if not input_path.exists():
        msg = "入力ファイルが存在しません。"
        log_event("[ERROR]", msg, category="dispatcher")
        return f"[ERROR] {msg}"

    command = input_path.read_text(encoding="utf-8").strip()
    if not command:
        msg = "入力が空です。"
        log_event("[ERROR]", msg, category="dispatcher")
        return f"[ERROR] {msg}"

    # ✅ AIルーティングを呼び出す
    try:
        response = route(command)
    except Exception as e:
        log_event("[ERROR]", f"AIルーティング失敗: {e}", category="dispatcher")
        return f"[ERROR] AIルーティング失敗: {e}"

    # 出力を保存
    (OUTPUT_DIR / "last_output.txt").write_text(response, encoding="utf-8")

    # ログを記録
    log_event("[SUCCESS]", "S1 dispatcher executed successfully", category="dispatcher")
    return response
