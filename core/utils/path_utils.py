import os
from pathlib import Path

def find_aimo_root():
    """
    AIMO プロジェクトのルートを探します。
    - GitHub Actions 環境（CI）: core と tools ディレクトリの存在のみチェック
    - ローカル開発環境       : core, tools, launch.py, api_keys を確認
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "core").is_dir() and (parent / "tools").is_dir():
            if os.getenv("GITHUB_ACTIONS") == "true":
                return str(parent)
            if (parent / "launch.py").exists() and (parent / "api_keys").is_dir():
                return str(parent)
            raise RuntimeError(
                "[AIMOルート特定失敗] ローカル実行時は launch.py と api_keys/ の存在を確認してください。"
            )
    raise RuntimeError("[AIMOルート特定失敗] core/ または tools/ ディレクトリが見つかりません。プロジェクト構成を確認してください。")
