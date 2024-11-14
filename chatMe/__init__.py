'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:22:34
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 21:27:12
FilePath: /ChatMe/chatMe/__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
AI语音助手主模块
"""
import os
import sys
from typing import Dict, Any, Optional

# 版本信息
from .version import __version__

# 导入主要组件
from .main import VoiceAssistant
from .exceptions import (
    AssistantError,
    NetworkError,
    AudioDeviceError,
    RecognitionError,
    SynthesisError,
    APIError,
    ConfigError,
    CacheError,
    ResourceError,
    ValidationError,
    DialogueError
)

# 检查Python版本
if sys.version_info < (3, 8):
    raise RuntimeError("Python 3.8 or higher is required")

# 检查必要的环境变量
def check_environment(
    config: Optional[Dict[str, Any]] = None,
    required_vars: Optional[list] = None
) -> None:
    """
    检查运行环境
    
    Args:
        config: 配置字典
        required_vars: 必需的环境变量列表
    """
    if required_vars is None:
        required_vars = ['OPENAI_API_KEY']
        
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")

# 导出的组件
__all__ = [
    'VoiceAssistant',
    'check_environment',
    '__version__',
    # 异常类
    'AssistantError',
    'NetworkError',
    'AudioDeviceError',
    'RecognitionError',
    'SynthesisError',
    'APIError',
    'ConfigError',
    'CacheError',
    'ResourceError',
    'ValidationError',
    'DialogueError'
]