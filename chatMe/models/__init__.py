'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:44:29
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 18:44:31
FilePath: /ChatMe/ai_voice_assistant/models/__init__.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
AI Voice Assistant Models
~~~~~~~~~~~~~~~~~~~~~~~

模型定义模块。
"""

from .assistant import Assistant, AssistantState, AssistantConfig

__all__ = [
    'Assistant',
    'AssistantState',
    'AssistantConfig'
]