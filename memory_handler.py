"""
memory_handler.py – AIMO 記憶統合モジュール（logs・summary・cache 等を統括）

- AIMOルートを自己検出（find_aimo_root）
- 各memoryモジュールを統合管理
- すべての操作に [INFO], [SUCCESS], [ERROR] ログを付加
"""

from core.find_aimo_root import find_aimo_root
from core.logger import log_event

from memory.logs.log_importer import import_conversations
from memory.logs.conversation_filter import filter_by_id
from memory.logs.markdown_exporter import export_to_markdown

from memory.summary.summary_saver import save_summary
from memory.summary.summary_loader import load_summary

from memory.cache.cache_checker import is_cached, update_cache

from pathlib import Path

ROOT = find_aimo_root()

def export_log_by_id(logfile: str, conv_id: str, output_file: str) -> None:
    log_event("[INFO]", f"ログ抽出開始: {logfile} / ID={conv_id}")
    try:
        logs = import_conversations(logfile)
        filtered = filter_by_id(logs, conv_id)
        export_to_markdown(filtered, filename=output_file)
        log_event("[SUCCESS]", f"Markdown出力完了: {output_file}")
    except Exception as e:
        log_event("[ERROR]", f"ログ抽出処理失敗: {e}")

def save_conversation_summary(conv_id: str, summary: str) -> None:
    log_event("[INFO]", f"要約保存開始: {conv_id}")
    try:
        save_summary(conv_id, summary)
        log_event("[SUCCESS]", f"要約保存完了: ID={conv_id}")
    except Exception as e:
        log_event("[ERROR]", f"要約保存失敗: {e}")

def load_conversation_summary(conv_id: str) -> str:
    log_event("[INFO]", f"要約読込開始: {conv_id}")
    try:
        summary = load_summary(conv_id)
        log_event("[SUCCESS]", f"要約読込成功: ID={conv_id}")
        return summary
    except Exception as e:
        log_event("[ERROR]", f"要約読込失敗: {e}")
        return ""

def check_and_update_cache(text: str) -> bool:
    log_event("[INFO]", f"キャッシュ確認開始 | len(text)={len(text)}")
    try:
        if is_cached(text):
            log_event("[SUCCESS]", "既存キャッシュに一致")
            return True
        update_cache(text)
        log_event("[SUCCESS]", "新規キャッシュ登録")
        return False
    except Exception as e:
        log_event("[ERROR]", f"キャッシュチェック失敗: {e}")
        return False
