'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:33:12
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 20:19:58
FilePath: /ChatMe/chatMe/exceptions.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
AI Voice Assistant Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

定义所有自定义异常类。
"""

class AssistantError(Exception):
    """AI语音助手基础异常类"""
    def __init__(self, message: str = None, *args, **kwargs):
        self.message = message or "AI语音助手发生错误"
        super().__init__(self.message, *args)

class NetworkError(AssistantError):
    """网络相关错误"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message or "网络连接错误", *args)

class AudioDeviceError(AssistantError):
    """音频设备错误"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message or "音频设备错误", *args)

class RecognitionError(AssistantError):
    """语音识别错误"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message or "语音识别失败", *args)

class SynthesisError(AssistantError):
    """语音合成错误"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message or "语音合成失败", *args)

class APIError(AssistantError):
    """API调用错误"""
    def __init__(self, message: str = None, status_code: int = None, *args, **kwargs):
        self.status_code = status_code
        message = message or f"API调用失败 (状态码: {status_code})"
        super().__init__(message, *args)

class ConfigError(AssistantError):
    """配置错误"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message or "配置错误", *args)

class CacheError(AssistantError):
    """缓存错误"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message or "缓存操作失败", *args)

class ResourceError(AssistantError):
    """资源错误"""
    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(message or "资源访问失败", *args)

class ValidationError(AssistantError):
    """数据验证错误"""
    def __init__(self, message: str = None, field: str = None, *args, **kwargs):
        self.field = field
        message = message or f"数据验证失败 (字段: {field})"
        super().__init__(message, *args)