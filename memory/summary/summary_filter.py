"""
summary_filter.py - AIMO memory/summary フィルタモジュール
保存された要約データに対してIDやキーワードで抽出を行う
"""

from typing import List, Dict
from core.logger import log_event

def filter_by_id(summaries: List[Dict], summary_id: str) -> List[Dict]:
    """指定されたIDに一致する要約を抽出"""
    result = [s for s in summaries if s.get("id") == summary_id]
    log_event("[INFO]", f"IDによるフィルター: id={summary_id} → {len(result)}件", category="summary")
    return result

def filter_by_keyword(summaries: List[Dict], keyword: str) -> List[Dict]:
    """本文中に指定キーワードを含む要約を抽出"""
    result = [s for s in summaries if keyword in s.get("summary", "")]
    log_event("[INFO]", f"キーワードフィルター: '{keyword}' → {len(result)}件", category="summary")
    return result

def filter_by_date(summaries: List[Dict], date_str: str) -> List[Dict]:
    """指定された日付文字列（例: '2025-04-19'）で抽出"""
    result = [s for s in summaries if s.get("date", "").startswith(date_str)]
    log_event("[INFO]", f"日付フィルター: {date_str} → {len(result)}件", category="summary")
    return result

# 簡易テスト用CLI実行時
if __name__ == "__main__":
    from summary_loader import load_summaries
    data = load_summaries()
    print(filter_by_keyword(data, "重要"))
