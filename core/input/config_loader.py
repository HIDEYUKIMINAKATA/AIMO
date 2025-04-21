import os
from pathlib import Path
from typing import Optional, Union
from core.path_utils import find_aimo_root
from core.logger import log_event

# ✅ AIMOルート自動設定
ROOT = find_aimo_root()
CONFIG_FILE = ROOT / "config.json"


def load_env_variables(dotenv_path: Optional[Union[str, Path]] = None) -> int:
    """
    .env ファイルを読み込み、環境変数として設定します。
    """
    from dotenv import load_dotenv

    dotenv_path = Path(dotenv_path) if dotenv_path else ROOT / ".env"
    if not dotenv_path.exists():
        log_event("[ERROR]", f".env ファイルが存在しません: {dotenv_path}", category="config")
        return 0

    try:
        load_dotenv(dotenv_path)
        keys_loaded = sum(1 for k in os.environ if k.strip())
        log_event("[SUCCESS]", f".env 読込成功: {dotenv_path} / 読込キー数: {keys_loaded}", category="config")
        return keys_loaded
    except Exception as e:
        log_event("[ERROR]", f".env 読込中に例外が発生: {e}", category="config")
        return 0


def get_config() -> dict:
    """
    config.json を読み込み辞書として返します。
    """
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            log_event("[SUCCESS]", f"設定ファイル読み込み成功: {CONFIG_FILE}", category="config")
            return config
    except FileNotFoundError:
        log_event("[ERROR]", f"設定ファイルが見つかりません: {CONFIG_FILE}", category="config")
        return {}
    except Exception as e:
        log_event("[ERROR]", f"設定ファイル読み込みエラー: {e}", category="config")
        return {}
