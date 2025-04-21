"""
summary_toolkit.py - AIMO memory/summary ユーティリティ統合モジュール

要約の読み込み・保存・検索（ID, キーワード, 日付）などの高レベル操作を提供
"""

from memory.summary.summary_loader import load_summaries
from memory.summary.summary_saver import save_summary
from memory.summary.summary_filter import (
    filter_by_id,
    filter_by_keyword,
    filter_by_date
)
from core.logger import log_event

def find_summary_by_id(summary_id: str):
    summaries = load_summaries()
    return filter_by_id(summaries, summary_id)

def find_summaries_by_keyword(keyword: str):
    summaries = load_summaries()
    return filter_by_keyword(summaries, keyword)

def find_summaries_by_date(date_str: str):
    summaries = load_summaries()
    return filter_by_date(summaries, date_str)

def save_new_summary(summary_text: str, metadata: dict = None):
    save_summary(summary_text, metadata or {})

# CLIテスト用
if __name__ == "__main__":
    log_event("[INFO]", "summary_toolkit CLI test")
    result = find_summaries_by_keyword("重要")
    for s in result:
        print(f"- {s.get('id')}: {s.get('summary')}")
