"""env_autogen.py
S11: APIキー整合確認機構 + 仮想環境整合 + 出力制御拡張

- find_aimo_root() でプロジェクトルート検出
- api_keys ディレクトリ配下の *_key.txt を列挙
- 2段階読み込み (第一引数 path1, path2) に対応
- diagnostic_log.txt に詳細を書き出し
- log_event() で INFO/SUCCESS/ERROR/WARN を出力
- PYTHONPYCACHEPREFIX / MPLCONFIGDIR / HF_HOME を統一管理
"""

import os
from datetime import datetime
from pathlib import Path

REQUIRED_KEYS = [
    "openai_key.txt",
    "claude_key.txt",
    "mixtral_key.txt",
    "gemini_key.txt",
    "imagegen_key.txt",
    "zephyr_key.txt"
]

def find_aimo_root() -> Path:
    """カレントから親方向に AIMO ルートを探索"""
    curr = Path(__file__).resolve()
    for _ in range(5):
        if (curr / 'api_keys').exists():
            return curr
        curr = curr.parent
    return Path(__file__).resolve().parent

ROOT = find_aimo_root()
API_DIR = ROOT / 'api_keys'
LOG_DIR = ROOT / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)
DIAG_PATH = LOG_DIR / 'diagnostic_log.txt'

# 追加: 出力先制御 (キャッシュ・ログ等)
os.environ["PYTHONPYCACHEPREFIX"] = str(ROOT / "__pycache__")
os.environ["MPLCONFIGDIR"] = str(ROOT / "__config__" / "matplotlib")
os.environ["HF_HOME"] = str(ROOT / "__cache__" / "hf")

def log_event(level: str, message: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{level}] {timestamp} | {message}"
    print(line)
    with open(LOG_DIR / 'env_autogen.log', 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def read_key_multi(filename: str):
    path = API_DIR / filename
    if not path.exists():
        log_event('ERROR', f'API key file missing: {filename}')
        return None
    with open(path, encoding='utf-8') as f:
        data = f.read().strip()
    second = Path(data)
    if second.exists():
        with open(second, encoding='utf-8') as f2:
            data = f2.read().strip()
        log_event('INFO', f'Loaded nested key for {filename}')
    return data

def diagnose():
    results = {}
    for fn in REQUIRED_KEYS:
        key_val = read_key_multi(fn)
        results[fn] = 'OK' if key_val else 'MISSING'
    with open(DIAG_PATH, 'w', encoding='utf-8') as d:
        for k, v in results.items():
            d.write(f"{k}: {v}\n")
    if all(v == 'OK' for v in results.values()):
        log_event('SUCCESS', 'All API keys present')
    else:
        log_event('WARN', 'Some API keys are missing - see diagnostic_log.txt')

if __name__ == '__main__':
    log_event('INFO', 'env_autogen diagnostic start')
    diagnose()
