"""
cli_parser.py – AIMO CLI入力整形ユーティリティ

用途:
- コマンドライン引数の標準化
- ファイル or 直接プロンプト入力を自動判定
- すべての処理にログ出力を含む

設計:
- AIMOルート自動検出
- ログ: [INFO], [SUCCESS], [ERROR]
"""

import sys
from pathlib import Path
from typing import Optional
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

def parse_cli_input() -> Optional[str]:
    log_event("[INFO]", "CLI引数解析開始", category="cli")

    if len(sys.argv) < 2:
        log_event("[WARN]", "引数が指定されていません", category="cli")
        return None

    arg = sys.argv[1].strip()
    if not arg:
        log_event("[ERROR]", "空の引数が渡されました", category="cli")
        return None

    if Path(arg).is_file():
        log_event("[INFO]", f"ファイルとして認識: {arg}", category="cli")
        try:
            text = Path(arg).read_text(encoding="utf-8").strip()
            log_event("[SUCCESS]", f"ファイル読込成功: {len(text)}文字", category="cli")
            return text
        except Exception as e:
            log_event("[ERROR]", f"ファイル読込エラー: {e}", category="cli")
            return None
    else:
        log_event("[INFO]", "文字列プロンプトとして認識", category="cli")
        return arg
