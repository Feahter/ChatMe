"""
AI Voice Assistant
~~~~~~~~~~~~~~~~~

一个基于Python的智能语音助手系统。

:copyright: (c) 2024
:license: MIT
"""

from .main import VoiceAssistant
from .exceptions import AssistantError, NetworkError, AudioDeviceError
from .config import Config
from .version import __version__

__all__ = [
    'VoiceAssistant',
    'AssistantError',
    'NetworkError',
    'AudioDeviceError',
    'Config',
    '__version__',
]

# 版本信息
__title__ = 'chatMe'
__description__ = 'An intelligent voice assistant powered by AI'
__url__ = 'https://github.com/Feahter/ChatMe.git'
__author__ = 'Your Name'
__author_email__ = 'your.email@example.com'
__license__ = 'MIT'
__copyright__ = 'Copyright 2024'

# 日志配置
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

def setup_logging(level=logging.INFO):
    """配置日志系统"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# 版本检查
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution(__title__).version
except pkg_resources.DistributionNotFound:
    __version__ = '0.0.0'

# 类型注解支持
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Dict, List, Any

# 环境变量检查
import os
from dotenv import load_dotenv
load_dotenv()

def check_environment():
    """检查必要的环境变量"""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

# 初始化检查
def check_dependencies():
    """检查必要的依赖"""
    try:
        import speech_recognition
        import pyttsx3
        import openai
    except ImportError as e:
        raise ImportError(f"Missing required dependency: {str(e)}")

# 助手实例创建函数
def create_assistant(
    config: Optional[Dict[str, Any]] = None,
    debug: bool = False
) -> 'VoiceAssistant':
    """
    创建语音助手实例
    
    Args:
        config: 可选的配置字典
        debug: 是否启用调试模式
    
    Returns:
        VoiceAssistant实例
    
    Raises:
        AssistantError: 初始化失败时抛出
    """
    if debug:
        setup_logging(logging.DEBUG)
    
    try:
        check_environment()
        check_dependencies()
        return VoiceAssistant(config)
    except Exception as e:
        raise AssistantError(f"Failed to create assistant: {str(e)}")

# 版本信息函数
def get_version() -> str:
    """获取当前版本号"""
    return __version__

# 健康检查函数
def health_check() -> bool:
    """
    执行系统健康检查
    
    Returns:
        bool: 系统是否健康
    """
    try:
        check_environment()
        check_dependencies()
        return True
    except Exception:
        return False