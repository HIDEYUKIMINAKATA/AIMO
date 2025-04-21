"""
core/bootstrap.py – パス初期化テンプレート
このモジュールを import または先頭で実行することで、
AIMOルートを sys.path に追加し、core や ai_nodes モジュールが import 可能になります。
"""

import sys
from pathlib import Path

try:
    from core.logger import log_event
except ImportError:
    def log_event(level, msg, category=None): print(f"[{level}] {msg}")

def init_path():
    current_file = Path(__file__).resolve()
    aimo_root = None
    for parent in current_file.parents:
        if (parent / "launch.py").is_file() and (parent / "api_keys").is_dir():
            aimo_root = parent
            log_event("[INFO]", f"AIMOルート検出: {aimo_root}", category="bootstrap")
            break
    if aimo_root is None:
        log_event("[ERROR]", "AIMOルートが見つかりません（launch.py と api_keys が必要です）", category="bootstrap")
        raise RuntimeError("AIMOルートが見つかりません（launch.py と api_keys が必要です）")

    sys.path.append(str(aimo_root))
    log_event("[SUCCESS]", f"パス追加完了: {aimo_root}", category="bootstrap")
    return aimo_root

# 実行時に自動でパス追加
AIMO_ROOT = init_path()
