"""
测试配置和通用fixture
"""

import pytest
import os
import tempfile
from typing import Generator, Dict, Any
from unittest.mock import MagicMock
from chatMe.main import VoiceAssistant
from chatMe.core.recognition import SpeechRecognizer
from chatMe.core.synthesis import SpeechSynthesizer
from chatMe.core.dialogue import DialogueManager
from chatMe.config import Config

@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """提供临时目录"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def test_config() -> Dict[str, Any]:
    """测试配置"""
    return {
        'name': 'Test Assistant',
        'language': 'zh-CN',
        'voice_id': 'test_voice',
        'wake_words': ['你好', '助手'],
        'max_conversation_history': 5,
        'auto_adjust_noise': False,
        'enable_performance_monitoring': False,
        'SPEECH_RATE': 150,
        'SPEECH_VOLUME': 1.0,
        'ENERGY_THRESHOLD': 300,
        'AMBIENT_DURATION': 1,
        'LISTEN_TIMEOUT': 5,
        'PHRASE_TIMEOUT': 3,
        'API_TIMEOUT': 10,
        'MAX_RETRIES': 3,
        'CACHE_SIZE': 100,
    }

@pytest.fixture
def mock_recognizer() -> MagicMock:
    """模拟语音识别器"""
    recognizer = MagicMock(spec=SpeechRecognizer)
    recognizer.listen.return_value = "测试输入"
    return recognizer

@pytest.fixture
def mock_synthesizer() -> MagicMock:
    """模拟语音合成器"""
    synthesizer = MagicMock(spec=SpeechSynthesizer)
    return synthesizer

@pytest.fixture
def mock_dialogue_manager() -> MagicMock:
    """模拟对话管理器"""
    dialogue_manager = MagicMock(spec=DialogueManager)
    dialogue_manager.get_response.return_value = "测试响应"
    return dialogue_manager

@pytest.fixture
def assistant(test_config: Dict[str, Any],
             mock_recognizer: MagicMock,
             mock_synthesizer: MagicMock,
             mock_dialogue_manager: MagicMock) -> VoiceAssistant:
    """创建测试用助手实例"""
    config = Config(**test_config)
    assistant = VoiceAssistant(config)
    
    # 替换为mock组件
    assistant.recognizer = mock_recognizer
    assistant.synthesizer = mock_synthesizer
    assistant.dialogue_manager = mock_dialogue_manager
    
    return assistant

@pytest.fixture
def env_setup() -> Generator[None, None, None]:
    """设置测试环境变量"""
    original_env = dict(os.environ)
    
    # 设置测试环境变量
    os.environ.update({
        'OPENAI_API_KEY': 'test_key',
        'SPEECH_LANGUAGE': 'zh-CN',
        'SPEECH_RATE': '150',
        'SKIP_ENV_CHECK': 'true'
    })
    
    yield
    
    # 恢复原始环境变量
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def sample_conversation() -> list:
    """示例对话数据"""
    return [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什么我可以帮你的吗？"},
        {"role": "user", "content": "今天天气怎么样？"},
        {"role": "assistant", "content": "抱歉，我无法获取实时天气信息。"},
    ]

@pytest.fixture
def performance_data() -> Dict[str, float]:
    """示例性能数据"""
    return {
        'cpu_percent': 25.5,
        'memory_percent': 45.2,
        'network_bytes_sent': 1024,
        'network_bytes_recv': 2048,
        'disk_usage_percent': 65.8
    }

@pytest.fixture
def speech_recognizer():
    return SpeechRecognizer()

@pytest.fixture
def dialogue_manager():
    return DialogueManager()