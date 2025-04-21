import argparse
from core.find_aimo_root import find_aimo_root
from core.logger import log_event
import os, sys

# ✅ パス解決 & sys.path 拡張
ROOT = find_aimo_root()
sys.path.append(str(ROOT))

# ✅ 各機能モジュールのインポート
from memory.logs.log_importer import import_conversations
from memory.logs.conversation_filter import filter_by_id
from memory.logs.markdown_exporter import export_to_markdown
from memory.summary.summary_loader import load_summaries

def main():
    parser = argparse.ArgumentParser(description="AIMO Memory Console")
    parser.add_argument("--log-id", type=str, help="ログIDで抽出・出力（Markdown保存）")
    parser.add_argument("--summary", action="store_true", help="保存された要約を表示")

    args = parser.parse_args()
    log_event("[INFO]", "AIMO Memory Console 起動")

    if args.log_id:
        log_event("[INFO]", f"ログ抽出ID指定あり: {args.log_id}")
        logs = import_conversations("conversations.jsonl")
        filtered = filter_by_id(logs, conv_id=args.log_id)
        export_to_markdown(filtered, filename=f"log_{args.log_id}.md")

    elif args.summary:
        log_event("[INFO]", "要約表示モード起動")
        summaries = load_summaries()
        for entry in summaries:
            print("-" * 40)
            print(f"[SUMMARY] {entry.get('title', '(No Title)')}")
            print(entry.get("text", ""))
            print()

    else:
        log_event("[WARN]", "引数なし：処理対象がありません。--log-id または --summary を指定してください")

if __name__ == "__main__":
    main()
