"""
env_utils.py – .env ファイルの読み書きと検証処理
AIMO v2.2.10 / coreユーティリティ

機能:
- .env ファイルの存在確認
- 指定キーの読み取り
- キーの書き込み（追記・上書き）
- 全項目の読み込み
- ログ出力を全ステップに実装
"""

import os
from pathlib import Path
from typing import Optional, Dict
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

AIMO_ROOT = Path(find_aimo_root())
ENV_PATH = AIMO_ROOT / ".env"

def check_env_exists() -> bool:
    if ENV_PATH.exists():
        log_event("[INFO]", f".env ファイル検出: {ENV_PATH}", category="env")
        return True
    else:
        log_event("[WARN]", f".env ファイルが存在しません: {ENV_PATH}", category="env")
        return False

def load_env() -> Dict[str, str]:
    env_vars = {}
    if not ENV_PATH.exists():
        log_event("[ERROR]", ".env ファイルが存在しないため読み込めません", category="env")
        return env_vars

    try:
        with open(ENV_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
        log_event("[SUCCESS]", f".env ファイル読込成功（{len(env_vars)}件）", category="env")
    except Exception as e:
        log_event("[ERROR]", f".env 読込失敗: {e}", category="env")

    return env_vars

def get_env_value(key: str) -> Optional[str]:
    env_vars = load_env()
    value = env_vars.get(key)
    if value:
        log_event("[INFO]", f"{key} の値を取得しました", category="env")
    else:
        log_event("[WARN]", f"{key} が .env に存在しません", category="env")
    return value

def set_env_value(key: str, value: str) -> None:
    try:
        lines = []
        updated = False
        if ENV_PATH.exists():
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith(f"{key}="):
                        lines.append(f"{key}={value}\n")
                        updated = True
                    else:
                        lines.append(line)
        if not updated:
            lines.append(f"{key}={value}\n")

        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)

        msg = f"{'更新' if updated else '追記'}完了: {key}={value}"
        log_event("[SUCCESS]", msg, category="env")
    except Exception as e:
        log_event("[ERROR]", f".env 書込失敗: {e}", category="env")
