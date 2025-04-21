# summary_loader_test.py
from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from memory.summary.summary_loader import load_summaries

def main():
    root = find_aimo_root()
    log_event("[INFO]", f"AIMOルート確認: {root}")
    
    try:
        summaries = load_summaries()
        if summaries:
            log_event("[SUCCESS]", f"{len(summaries)} 件の要約を読み込みました")
            for item in summaries:
                log_event("[INFO]", f"出典: {item.get('source')} / 要約: {item.get('summary')}")
        else:
            log_event("[WARN]", "読み込まれた要約はありませんでした")
    except Exception as e:
        log_event("[ERROR]", f"要約読み込み失敗: {e}")

if __name__ == "__main__":
    main()
