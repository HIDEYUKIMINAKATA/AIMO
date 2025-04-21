import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
def export_to_markdown(messages, output_path):
    """指定メッセージリストを Markdown に整形して保存"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# AIMOプロジェクトログ出力\n\n")
        for msg in messages:
            role = msg.get("author", {}).get("role", "unknown").upper()
            content = msg.get("message", {}).get("content", {}).get("parts", [""])[0]
            f.write(f"## [{role}]\n{content.strip()}\n\n---\n")
