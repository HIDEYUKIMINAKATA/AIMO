"""summary_builder.py – 対話ログの要約生成と保存"""

import sys
from pathlib import Path

from core.find_aimo_root import find_aimo_root
from core.logger import log_event

from memory.logs.log_importer import import_conversations
from memory.logs.conversation_filter import filter_by_id
from ai_nodes.summarizer_hub import summarize_text

def summarize_conversation(conv_id: str):
    log_event("[INFO]", f"要約処理開始 | ID: {conv_id}", category="summary")

    root = Path(find_aimo_root())
    input_path = root / "logs" / "imports" / "conversations.jsonl"
    output_dir = root / "logs" / "summaries"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"summary_{conv_id}.txt"

    try:
        conversations = import_conversations(input_path)
        filtered = filter_by_id(conversations, conv_id=conv_id)
        text_to_summarize = "\n".join([entry["content"] for entry in filtered])
        summary = summarize_text(text_to_summarize)

        output_path.write_text(summary, encoding="utf-8")
        log_event("[SUCCESS]", f"要約出力完了: {output_path}", category="summary")
    except Exception as e:
        log_event("[ERROR]", f"要約処理失敗: {e}", category="summary")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summary_builder.py <conversation_id>")
        sys.exit(1)
    summarize_conversation(sys.argv[1])
