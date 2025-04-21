"""
memory_handler.py – AIMO記憶ログ統合インターフェース

本モジュールは、ログの読み込み・抽出・出力などを一括で制御する。
"""

from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

from memory.logs.log_importer import import_conversations
from memory.logs.conversation_filter import filter_by_id
from memory.logs.markdown_exporter import export_to_markdown

def handle_log_export(log_id: str, output_filename: str = None) -> str:
    """指定されたログIDに対するMarkdown出力を実行"""
    try:
        root = Path(find_aimo_root())
        input_path = root / "logs" / "imports" / "conversations.jsonl"
        output_path = root / "logs" / "aimobot_conversations"

        log_event("[INFO]", f"読み込み対象: {input_path}", category="memory")
        conversations = import_conversations(str(input_path))

        log_event("[INFO]", f"フィルタ実行: ID={log_id}", category="memory")
        filtered = filter_by_id(conversations, conv_id=log_id)

        if not output_filename:
            output_filename = f"log_{log_id}.md"
        output_file = output_path / output_filename

        log_event("[INFO]", f"Markdown出力先: {output_file}", category="memory")
        export_to_markdown(filtered, filename=str(output_file))

        log_event("[SUCCESS]", f"ログ出力完了: {output_file}", category="memory")
        return f"[SUCCESS] ログ出力成功: {output_file}"

    except Exception as e:
        log_event("[ERROR]", f"ログ出力失敗: {e}", category="memory")
        return f"[ERROR] ログ出力失敗: {e}"


if __name__ == "__main__":
    import sys
    _id = sys.argv[1] if len(sys.argv) > 1 else "test_id"
    result = handle_log_export(log_id=_id)
    print(result)
