"""
主模块测试
"""

import pytest
from unittest.mock import patch, MagicMock
from chatMe import (
    VoiceAssistant,
    ChatMe,
    AssistantError,
    NetworkError,
    AudioDeviceError,
    RecognitionError,
    SynthesisError
)
from chatMe.models.assistant import AssistantState
from chatMe.core.providers import AIProvider

def test_assistant_initialization(assistant):
    """测试助手初始化"""
    assert assistant is not None
    assert assistant.state == AssistantState.IDLE
    assert assistant.config.name == 'Test Assistant'
    assert assistant.config.language == 'zh-CN'

def test_assistant_start_stop(assistant):
    """测试助手启动和停止"""
    # 模拟用户说"再见"
    assistant.recognizer.listen.return_value = "再见"
    
    # 启动助手
    assistant.start()
    
    # 验证调用
    assistant.synthesizer.speak.assert_called_with("你好，我是Test Assistant")
    assistant.synthesizer.speak.assert_called_with("再见！")
    assert assistant.state == AssistantState.TERMINATED

def test_assistant_conversation_flow(assistant):
    """测试对话流程"""
    # 模拟正常对话
    assistant.recognizer.listen.side_effect = [
        "你好",
        "今天天气怎么样",
        "再见"
    ]
    
    assistant.dialogue_manager.get_response.side_effect = [
        "你好！有什么我可以帮你的吗？",
        "今天是晴天，气温25度。",
    ]
    
    # 启动助手
    assistant.start()
    
    # 验证对话流程
    assert assistant.dialogue_manager.get_response.call_count == 2
    assert assistant.synthesizer.speak.call_count == 4  # 包括开场和结束语

def test_assistant_error_handling(assistant):
    """测试错误处理"""
    # 模拟错误
    assistant.recognizer.listen.side_effect = Exception("测试错误")
    
    # 验证错误处理
    with pytest.raises(AssistantError) as exc_info:
        assistant.start()
    
    assert "助手运行错误" in str(exc_info.value)
    assert assistant.state == AssistantState.ERROR

@pytest.mark.asyncio
async def test_assistant_performance_monitoring(assistant, performance_data):
    """测试性能监控"""
    # 启用性能监控
    assistant.config.enable_performance_monitoring = True
    
    with patch('chatMe.utils.monitoring.PerformanceMonitor') as mock_monitor:
        # 设置mock返回值
        mock_monitor.return_value.get_performance_report.return_value = performance_data
        
        # 重新初始化助手
        assistant._init_components()
        
        # 获取性能报告
        report = assistant.get_status()['performance']
        
        assert report == performance_data
        assert 'cpu_percent' in report
        assert 'memory_percent' in report

def test_assistant_conversation_history(assistant, sample_conversation):
    """测试对话历史管理"""
    # 设置模拟对话历史
    assistant.dialogue_manager.get_history.return_value = sample_conversation
    
    # 保存对话历史
    with patch('builtins.open', MagicMock()) as mock_file:
        assistant.save_conversation_history()
        
        # 验证文件操作
        mock_file.assert_called_once()
        
    # 验证对话历史内容
    history = assistant.dialogue_manager.get_history()
    assert len(history) == 4
    assert history[0]['role'] == 'user'
    assert history[0]['content'] == '你好'

def test_assistant_config_validation(test_config):
    """测试配置验证"""
    # 测试无效配置
    invalid_config = test_config.copy()
    invalid_config['max_conversation_history'] = -1
    
    with pytest.raises(ValueError):
        VoiceAssistant(invalid_config)
    
    # 测试缺失必要配置
    incomplete_config = test_config.copy()
    del incomplete_config['language']
    
    with pytest.raises(KeyError):
        VoiceAssistant(incomplete_config)

def test_assistant_resource_cleanup(assistant, temp_dir):
    """测试资源清理"""
    # 设置临时文件路径
    conversation_file = f"{temp_dir}/conversation_history.json"
    performance_file = f"{temp_dir}/performance_report.json"
    
    # 执行清理
    with patch('builtins.open', MagicMock()) as mock_file:
        assistant.cleanup()
        
        # 验证文件操作
        assert mock_file.call_count == 1  # 只保存对话历史，因为性能监控被禁用

def test_assistant_context_manager(assistant):
    """测试上下文管理器"""
    with patch.object(assistant, 'cleanup') as mock_cleanup:
        with assistant:
            pass
        
        # 验证清理被调用
        mock_cleanup.assert_called_once()

@pytest.mark.parametrize("input_text,expected_response", [
    ("你好", "你好！有什么我可以帮你的吗？"),
    ("再见", None),
    (None, None),
])
def test_assistant_responses(assistant, input_text, expected_response):
    """测试不同输入的响应"""
    assistant.recognizer.listen.return_value = input_text
    if expected_response:
        assistant.dialogue_manager.get_response.return_value = expected_response
    
    if input_text == "再见":
        assistant.start()
        assert assistant.state == AssistantState.TERMINATED
    else:
        assistant.start()
        if expected_response:
            assistant.dialogue_manager.get_response.assert_called_with(input_text)

def test_voice_assistant_initialization():
    """测试助手初始化"""
    assistant = VoiceAssistant()
    assert assistant is not None
    assert hasattr(assistant, 'recognizer')
    assert hasattr(assistant, 'engine')

def test_error_handling():
    """测试错误处理"""
    with pytest.raises(AssistantError):
        raise AssistantError("测试错误")
        
    with pytest.raises(NetworkError):
        raise NetworkError("网络错误")
        
    with pytest.raises(AudioDeviceError):
        raise AudioDeviceError("音频设备错误")
        
    with pytest.raises(RecognitionError):
        raise RecognitionError("语音识别错误")
        
    with pytest.raises(SynthesisError):
        raise SynthesisError("语音合成错误")

def test_environment_check(env_setup):
    """测试环境检查"""
    assistant = VoiceAssistant()
    assert assistant._check_environment() is None

def test_voice_engine_setup():
    """测试语音引擎设置"""
    assistant = VoiceAssistant()
    assert assistant.engine is not None
    assert assistant.engine.getProperty('rate') > 0
    assert 0 <= assistant.engine.getProperty('volume') <= 1.0

@pytest.mark.asyncio
async def test_async_operations():
    """测试异步操作"""
    assistant = VoiceAssistant()
    response = await assistant.get_ai_response_async("你好")
    assert isinstance(response, str)
    assert len(response) > 0

class MockProvider(AIProvider):
    def generate_response(self, prompt: str, **kwargs):
        return "Mock response"
        
    def validate_config(self, config):
        return True

def test_chat_with_provider():
    """测试ChatMe基本功能"""
    provider = MockProvider()
    chat = ChatMe(provider=provider)
    
    response = chat.chat("Hello")
    assert response == "Mock response"
    
def test_chat_without_provider():
    """测试没有提供者的情况"""
    chat = ChatMe()
    with pytest.raises(ValueError):
        chat.chat("Hello")