
"""
auto_improve.py – S8 自動改善モジュール

概要:
1. 最新の error ログを検出し、エラー種別を抽出
2. 改善前にプロジェクト全体を ZIP でバックアップ
3. 既知エラー (例: ModuleNotFoundError) を修復する簡易パッチを適用
4. すべてのステップを log_event() で記録
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import re, datetime, zipfile, shutil
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

ROOT = Path(find_aimo_root())
LOG_DIR = ROOT / "logs" / "error"
BACKUP_DIR = ROOT / "backup"
BACKUP_DIR.mkdir(exist_ok=True)

def latest_error_log():
    files = sorted(LOG_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None

def backup():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = BACKUP_DIR / f"aimo_backup_{ts}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in ROOT.rglob("*"):
            if f.is_file() and BACKUP_DIR not in f.parents:
                zf.write(f, f.relative_to(ROOT))
    log_event("SUCCESS", f"バックアップ完了: {zip_path}")
    return zip_path

def fix_missing_module(module_name:str):
    stub = ROOT / f"{module_name}.py"
    if stub.exists():
        return False
    stub.write_text(f"# Auto-generated stub for missing module '{module_name}'\n")
    log_event("SUCCESS", f"Stub module generated: {stub}")
    return True

def run():
    log_event("INFO", "auto_improve 起動")
    log_path = latest_error_log()
    if not log_path:
        log_event("WARN", "エラーログが存在しません")
        return
    text = log_path.read_text(encoding="utf-8")
    mm = re.search(r"ModuleNotFoundError: No module named '(.+?)'", text)
    if mm:
        module = mm.group(1)
        log_event("INFO", f"欠損モジュール検出: {module}")
        backup()
        if fix_missing_module(module):
            log_event("SUCCESS", "auto_improve 修正完了")
        else:
            log_event("WARN", "修正不要または失敗")
    else:
        log_event("WARN", "既知パターン外のエラー。手動対応が必要")

if __name__ == "__main__":
    run()
