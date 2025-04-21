"""
test_dataset.py - AIMO memory/tests 用テストプロンプト管理

目的:
- テスト用の入力＋期待出力の組を記録
- 検証やベンチマークに使用可能
"""

import json
from datetime import datetime
from pathlib import Path
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

TESTS_DIR = Path(find_aimo_root()) / "memory" / "tests"
TEST_FILE = TESTS_DIR / "test_prompts.jsonl"
TESTS_DIR.mkdir(parents=True, exist_ok=True)

def save_test_case(prompt: str, expected: str, category: str = "general", notes: str = "") -> None:
    """
    テストケースを保存
    """
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "expected": expected,
        "category": category,
        "notes": notes
    }

    try:
        with open(TEST_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log_event("[SUCCESS]", f"テストケース登録: {category}", category="tests")
    except Exception as e:
        log_event("[ERROR]", f"テストケース保存失敗: {e}", category="tests")

def load_test_cases(category_filter: str = None) -> list:
    """
    テストケースを全件読み込み（カテゴリでフィルタ可能）
    """
    if not TEST_FILE.exists():
        return []

    try:
        with open(TEST_FILE, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f if line.strip()]
        if category_filter:
            lines = [entry for entry in lines if entry.get("category") == category_filter]
        log_event("[INFO]", f"テストケース読み込み: {len(lines)}件", category="tests")
        return lines
    except Exception as e:
        log_event("[ERROR]", f"テストケース読み込み失敗: {e}", category="tests")
        return []

# CLIテスト用
if __name__ == "__main__":
    save_test_case("水の沸点は？", "100℃", category="science")
    for case in load_test_cases():
        print(f"[{case['category']}] {case['prompt']} => {case['expected']}")
