from core.logger import log_event
from core.find_aimo_root import find_aimo_root
from pathlib import Path

def export_to_markdown(conversations: list, filename: str = "export.md") -> None:
    if not conversations:
        log_event("[WARN]", "Markdown出力対象が空です", category="log")
        return

    root = find_aimo_root()
    output_dir = Path(root) / "logs" / "aimobot_conversations"
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / filename
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for entry in conversations:
                f.write(f"### {entry.get('role', 'unknown')}\n")
                f.write(f"{entry.get('content', '')}\n\n")
        log_event("[SUCCESS]", f"Markdownファイル保存成功: {filepath}", category="log")
    except Exception as e:
        log_event("[ERROR]", f"Markdown出力失敗: {e}", category="log")
