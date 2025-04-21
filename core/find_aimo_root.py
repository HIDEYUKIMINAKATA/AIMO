from pathlib import Path

try:
    from core.logger import log_event
except ImportError:
    def log_event(level, message, category=None): print(f"[{level}] {message}")

def find_aimo_root() -> str:
    """
    AIMOプロジェクトのルートパスを特定する。
    判定条件: launch.py と api_keys フォルダが両方存在するディレクトリ
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        launch = parent / "launch.py"
        keys = parent / "api_keys"
        if launch.is_file() and keys.is_dir():
            log_event("[INFO]", f"AIMOルート特定成功: {parent}", category="core")
            return str(parent)
    
    msg = "AIMOルートが特定できません。launch.py と api_keys を確認してください。"
    log_event("[ERROR]", msg, category="core")
    raise RuntimeError(msg)
