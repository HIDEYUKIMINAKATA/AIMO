#!/usr/bin/env python3
# check_aimo_setup.py
"""
AIMO 完全構成チェックスクリプト

以下を検査します：
- プロジェクトルート直下の必須ディレクトリ／ファイル存在
- ai_nodes 以下のハンドラモジュール読み込み可否
- input/cli, input/audio, output/ai_nodes, output/audio, api_keys, core, scripts, logs, memory ディレクトリ存在
- api_keys/*.txt が空でないか
- .env ファイルの整合性
- 仮想環境内での依存ライブラリ（requirements.txt）のインストール状況
"""

import os
import sys
import importlib
from pathlib import Path
import pkgutil
import subprocess

# —————— 設定 ——————
REQUIRED_DIRS = [
    "ai_nodes",
    "core",
    "api_keys",
    os.path.join("input", "cli"),
    os.path.join("input", "audio"),
    os.path.join("output", "ai_nodes"),
    os.path.join("output", "audio"),
    "logs",
    "memory",
]
REQUIRED_FILES = [
    "dispatcher.py",
    "route_ai.py",
    "launch.py",
    "env_autogen.py",
    "requirements.txt",
]
API_KEY_FILES = [
    "openai_key.txt",
    "claude_key.txt",
    "mixtral_key.txt",
    "gemini_key.txt",
    "imagegen_key.txt",
    "zephyr_key.txt",
]
HANDLER_MODULES = [
    "ai_nodes.mixtral_handler",
    "ai_nodes.gemini_handler",
    "ai_nodes.zephyr_handler",
    "ai_nodes.claude_handler",
    "ai_nodes.gpt_handler",
    "ai_nodes.summarizer_hub",
    "ai_nodes.hf_image_handler",
    "ai_nodes.voice_handler",
    "ai_nodes.cogvlm_handler",
]

def find_root() -> Path:
    # このスクリプトから見たプロジェクトルート
    return Path(__file__).resolve().parent

def check_dirs(root: Path):
    print("■ ディレクトリ構成チェック")
    ok = True
    for d in REQUIRED_DIRS:
        p = root / d
        status = "OK" if p.is_dir() else "MISSING"
        if status != "OK": ok = False
        print(f"  {d:<20} : {status}")
    return ok

def check_files(root: Path):
    print("\n■ ファイル存在チェック")
    ok = True
    for f in REQUIRED_FILES:
        p = root / f
        status = "OK" if p.is_file() else "MISSING"
        if status != "OK": ok = False
        print(f"  {f:<20} : {status}")
    return ok

def check_api_keys(root: Path):
    print("\n■ API キー整合チェック (api_keys/*.txt)")
    api_dir = root / "api_keys"
    ok = True
    for fn in API_KEY_FILES:
        p = api_dir / fn
        if p.is_file() and p.stat().st_size > 10:
            status = "OK"
        elif p.is_file():
            status = "EMPTY"
            ok = False
        else:
            status = "MISSING"
            ok = False
        print(f"  {fn:<20} : {status}")
    return ok

def check_handlers():
    print("\n■ AIハンドラ モジュール読み込みチェック")
    ok = True
    for mod in HANDLER_MODULES:
        spec = pkgutil.find_loader(mod)
        status = "OK" if spec else "FAIL"
        if status != "OK": ok = False
        print(f"  {mod:<30} : {status}")
    return ok

def check_env_file(root: Path):
    print("\n■ .env ファイルチェック")
    env = root / ".env"
    if not env.is_file():
        print("  .env                : MISSING")
        return False
    lines = env.read_text(encoding="utf-8").splitlines()
    filled = [l for l in lines if "=" in l and not l.strip().startswith("#")]
    print(f"  .env lines          : {len(lines)} lines, {len(filled)} アクティブエントリ")
    if len(filled) < len(API_KEY_FILES):
        print("  ⚠ .env に登録されているキーが不足しています")
        return False
    return True

def check_requirements(root: Path):
    print("\n■ requirements.txt インストール状態チェック")
    req = root / "requirements.txt"
    if not req.is_file():
        print("  requirements.txt    : MISSING")
        return False
    # pip に問い合わせ（仮想環境で実行されている想定）
    try:
        out = subprocess.check_output([sys.executable, "-m", "pip", "check"], stderr=subprocess.STDOUT)
        lines = out.decode().splitlines()
        if lines:
            print("  pip check warnings:")
            for l in lines:
                print("   ", l)
            return False
        else:
            print("  pip check           : OK")
            return True
    except Exception as e:
        print("  pip check failed    :", e)
        return False

def main():
    root = find_root()
    print(f"AIMO セットアップチェッカー\nProject root: {root}\n")
    results = []
    results.append(check_dirs(root))
    results.append(check_files(root))
    results.append(check_api_keys(root))
    results.append(check_handlers())
    results.append(check_env_file(root))
    results.append(check_requirements(root))

    print("\n■ 総合結果:", "PASS" if all(results) else "FAIL")
    sys.exit(0 if all(results) else 1)

if __name__ == "__main__":
    main()
