# ai_nodes ディレクトリ構成

AIMOにおける各AIノード（モデル）のルーティング・呼び出し処理を担うモジュール群です。

## 概要

このディレクトリには、各種AIモデルと連携するための「ハンドラ」が含まれています。  
それぞれのハンドラは以下の役割を担います。

| ファイル名             | 機能概要                         | 接続対象AI                    |
|------------------------|----------------------------------|-------------------------------|
| `mixtral_handler.py`   | Mixtral 8x7B 経由の主対話AI処理     | OpenRouter（Together）        |
| `zephyr_handler.py`    | HuggingFace Zephyr 7B            | HuggingFace API               |
| `claude_handler.py`    | Claude API 呼び出し（未実装）      | Anthropic                     |
| `gpt_handler.py`       | OpenAI GPT 系呼び出し             | OpenAI API                    |
| `gemini_handler.py`    | Gemini Free API 呼び出し         | Google Gemini                 |
| `summarizer_hub.py`    | モデル横断の要約処理共通モジュール | Zephyr / T5 / BARTなど        |
| `image_handler.py`     | 画像生成（Diffusers）            | HuggingFace Diffusers         |
| `voice_handler.py`     | Whisper＋Coqui音声双方向処理      | Whisper / Coqui               |
| `cogvlm_handler.py`    | 画像＋テキスト統合理解            | CogVLM（THUDM）               |
| `hf_text_handler.py`   | HuggingFace Zephyr用軽量テキスト  | HuggingFace API               |
| `hf_image_handler.py`  | 画像生成用の補助モデル            | HuggingFace API               |

## 補足

- 全てのハンドラには `[INFO]`, `[SUCCESS]`, `[ERROR]` ログ出力が実装されています。
- APIキーは `api_keys/` 以下のテキストファイルから自動読み込みされます。
