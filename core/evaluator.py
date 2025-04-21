"""
evaluator.py – AIMO v2.2.10 AI応答評価モジュール
- AI出力に対する簡易評価（キーワード一致・長さ等）
- 評価結果を logs/evaluation/ に保存
- 全ステップに log_event による [INFO]/[SUCCESS]/[ERROR] を出力
"""

import os
import re
from datetime import datetime
from pathlib import Path
from core.find_aimo_root import find_aimo_root
from core.logger import log_event

# 評価ログ保存先
ROOT = Path(find_aimo_root())
EVAL_LOG_DIR = ROOT / "logs" / "evaluation"
EVAL_LOG_DIR.mkdir(parents=True, exist_ok=True)

def evaluate_response(prompt: str, response: str) -> dict:
    """
    与えられたプロンプトと応答に対し、簡易的な評価スコアを算出。
    - 応答長スコア
    - キーワード一致スコア
    """
    log_event("[INFO]", "AI応答評価を開始", category="eval")

    try:
        prompt_keywords = set(re.findall(r'\b\w{4,}\b', prompt.lower()))
        response_keywords = set(re.findall(r'\b\w{4,}\b', response.lower()))
        keyword_overlap = prompt_keywords & response_keywords
        keyword_score = len(keyword_overlap) / max(len(prompt_keywords), 1)

        length_score = min(len(response) / 300, 1.0)  # 最大スコア1.0（300文字以上）

        total_score = round((keyword_score + length_score) / 2, 3)

        result = {
            "prompt_len": len(prompt),
            "response_len": len(response),
            "keyword_score": round(keyword_score, 3),
            "length_score": round(length_score, 3),
            "total_score": total_score,
            "timestamp": datetime.now().isoformat()
        }

        # 結果保存
        filename = f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = EVAL_LOG_DIR / filename
        with open(output_path, "w", encoding="utf-8") as f:
            import json
            json.dump(result, f, indent=2, ensure_ascii=False)

        log_event("[SUCCESS]", f"AI応答評価完了 | スコア={total_score}", category="eval")
        return result

    except Exception as e:
        log_event("[ERROR]", f"AI応答評価に失敗: {e}", category="eval")
        return {
            "error": str(e),
            "score": 0.0
        }


# テスト実行用
if __name__ == "__main__":
    sample_prompt = "地球温暖化について説明してください。"
    sample_response = "地球温暖化は温室効果ガスの増加により気温が上昇する現象です。特に二酸化炭素の排出が大きな原因となっています。"

    result = evaluate_response(sample_prompt, sample_response)
    print("[EVAL RESULT]", result)
