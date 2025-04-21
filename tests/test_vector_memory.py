from memory.vector_memory import VectorMemory

def test_add_and_search_memory():
    vm = VectorMemory()
    vm.add_memory("これはテスト用の記憶です。")
    results = vm.search_memory("テスト")
    assert any("テスト" in text for text, _ in results)
