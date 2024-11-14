'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:37:28
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 18:37:31
FilePath: /ChatMe/ai_voice_assistant/core/synthesis.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
语音合成模块
"""

import pyttsx3
from typing import Optional, Dict, Any
import logging
from ..exceptions import SynthesisError
from ..config import Config

class SpeechSynthesizer:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self._init_engine()
    
    def _init_engine(self):
        """初始化语音引擎"""
        try:
            self.engine = pyttsx3.init()
            self._configure_engine()
        except Exception as e:
            raise SynthesisError(f"语音引擎初始化失败: {str(e)}")
    
    def _configure_engine(self):
        """配置语音引擎参数"""
        self.engine.setProperty('rate', self.config.SPEECH_RATE)
        self.engine.setProperty('volume', self.config.SPEECH_VOLUME)
        
        # 设置声音
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if self.config.SPEECH_LANGUAGE in voice.languages:
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text: str):
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            
        Raises:
            SynthesisError: 语音合成失败
        """
        if not text:
            return
            
        try:
            self.logger.info(f"正在合成语音: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            raise SynthesisError(f"语音合成失败: {str(e)}")
    
    def save_to_file(self, text: str, filename: str):
        """
        将合成的语音保存到文件
        
        Args:
            text: 要转换的文本
            filename: 输出文件名
            
        Raises:
            SynthesisError: 保存失败
        """
        try:
            self.logger.info(f"正在保存语音到文件: {filename}")
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
        except Exception as e:
            raise SynthesisError(f"语音保存失败: {str(e)}")
    
    def stop(self):
        """停止当前语音输出"""
        try:
            self.engine.stop()
        except Exception as e:
            self.logger.error(f"停止语音失败: {str(e)}")