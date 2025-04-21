from core.find_aimo_root import find_aimo_root
from core.logger import log_event
from pathlib import Path
import os
import sounddevice as sd
import soundfile as sf
import whisper
from TTS.api import TTS

# 📌 モデル初期化（1回のみ）
log_event("[INFO]", "Whisperモデル初期化中...", category="voice")
model = whisper.load_model("base")

log_event("[INFO]", "Coqui TTSモデル初期化中...", category="voice")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# 📁 パス初期化
ROOT = Path(find_aimo_root())
INPUT_AUDIO = ROOT / "input" / "audio"
OUTPUT_AUDIO = ROOT / "output" / "audio"
INPUT_AUDIO.mkdir(parents=True, exist_ok=True)
OUTPUT_AUDIO.mkdir(parents=True, exist_ok=True)

# 🔊 音声再生関数
def play_audio(file_path: str):
    try:
        data, fs = sf.read(file_path)
        log_event("[INFO]", f"音声ファイル読み込み成功: {file_path}", category="voice")
        sd.play(data, fs)
        sd.wait()
        log_event("[SUCCESS]", "音声再生完了", category="voice")
    except Exception as e:
        log_event("[ERROR]", f"音声再生失敗: {e}", category="voice")

# 🎤 音声処理関数
def generate_voice(prompt: str) -> str:
    if not prompt.endswith(".wav") and not prompt.endswith(".mp3"):
        prompt += ".wav"

    # パス解決（絶対・相対両対応）
    audio_path = Path(prompt)
    if not audio_path.is_file():
        audio_path = INPUT_AUDIO / prompt

    if not audio_path.exists():
        msg = f"[ERROR] 入力音声が存在しません: {audio_path}"
        log_event("[ERROR]", msg, category="voice")
        return msg

    log_event("[INFO]", f"音声ハンドラ起動: {audio_path.name}", category="voice")

    # Whisper による文字起こし
    try:
        result = model.transcribe(str(audio_path), fp16=False)
        response = result["text"]
        log_event("[SUCCESS]", f"音声認識成功: {response}", category="voice")
    except Exception as e:
        log_event("[ERROR]", f"音声認識失敗: {e}", category="voice")
        return f"[ERROR] 音声認識に失敗しました: {e}"

    # TTS による読み上げと再生
    try:
        output_path = OUTPUT_AUDIO / f"tts_{audio_path.stem}.wav"
        tts.tts_to_file(text=response, file_path=str(output_path))
        log_event("[SUCCESS]", f"TTS音声出力成功: {output_path}", category="voice")
        play_audio(str(output_path))
    except Exception as e:
        log_event("[ERROR]", f"TTS出力失敗: {e}", category="voice")
        return f"[ERROR] 音声出力に失敗しました: {e}"

    return f"[RESULT] {response}\n[FILE] {output_path}"
