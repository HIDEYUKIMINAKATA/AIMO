"""
file_utils.py – AIMO共通ファイルユーティリティ

機能:
- テキストファイル読み書き
- JSONファイル読み書き
- ファイル存在チェック
- 全てにログ出力対応 ([INFO], [SUCCESS], [ERROR])

依存:
- find_aimo_root() によるルート解決
- log_event() によるログ出力
"""

import json
from pathlib import Path
from typing import Optional
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

# プロジェクトルートの取得
ROOT = Path(find_aimo_root())

def read_text_file(path: Path) -> Optional[str]:
    log_event("[INFO]", f"テキスト読込開始: {path}", category="file")
    try:
        content = path.read_text(encoding="utf-8")
        log_event("[SUCCESS]", f"テキスト読込成功 ({len(content)}文字)", category="file")
        return content
    except Exception as e:
        log_event("[ERROR]", f"テキスト読込失敗: {e}", category="file")
        return None

def write_text_file(path: Path, content: str) -> bool:
    log_event("[INFO]", f"テキスト書込開始: {path}", category="file")
    try:
        path.write_text(content, encoding="utf-8")
        log_event("[SUCCESS]", f"テキスト書込成功: {path}", category="file")
        return True
    except Exception as e:
        log_event("[ERROR]", f"テキスト書込失敗: {e}", category="file")
        return False

def read_json_file(path: Path) -> Optional[dict]:
    log_event("[INFO]", f"JSON読込開始: {path}", category="file")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        log_event("[SUCCESS]", f"JSON読込成功: {path}", category="file")
        return data
    except Exception as e:
        log_event("[ERROR]", f"JSON読込失敗: {e}", category="file")
        return None

def write_json_file(path: Path, data: dict) -> bool:
    log_event("[INFO]", f"JSON書込開始: {path}", category="file")
    try:
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        log_event("[SUCCESS]", f"JSON書込成功: {path}", category="file")
        return True
    except Exception as e:
        log_event("[ERROR]", f"JSON書込失敗: {e}", category="file")
        return False

def file_exists(path: Path) -> bool:
    exists = path.exists()
    log_event("[INFO]", f"存在チェック: {path} → {exists}", category="file")
    return exists
