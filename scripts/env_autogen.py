"""AIMO v2.2.10 - S7 env_autogen.py
診断用スクリプト: APIキーの存在チェックと diagnostic_log.txt 出力

共通仕様:
 - find_aimo_root() でプロジェクトルートを検出
 - log_event() によりログ統一出力 ([INFO], [SUCCESS], [WARN], [ERROR])
 - logs/diagnostic_log.txt に結果を追記
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import os
from datetime import datetime
from pathlib import Path

# --- Fallback-safe imports -------------------------
try:
    from core.find_aimo_root import find_aimo_root
except ImportError:
    def find_aimo_root() -> str:
        return str(Path(__file__).resolve().parents[2])

try:
    from core.logger import log_event
except ImportError:
    def log_event(level: str, message: str, category: str = "diagnostic"):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{level} {ts} {message}")

# --- 定数定義 -------------------------------------
ROOT = Path(find_aimo_root())
API_DIR = ROOT / "api_keys"
LOG_DIR = ROOT / "logs" / "system"
DIAG_PATH = LOG_DIR / "diagnostic_log.txt"

REQUIRED_KEYS = {
    "claude_key.txt": "Claude",
    "gemini_key.txt": "Gemini",
    "mixtral_key.txt": "Mixtral",
    "openai_key.txt": "GPT / LLaMA",
    "imagegen_key.txt": "Image generation",
    "zephyr_key.txt": "Zephyr"
}

# --- メイン処理 -----------------------------------
def run_diagnostic() -> None:
    log_event("[INFO]", "env_autogen.py start", category="diagnostic")
    missing = []
    lines = []

    for fname, desc in REQUIRED_KEYS.items():
        fpath = API_DIR / fname
        if fpath.exists():
            content = fpath.read_text(encoding="utf-8").strip()
            if len(content) > 10:
                lines.append(f"{fname}: FOUND ({desc}) - OK")
                log_event("[SUCCESS]", f"{desc} キー OK: {fname}", category="diagnostic")
            else:
                lines.append(f"{fname}: FOUND ({desc}) - EMPTY OR SHORT")
                log_event("[ERROR]", f"{desc} キーが空または不正です: {fname}", category="diagnostic")
                missing.append(fname)
        else:
            lines.append(f"{fname}: MISSING ({desc})")
            log_event("[WARN]", f"{desc} キーが見つかりません: {fname}", category="diagnostic")
            missing.append(fname)

    # ログ出力と保存
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(DIAG_PATH, "a", encoding="utf-8") as f:
        f.write(f"=== Diagnostic {timestamp} ===\n")
        f.write("\n".join(lines) + "\n\n")

    # 結果メッセージ
    if missing:
        log_event("[WARN]", f"{len(missing)} 件のキーが不足または不正: {', '.join(missing)}", category="diagnostic")
    else:
        log_event("[SUCCESS]", "すべてのAPIキーが有効です", category="diagnostic")

# --- 実行可能 -------------------------------------
if __name__ == "__main__":
    run_diagnostic()
