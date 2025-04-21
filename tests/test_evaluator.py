from core.evaluator import evaluate_responses

def test_evaluate_responses():
    responses = {
        "AI-A": "今日はいい天気です",
        "AI-B": "エラーが発生しました",
    }
    scores = evaluate_responses(responses, reference="今日はいい天気ですね")
    assert len(scores) == 2
