"""
image_handler.py – SDXL画像生成（画像を自動表示付き）
生成後に画像を自動で開く（Windows環境専用）
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv

from core.find_aimo_root import find_aimo_root
from core.logger import log_event

# 🔹 環境変数から API キーを取得
load_dotenv()
HF_IMAGE_KEY = os.getenv("HF_IMAGE_KEY")

# 🔹 モデル・デバイス設定
MODEL_NAME = "stabilityai/stable-diffusion-2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_pipe = None
def _get_pipe():
    global _pipe
    if _pipe is None:
        log_event("[INFO]", f"画像生成モデルを初期化中（デバイス: {DEVICE}）", category="imagegen")
        try:
            _pipe = StableDiffusionPipeline.from_pretrained(
                MODEL_NAME,
                use_auth_token=HF_IMAGE_KEY,
                torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
            ).to(DEVICE)
            log_event("[SUCCESS]", "画像生成モデルの初期化完了", category="imagegen")
        except Exception as e:
            log_event("[ERROR]", f"モデル初期化失敗: {e}", category="imagegen")
            raise RuntimeError(f"モデル初期化失敗: {e}")
    return _pipe

def generate_image(prompt: str) -> str:
    log_event("[INFO]", f"画像生成処理開始: {prompt}", category="imagegen")
    try:
        root = find_aimo_root()
        img_dir = root / "output" / "images"
        img_dir.mkdir(parents=True, exist_ok=True)

        filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img_path = img_dir / filename

        pipe = _get_pipe()
        log_event("[INFO]", f"画像生成プロンプト受信: {prompt}", category="imagegen")
        result = pipe(prompt)
        image = result.images[0]
        image.save(img_path)

        log_event("[SUCCESS]", f"画像生成成功: {img_path}", category="imagegen")

        # 🔹 Windows環境で画像を自動で開く
        if os.name == "nt":
            try:
                subprocess.Popen(['start', str(img_path)], shell=True)
                log_event("[INFO]", f"画像自動表示開始: {img_path}", category="imagegen")
            except Exception as e:
                log_event("[WARN]", f"画像自動表示失敗: {e}", category="imagegen")

        return f"[IMAGE] {filename}"
    except Exception as e:
        log_event("[ERROR]", f"画像生成失敗: {e}", category="imagegen")
        return f"[ERROR] 画像生成に失敗しました: {e}"
