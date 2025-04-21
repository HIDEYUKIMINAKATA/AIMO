import os
import sys

# ✅ パス解決
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.context.context_stacker import stack_context_for_prompt

# 🧪 テスト入力（自由に変更OK）
test_input = "自然エネルギーの将来性について教えてください。"

# ✅ 文脈統合処理の実行
result = stack_context_for_prompt(test_input, top_k=3, threshold=0.4)

# === 統合結果 ===
print("\n=== 統合結果 ===")
print(f"Final Prompt:\n{result['final_prompt']}\n")
print("Context Segments:")
for seg in result["context_segments"]:
    print(f"- Score: {seg['score']:.3f} | Source: {seg['source']}")
    print(f"  Text: {seg['text']}\n")

