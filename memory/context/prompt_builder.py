# memory/context/prompt_builder.py

def build_prompt(context_segments: list, input_text: str) -> str:
    """
    context_segments と input_text を結合し、文脈付きプロンプトを生成する
    """
    try:
        prompt_parts = []
        for i, seg in enumerate(context_segments):
            prefix = f"【文脈{i+1}（{seg['source']}）】"
            prompt_parts.append(f"{prefix}\n{seg['text']}\n")

        prompt_parts.append(f"【現在の質問】\n{input_text}")

        return "\n".join(prompt_parts)

    except Exception as e:
        return f"[ERROR] プロンプト生成失敗: {e}\n\n{input_text}"
