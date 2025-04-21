# memory/logs/log_toolkit.py

from memory.logs.log_importer import import_conversations
from memory.logs.conversation_filter import filter_by_id
from memory.logs.markdown_exporter import export_to_markdown
from core.logger import log_event

def extract_markdown_from_id(logfile: str, conv_id: str, outfile: str = None) -> str:
    log_event("[INFO]", f"ログ読込: {logfile}")
    conversations = import_conversations(logfile)

    log_event("[INFO]", f"会話ID抽出: {conv_id}")
    filtered = filter_by_id(conversations, conv_id)

    if not filtered:
        msg = f"[ERROR] 会話IDが見つかりません: {conv_id}"
        log_event("[ERROR]", msg)
        return msg

    outfile = outfile or f"log_{conv_id}.md"
    export_to_markdown(filtered, filename=outfile)
    log_event("[SUCCESS]", f"Markdown保存完了: {outfile}")
    return outfile
