from pathlib import Path

def find_aimo_root() -> str:
    """
    AIMOプロジェクトのルートディレクトリ（launch.pyがある場所）を探し、そのパスを返す。
    環境がGitHub Actionsなどでパスを特定できない場合、例外に詳細を含めて通知する。
    """
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "launch.py").exists():
            return str(parent)
    msg = (
        "[ERROR] AIMOルートディレクトリが見つかりません。\n"
        "このエラーは通常、`launch.py` が存在しない場所でスクリプトを実行しているか、"
        "`find_aimo_root()` をCI環境で使用している場合に発生します。\n"
        "対処法:\n"
        "1. `launch.py` が正しい場所にあるか確認してください。\n"
        "2. CIなどで `launch.py` が無い場合、`find_aimo_root()` を使わずルートパスを環境変数などで明示指定してください。\n"
        f"現在の探索開始パス: {current_path}"
    )
    raise RuntimeError(msg)
