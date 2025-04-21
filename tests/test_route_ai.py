# tests/test_route_ai.py
from route_ai import route

def test_zephyr_stub():
    prompt = "こんにちは"
    out = route(prompt)
    assert "応答" in out or "STUB" in out

def test_gpt_fallback():
    prompt = "普通の英語で話して"
    out = route(prompt)
    assert "応答" in out or "STUB" in out

def test_image_route():
    prompt = "画像 サングラスをかけた猫"
    out = route(prompt)
    assert "[IMAGE]" in out or "画像生成に失敗" in out

def test_voice_route():
    prompt = "音声 テストしてね"
    out = route(prompt)
    assert "[VOICE-STUB]" in out

def test_summary_route():
    prompt = "要約 AIMOは素晴らしいAIです"
    out = route(prompt)
    assert "[SUMMARY-STUB]" in out

def test_cogvlm_route():
    prompt = "統合 この画像を説明して"
    out = route(prompt)
    assert "[COGVLM-STUB]" in out
