from dispatcher import dispatch_from_input
import os

def test_dispatcher_with_valid_input(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("こんにちは")
    result = dispatch_from_input(str(test_file))
    assert "Received" in result or "応答" in result
