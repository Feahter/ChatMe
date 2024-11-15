'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:22:34
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 21:30:29
FilePath: /ChatMe/chatMe/__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
ChatMe - AI语音助手
"""
from .version import __version__
from .main import VoiceAssistant, ChatMe
from .core.providers import AIProvider
from .exceptions import (
    AssistantError,
    NetworkError,
    AudioDeviceError,
    RecognitionError,
    SynthesisError,
    APIError,
    ConfigError,
    DialogueError,
    ValidationError,
    StateError,
    ResourceError,
    CacheError,
    MonitoringError
)

__all__ = [
    'VoiceAssistant',
    'ChatMe',
    'AIProvider',
    '__version__',
    'AssistantError',
    'NetworkError',
    'AudioDeviceError',
    'RecognitionError',
    'SynthesisError',
    'APIError',
    'ConfigError',
    'DialogueError',
    'ValidationError',
    'StateError',
    'ResourceError',
    'CacheError',
    'MonitoringError'
]