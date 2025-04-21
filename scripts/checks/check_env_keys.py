# scripts/checks/check_env_keys.py
import os
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from dotenv import dotenv_values

def check_env_keys():
    root = Path(find_aimo_root())
    env_path = root / ".env"
    key_dir = root / "api_keys"

    log_event("[INFO]", f".envパス確認: {env_path}")
    log_event("[INFO]", f"APIキー格納ディレクトリ: {key_dir}")

    if not env_path.exists():
        log_event("[ERROR]", ".env ファイルが存在しません。")
        return

    if not key_dir.exists():
        log_event("[ERROR]", "api_keys ディレクトリが存在しません。")
        return

    # .env 読み込み
    env_vars = dotenv_values(env_path)
    log_event("[SUCCESS]", f".env から読み込まれたキー数: {len(env_vars)}")

    # 各APIキーとの整合チェック
    for keyfile in key_dir.glob("*.txt"):
        try:
            lines = keyfile.read_text(encoding="utf-8").strip().splitlines()
            keys_in_file = [line.strip() for line in lines if line.strip()]
            filename = keyfile.stem.upper()

            if not keys_in_file:
                log_event("[WARN]", f"{keyfile.name} に有効なAPIキーが見つかりませんでした")
                continue

            # .env に含まれているか？
            found_match = any(key in env_vars.values() for key in keys_in_file)

            if found_match:
                log_event("[SUCCESS]", f"{keyfile.name} のAPIキーが .env に登録されています")
            else:
                log_event("[ERROR]", f"{keyfile.name} のAPIキーが .env に見つかりません")

        except Exception as e:
            log_event("[ERROR]", f"{keyfile.name} の検査中にエラー: {e}")

if __name__ == "__main__":
    log_event("[INFO]", "=== AIMO .env/APIキー 整合性チェッカー 開始 ===")
    check_env_keys()
    log_event("[INFO]", "=== チェック完了 ===")
