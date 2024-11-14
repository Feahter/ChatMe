'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:35:36
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 18:35:40
FilePath: /ChatMe/ai_voice_assistant/core/recognition.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
语音识别模块
"""

import speech_recognition as sr
import numpy as np
from typing import Optional, Dict, Any
import logging
from ..exceptions import RecognitionError, AudioDeviceError
from ..config import Config

class SpeechRecognizer:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or Config()
        self.recognizer = sr.Recognizer()
        self.logger = logging.getLogger(__name__)
        
        # 配置识别器参数
        self.recognizer.energy_threshold = self.config.ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        self._setup_microphone()
    
    def _setup_microphone(self):
        """初始化麦克风"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        except Exception as e:
            raise AudioDeviceError(f"麦克风初始化失败: {str(e)}")
    
    def _check_volume(self, audio_data: np.ndarray) -> bool:
        """检查音量是否足够"""
        rms = np.sqrt(np.mean(np.square(audio_data)))
        return rms > self.config.MINIMUM_VOLUME
    
    def listen(self) -> Optional[str]:
        """
        监听并识别语音
        
        Returns:
            str: 识别的文本，如果识别失败返回None
        
        Raises:
            RecognitionError: 识别过程出错
            AudioDeviceError: 音频设备错误
        """
        try:
            with self.microphone as source:
                self.logger.info("正在监听...")
                audio = self.recognizer.listen(
                    source,
                    timeout=self.config.LISTEN_TIMEOUT,
                    phrase_time_limit=self.config.PHRASE_TIMEOUT
                )
                
                # 检查音量
                if not self._check_volume(np.frombuffer(audio.frame_data, np.int16)):
                    self.logger.warning("音量太小")
                    return None
                
                self.logger.info("正在识别...")
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.config.SPEECH_LANGUAGE,
                    show_all=False
                )
                
                self.logger.info(f"识别结果: {text}")
                return text
                
        except sr.WaitTimeoutError:
            self.logger.warning("监听超时")
            return None
        except sr.UnknownValueError:
            self.logger.warning("无法识别语音")
            return None
        except sr.RequestError as e:
            raise RecognitionError(f"语音识别服务错误: {str(e)}")
        except Exception as e:
            raise RecognitionError(f"识别过程出错: {str(e)}")
    
    def adjust_for_ambient_noise(self):
        """调整环境噪音"""
        try:
            with self.microphone as source:
                self.logger.info("正在调整环境噪音...")
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=self.config.AMBIENT_DURATION
                )
        except Exception as e:
            raise AudioDeviceError(f"环境噪音调整失败: {str(e)}")