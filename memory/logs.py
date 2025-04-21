# init_memory_logs.py

from pathlib import Path
from datetime import datetime

def log_event(level: str, message: str, category: str = "memory.logs") -> None:
    """共通ログ出力関数"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{level}] {now} | {category} | {message}")

def init_memory_logs_dir(base_path: Path) -> Path:
    """memory/logs/ 以下のサブフォルダを自動生成"""
    logs_root = base_path / "memory" / "logs"
    logs_root.mkdir(parents=True, exist_ok=True)

    subdirs = ["raw", "exported", "filtered"]
    for sub in subdirs:
        path = logs_root / sub
        path.mkdir(exist_ok=True)
        log_event("[INFO]", f"ディレクトリ確認: {path}", category="memory.logs")

    return logs_root

# 使用例
if __name__ == "__main__":
    ROOT = Path(__file__).resolve().parent
    init_memory_logs_dir(ROOT)
