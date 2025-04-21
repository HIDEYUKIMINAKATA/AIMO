# memory/logs/run_log_export.py

import argparse
from memory.logs.log_importer import import_conversations
from memory.logs.conversation_filter import filter_by_id
from memory.logs.markdown_exporter import export_to_markdown
from core.logger import log_event

def main():
    parser = argparse.ArgumentParser(description="ログIDでMarkdown出力")
    parser.add_argument("--id", type=str, required=True, help="抽出対象の会話ID")
    parser.add_argument("--logfile", type=str, default="conversations.jsonl", help="ログファイル名")
    parser.add_argument("--outfile", type=str, default=None, help="出力ファイル名（省略時は log_<ID>.md）")
    args = parser.parse_args()

    log_event("[INFO]", f"対話ログ読込開始: {args.logfile}")
    conversations = import_conversations(args.logfile)

    log_event("[INFO]", f"会話IDでフィルタリング: {args.id}")
    filtered = filter_by_id(conversations, args.id)

    if not filtered:
        log_event("[WARN]", f"指定IDの対話が見つかりません: {args.id}")
        return

    outfile = args.outfile or f"log_{args.id}.md"
    export_to_markdown(filtered, filename=outfile)
    log_event("[SUCCESS]", f"Markdown出力完了: {outfile}")

if __name__ == "__main__":
    main()
