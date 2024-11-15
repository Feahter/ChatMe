'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:33:12
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 21:23:51
FilePath: /ChatMe/chatMe/exceptions.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
异常定义模块
"""

class AssistantError(Exception):
    """助手基础异常类"""
    pass

class NetworkError(AssistantError):
    """网络错误"""
    pass

class AudioDeviceError(AssistantError):
    """音频设备错误"""
    pass

class RecognitionError(AssistantError):
    """语音识别错误"""
    pass

class SynthesisError(AssistantError):
    """语音合成错误"""
    pass

class APIError(AssistantError):
    """API调用错误"""
    pass

class ConfigError(AssistantError):
    """配置错误"""
    pass

class DialogueError(AssistantError):
    """对话管理错误"""
    pass

class ValidationError(AssistantError):
    """验证错误"""
    pass

class StateError(AssistantError):
    """状态错误"""
    pass

class ResourceError(AssistantError):
    """资源错误"""
    pass

class CacheError(AssistantError):
    """缓存错误"""
    pass

class MonitoringError(AssistantError):
    """监控错误"""
    pass

# 导出所有异常类
__all__ = [
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