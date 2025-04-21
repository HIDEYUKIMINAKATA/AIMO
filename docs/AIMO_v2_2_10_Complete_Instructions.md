# AIMO v2.2.10 完全指令書（S1〜S13 + 構成照合付き）

本指令書は、AIMO v2.2.10 の構築における全13ステップ（S1〜S13）を、正確かつ段階的に構築・検証・納品するための完全テンプレートです。  
各ステップでは、指定されたファイル／モジュールを出力し、それぞれの**「含まれるべき構成」と照合して、不備の有無を検証**してください。

---

## 🔹 共通構成指示（全ステップ共通）

- `find_aimo_root()` によるルートパス解決を使用
- `log_event()` による `[INFO]`, `[SUCCESS]`, `[ERROR]`, `[WARN]` ログ出力をすべての処理に含めること
- 各ステップで構成に不備がある場合は `[ERROR]`, `[WARN]` としてログ出力し、詳細を明記
- 不備がなければ `[SUCCESS] Sx構築完了` を明示

---

## 📘 指令セット S1〜S13

### ✅ S1：起動構造・ディスパッチャ構成
- 出力対象: `launch.py`, `dispatcher.py`
- 初期フォルダ作成: `logs/`, `memory/`, `api_keys/`
- 構成照合対象: 上記ファイルと各ディレクトリの存在と内容初期化

### ✅ S2：AIルーティング構成
- 出力対象: `route_ai.py`
- 構成照合: 優先順位ロジックとルーティング記述の正当性チェック

### ✅ S3：Zephyr優先化・ログ保証構成
- 出力対象: `hf_text_handler.py`
- 構成照合: APIキー2段構成、タイムアウト60秒、log_event対応

### ✅ S4：意味ベクトル記憶の導入
- 出力対象: `vector_memory.py`
- 構成照合: FAISSとsentence-transformersの記述、memory_vector.jsonとの連携

### ✅ S5：AI評価スコアリング構造
- 出力対象: `evaluator.py`
- 構成照合: 複数AI出力の評価・選出構造とスコア付け処理

### ✅ S6：ログ構造の全統一
- 出力対象: `logger.py`
- 構成照合: 全モジュールのlog_event()への対応確認

### ✅ S7：env_autogen診断強化
- 出力対象: `env_autogen.py`
- 構成照合: APIキー診断・diagnostic_log.txtの出力処理

### ✅ S8：自動改善機構（auto_improve）
- 出力対象: `auto_improve.py`
- 構成照合: 仮適用→本採用の改善ループ構造、log差分記録

### ✅ S9：復元構造（restore_backup）
- 出力対象: `restore_backup.py`
- 構成照合: ZIP保存処理と復元処理、log_event対応

### ✅ S10：テスト構造の導入
- 出力対象: `tests/test_*.py`
- 構成照合: pytest構造に準拠したテストファイルの存在と記述内容

### ✅ S11：APIキー整合確認機構
- 出力対象: `env_autogen.py`
- 構成照合: すべての `api_keys/xxx_key.txt` の存在と2段読み込み処理

### ✅ S12：会話履歴処理モジュール
- 出力対象: `log_importer.py`, `conversation_filter.py`, `markdown_exporter.py`
- 構成照合: `logs/imports/`, `logs/aimobot_conversations/` フォルダと連動動作の確認

### ✅ S13：最終統合テストと納品構造
- 出力対象: `AIMO_Enterprise_v2.2.10_xxx.zip`
- 構成照合: launch→dispatcher→AI応答→記憶→ログ→改善までの統合テストログと AIMO_OVERVIEW.md の存在確認

---

この指令に従って、すべての構成要素が揃い、不備なく段階的に出力されることを求めます。
