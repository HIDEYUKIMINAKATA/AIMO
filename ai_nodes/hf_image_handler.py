# ai_nodes/hf_image_handler.py – HuggingFace Image Generation Handler (Stable Diffusion 2)
# AIMO v2.2.10 – 完全ログ + エラーハンドリング + 出力保存パス明示

import os
import requests
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from dotenv import load_dotenv

# .env読み込み
load_dotenv()
API_KEY = os.getenv("HF_IMAGE_KEY")

# 出力パス準備
ROOT = Path(find_aimo_root())
SAVE_DIR = ROOT / "output" / "images"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# 画像生成関数（Stable Diffusion 2）
def generate_image(prompt: str) -> str:
    if not API_KEY:
        log_event("ERROR", "画像生成APIキーが未定義（HF_IMAGE_KEY）")
        return "[ERROR] HuggingFace APIキーが設定されていません。"

    log_event("INFO", f"画像生成リクエスト開始: {prompt[:30]}")

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"inputs": prompt},
            timeout=60
        )

        if response.status_code != 200:
            log_event("ERROR", f"画像生成失敗: {response.status_code} - {response.text[:200]}")
            return f"[ERROR] 画像生成に失敗しました（{response.status_code}）"

        # ファイル名作成と保存処理
        fname = f"image_{prompt[:10].strip().replace(' ', '_')}.png"
        fpath = SAVE_DIR / fname
        fpath.write_bytes(response.content)

        log_event("SUCCESS", f"画像生成成功: {fpath}")
        return f"[IMAGE] {fpath.name}"

    except requests.exceptions.Timeout:
        log_event("ERROR", "画像生成タイムアウト（60秒）")
        return "[ERROR] タイムアウト（60秒）"

    except Exception as e:
        log_event("ERROR", f"画像生成例外: {e}")
        return f"[ERROR] 画像生成中に例外が発生しました: {e}"
