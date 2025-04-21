# summary_saver_test.py
import sys
from core.find_aimo_root import find_aimo_root
from memory.summary.summary_saver import save_summary
from core.logger import log_event

def main():
    root = find_aimo_root()
    log_event("[INFO]", f"AIMOルート確認: {root}")

    try:
        # 必須の3引数を正しく渡す
        save_summary(
            prompt_id="abc123",
            ai_model="Claude",
            summary_text="これは summary_saver_test.py によって保存された要約です。"
        )
        log_event("[SUCCESS]", "要約保存テスト完了")
    except Exception as e:
        log_event("[ERROR]", f"要約保存に失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

