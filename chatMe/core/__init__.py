'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:30:50
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 18:30:53
FilePath: /ChatMe/ai_voice_assistant/core/__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
核心功能模块
"""

from .dialogue import DialogueManager
from .recognition import SpeechRecognizer

__all__ = [
    'DialogueManager',
    'SpeechRecognizer'
]