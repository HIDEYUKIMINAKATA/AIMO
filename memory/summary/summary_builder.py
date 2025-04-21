"""
summary_builder.py – 保存された要約データを読み込み、AIに再要約を依頼する。
再要約後の結果は summary_saver.py により保存される。
"""

import os
from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from memory.summary.summary_loader import load_summaries
from memory.summary.summary_saver import save_summary
from ai_nodes.zephyr_handler import generate_text as zephyr_generate

def summarize_all_unsummarized():
    root = find_aimo_root()
    log_event("INFO", f"要約ビルダー起動 | AIMOルート: {root}", category="summary")

    try:
        summaries = load_summaries()
        log_event("INFO", f"要約ディレクトリ確認: {os.path.join(root, 'memory', 'summary')}", category="summary")
        log_event("SUCCESS", f"要約ファイル読み込み完了（{len(summaries)}件）", category="summary")

        for idx, entry in enumerate(summaries, 1):
            prompt_id = entry.get("id", f"unknown_{idx}")
            original_summary = entry.get("text", "")
            model = entry.get("model", "Unknown")
            log_event("INFO", f"[{idx}] 要約開始 | source={prompt_id} | len={len(original_summary)}", category="summary")

            try:
                log_event("INFO", f"Zephyr スタブ実行開始: {original_summary}", category="summary")
                ai_summary = zephyr_generate(original_summary, max_tokens=256)
                log_event("SUCCESS", "Zephyr 応答生成成功", category="summary")
                save_summary(prompt_id=prompt_id, ai_model="Zephyr", summary_text=ai_summary)
            except Exception as e:
                log_event("ERROR", f"Zephyr 要約失敗: {e}", category="summary")
    except Exception as e:
        log_event("ERROR", f"要約ビルダーで致命的エラー: {e}", category="summary")

if __name__ == "__main__":
    summarize_all_unsummarized()
