import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
def filter_conversations_by_id(data, target_ids):
    """conversations.json の mapping から target_ids に含まれる会話だけ抽出"""
    filtered = []
    mapping = data.get("mapping", {})
    for convo in mapping.values():
        if isinstance(convo, dict) and convo.get("conversation_id") in target_ids:
            filtered.append(convo)
    return filtered
