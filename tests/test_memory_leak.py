def test_memory_usage():
    initial_memory = psutil.Process().memory_info().rss
    
    for _ in range(100):
        with VoiceAssistant() as assistant:
            assistant.get_ai_response("测试")
    
    final_memory = psutil.Process().memory_info().rss
    assert (final_memory - initial_memory) < 10 * 1024 * 1024  # 允许10MB增长