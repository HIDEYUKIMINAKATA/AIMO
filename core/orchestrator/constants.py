"""
constants.py – AIMO定数定義モジュール

このモジュールはグローバルで使用する定数群を一元的に管理します。
ログ出力カテゴリやAI名、タイムアウト秒数、ディレクトリ名などを定義します。
"""

# 共通ログカテゴリ
CATEGORY_DISPATCHER = "dispatcher"
CATEGORY_ROUTE = "route"
CATEGORY_VOICE = "voice"
CATEGORY_IMAGE = "image"
CATEGORY_CONFIG = "config"
CATEGORY_EVAL = "eval"
CATEGORY_SETUP = "setup"

# デフォルトタイムアウト（秒）
DEFAULT_TIMEOUT = 60
TTS_TIMEOUT = 45
TRANSCRIBE_TIMEOUT = 60

# モデル名
MODEL_ZEPHYR = "zephyr"
MODEL_MIXTRAL = "mixtral"
MODEL_GEMINI = "gemini"
MODEL_CLAUDE = "claude"
MODEL_GPT = "gpt"
MODEL_SUMMARIZER = "summarizer"

# API キーファイル名（api_keys フォルダ内）
KEYFILE_OPENAI = "openai_key.txt"
KEYFILE_CLAUDE = "claude_key.txt"
KEYFILE_MIXTRAL = "mixtral_key.txt"
KEYFILE_GEMINI = "gemini_key.txt"
KEYFILE_IMAGEGEN = "imagegen_key.txt"
KEYFILE_ZEPHYR = "zephyr_key.txt"

# デフォルト拡張子
DEFAULT_AUDIO_EXT = ".wav"
DEFAULT_IMAGE_EXT = ".png"

# プロンプトキーワード（prefix判定用）
PREFIX_IMAGE = "画像"
PREFIX_AUDIO = "音声"
PREFIX_MULTIMODAL = "統合"
PREFIX_ANALYSIS = "解析"

# その他
AIMO_NAME = "AIMO v2.2.10"
AIMO_AUTHOR = "AIMO Team"
