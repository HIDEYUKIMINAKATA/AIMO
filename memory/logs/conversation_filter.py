"""conversation_filter.py – 対話ログから特定の条件（IDやキーワード）で抽出"""

from typing import List, Dict
from core.logger import log_event

def filter_by_id(conversations: List[Dict], conv_id: str) -> List[Dict]:
    """指定された会話IDに一致する対話だけを抽出"""
    filtered = [conv for conv in conversations if conv.get("id") == conv_id]
    if filtered:
        log_event("[SUCCESS]", f"ID '{conv_id}' に一致する対話を {len(filtered)} 件抽出", category="conv_filter")
    else:
        log_event("[WARN]", f"ID '{conv_id}' に一致する対話は見つかりませんでした", category="conv_filter")
    return filtered

def filter_by_keyword(conversations: List[Dict], keyword: str) -> List[Dict]:
    """任意のキーワードを含む対話だけを抽出"""
    filtered = []
    for conv in conversations:
        if keyword in json.dumps(conv, ensure_ascii=False):
            filtered.append(conv)
    if filtered:
        log_event("[SUCCESS]", f"キーワード '{keyword}' を含む対話を {len(filtered)} 件抽出", category="conv_filter")
    else:
        log_event("[WARN]", f"キーワード '{keyword}' を含む対話は見つかりませんでした", category="conv_filter")
    return filtered

# ✅ テスト実行用
if __name__ == "__main__":
    from log_importer import import_conversations
    logs = import_conversations()
    filtered = filter_by_id(logs, "abc123")
    print(filtered)
