import os

def find_aimo_root() -> str:
    """
    AIMOプロジェクトのルートディレクトリを自動検出する。
    現在のスクリプト位置から親ディレクトリを順に辿り、
    AIMOルートに含まれる marker ファイル/ディレクトリを基準に判定する。
    """
    current = os.path.abspath(os.path.dirname(__file__))

    while True:
        # AIMOルートと判断できる目印（必ず存在する構成要素）
        candidate = os.path.join(current, "core")
        if os.path.isdir(candidate):
            return current

        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("AIMOルートが検出できませんでした。構成を確認してください。")
        current = parent
