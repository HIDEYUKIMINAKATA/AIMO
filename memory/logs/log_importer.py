"""log_importer.py – JSON/JSONLログを読み込んで対話記録を取り出す"""

import json
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

def import_conversations(filename: str = "conversations.jsonl") -> list[dict]:
    root = Path(find_aimo_root())
    path = root / "logs" / "imports" / filename

    if not path.exists():
        log_event("[ERROR]", f"ログファイルが見つかりません: {path}", category="log_importer")
        return []

    conversations = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    conversations.append(json.loads(line))
        log_event("[SUCCESS]", f"{len(conversations)} 件の対話を読み込みました。", category="log_importer")
    except Exception as e:
        log_event("[ERROR]", f"ログ読み込み失敗: {e}", category="log_importer")
        return []

    return conversations

if __name__ == "__main__":
    logs = import_conversations()
    print(json.dumps(logs[:2], indent=2, ensure_ascii=False))  # ✅ 確認用
