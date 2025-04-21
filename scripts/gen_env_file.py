import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from pathlib import Path
from datetime import datetime

# ✅ 明示的に core の find_aimo_root を使う（失敗時は例外で止める）
from core.find_aimo_root import find_aimo_root

ROOT = Path(find_aimo_root())
print(f"[DEBUG] find_aimo_root(): {ROOT}")

KEY_DIR = ROOT / "api_keys"
ENV_PATH = ROOT / ".env"

KEY_MAP = {
    "zephyr_key.txt": "HF_API_KEY",
    "imagegen_key.txt": "HF_IMAGE_KEY",
    "openai_key.txt": "OPENAI_API_KEY",
    "claude_key.txt": "CLAUDE_API_KEY",
    "gemini_key.txt": "GEMINI_API_KEY",
    "mixtral_key.txt": "MIXTRAL_API_KEY"
}

def generate_env_file():
    lines = []
    for fname, env_var in KEY_MAP.items():
        fpath = KEY_DIR / fname
        if fpath.exists():
            key = fpath.read_text(encoding="utf-8").strip()
            if len(key) >= 10:
                lines.append(f"{env_var}={key}")
            else:
                lines.append(f"# {env_var}=  # ⚠ 空ファイルです")
        else:
            lines.append(f"# {env_var}=  # ⚠ 未検出")

    lines.insert(0, f"# .env 自動生成日時: {datetime.now()}")
    ENV_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SUCCESS] .env ファイルを生成しました: {ENV_PATH}")

if __name__ == "__main__":
    generate_env_file()
