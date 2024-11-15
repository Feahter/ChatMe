from speech_recognition import Recognizer, Microphone
import pyttsx3
import openai
import requests
import numpy as np
from functools import lru_cache
from pathlib import Path
import time
import logging
import os
import sys
from typing import Optional, Dict, Any, List
import psutil

from .config import Config, AIConfig
from .utils import filter_sensitive_info
from .utils.monitoring import performance_monitor
import speech_recognition as sr
from .models.assistant import AssistantState
from .core.providers import AIProvider
from .exceptions import (
    AssistantError,
    NetworkError,
    AudioDeviceError,
    RecognitionError,
    SynthesisError,
    APIError,
    ConfigError
)

try:
    import aifc
except ImportError:
    import wave as aifc
    logging.warning("使用 wave 模块替代 aifc")

class ChatMe:
    """简单的聊天接口类"""
    def __init__(self, 
                 provider: Optional[str] = None,
                 config_path: Optional[str] = None,
                 **kwargs):
        """
        Args:
            provider: AI提供者名称，如 'openai'
            config_path: 配置文件路径
            **kwargs: 覆盖配置文件的参数
        """
        self.config = AIConfig(config_path)
        
        # 获取提供者名称
        provider_name = provider or self.config.config.get('default_provider')
        if not provider_name:
            raise ValueError("未指定AI提供者")
            
        # 获取提供者配置
        provider_config = self.config.get_provider_config(provider_name)
        provider_config.update(kwargs)  # 使用kwargs覆盖配置
        
        # 初始化提供者
        self.provider = self._init_provider(provider_name, provider_config)
    
    def _init_provider(self, provider_name: str, config: Dict[str, Any]) -> AIProvider:
        """初始化AI提供者"""
        try:
            provider_config = {
                "type": provider_name,
                "settings": config
            }
            return AIProvider.from_config(provider_config)
        except Exception as e:
            raise ConfigError(f"初始化AI提供者失败: {str(e)}")
    
    def chat(self, message: str) -> str:
        """与AI对话"""
        if not self.provider:
            raise ValueError("未设置AI提供者")
            
        return self.provider.generate_response(message)

class VoiceAssistant:
    def __init__(self, config_path: Optional[str] = None):
        """初始化语音助手
        
        Args:
            config_path: 配置文件路径
        """
        self.config = AIConfig(config_path)
        self.state = AssistantState.IDLE
        
        self._init_logging()
        if os.getenv('SKIP_ENV_CHECK') != 'true':
            self._check_environment()
        
        # 初始化组件
        self.recognizer = Recognizer()
        self.engine = pyttsx3.init()
        self._setup_voice_engine()
        
        # 初始化AI提供者
        provider_name = self.config.config.get('default_provider')
        if not provider_name:
            raise ConfigError("未指定默认AI提供者")
            
        provider_config = self.config.get_provider_config(provider_name)
        self.provider = self._init_provider(provider_name, provider_config)
        
        self.conversation_history = []
    
    def _init_provider(self, provider_name: str, config: Dict[str, Any]) -> AIProvider:
        """初始化AI提供者"""
        try:
            provider_config = {
                "type": provider_name,
                "settings": config
            }
            return AIProvider.from_config(provider_config)
        except Exception as e:
            raise ConfigError(f"初始化AI提供者失败: {str(e)}")
    
    def _init_logging(self):
        """初始化日志系统"""
        log_file = Path("logs/assistant.log")
        log_file.parent.mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    def _setup_voice_engine(self):
        """
        初始化语音引擎
        """
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.config.speech_rate)
            self.engine.setProperty('volume', self.config.volume)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if self.config.language in voice.languages:
                    self.engine.setProperty('voice', voice.id)
                    break
        except Exception as e:
            raise SynthesisError(f"语音引擎初始化失败: {str(e)}")

    def _get_optimal_voice(self):
        """选择最优的语音引擎"""
        voices = self.engine.getProperty('voices')
        return next((v for v in voices if 'chinese' in v.languages), voices[0])
    
    @performance_monitor
    def get_ai_response(self, user_input):
        """添加性能监控装饰器"""
        if psutil.cpu_percent() > 80:
            logging.warning("CPU负载过高，可能影响响应时间")
        return self._cached_ai_response(user_input)
        
    def _check_environment(self):
        """环境检查"""
        # 检查API密钥
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("未设置OpenAI API密钥")
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # 检查网络连接
        if not self._check_network():
            raise ConnectionError("网络连接不可用")
            
        # 检查音频设备
        self._check_audio_devices()

    def _check_network(self):
        """检查网络连接"""
        try:
            requests.get("https://api.openai.com", timeout=Config.NETWORK_TIMEOUT)
            return True
        except:
            logging.error("网络连接失败")
            raise NetworkError("网络连接不可用")

    def _check_audio_devices(self):
        """检查音频设备"""
        try:
            Microphone.list_microphone_names()
        except Exception as e:
            logging.error(f"麦克风检查失败: {str(e)}")
            raise AudioDeviceError("请确保麦克风已正确连接")

    def _setup_voice_engine(self):
        """配置语音引擎"""
        try:
            self.engine.setProperty('rate', self.config.speech_rate)
            self.engine.setProperty('volume', self.config.volume)
        except Exception as e:
            raise SynthesisError(f"语音引擎配置失败: {str(e)}")

    def _check_volume(self, audio_data):
        """检查音量级别"""
        if np.abs(audio_data).mean() < Config.MINIMUM_VOLUME:
            return False
        return True

    @lru_cache(maxsize=100)
    def _cached_ai_response(self, user_input: str) -> str:
        """缓存的AI响应"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
                timeout=self.config.api_timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            raise APIError(f"OpenAI API调用失败: {str(e)}")

    def listen(self):
        """增强的语音识别"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                with Microphone() as source:
                    logging.info("正在听取用户输入...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                    
                    # 检查音量
                    if not self._check_volume(np.frombuffer(audio.frame_data, np.int16)):
                        self.speak("声音太小，请说话声音大一点")
                        continue
                    
                    text = self.recognizer.recognize_google(
                        audio, 
                        language=Config.SPEECH_LANGUAGE
                    )
                    
                    # 过滤敏感信息
                    text = filter_sensitive_info(text)
                    logging.info(f"识别到的文字: {text}")
                    return text
                    
            except sr.UnknownValueError:
                if attempt == Config.MAX_RETRIES - 1:
                    logging.error("无法识别语音")
                    return None
                time.sleep(Config.RETRY_DELAY)
            except sr.RequestError as e:
                logging.error(f"语音识别服务错误: {str(e)}")
                return None

    def get_ai_response(self, user_input):
        """获取AI响应（带缓存）"""
        try:
            # 检查网络
            if not self._check_network():
                return "网络连接不稳定，请检查网络后重试"
                
            # 使用缓存响应
            return self._cached_ai_response(user_input)
            
        except openai.error.Timeout:
            logging.error("AI响应超时")
            return "响应时间过长，请稍后重试"
        except Exception as e:
            logging.error(f"AI响应错误: {str(e)}")
            return "抱歉，我现在无法回答"

    def _get_ai_response_impl(self, user_input):
        """实际的AI响应实现"""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        response = openai.ChatCompletion.create(
            model=Config.AI_MODEL,
            messages=[
                {"role": "system", "content": Config.SYSTEM_PROMPT},
                *self.conversation_history
            ],
            max_tokens=Config.MAX_TOKENS,
            timeout=Config.RESPONSE_TIMEOUT
        )
        
        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        if len(self.conversation_history) > Config.MAX_HISTORY:
            self.conversation_history = self.conversation_history[-Config.MAX_HISTORY:]
            
        return ai_response

    def speak(self, text):
        """改进的语音合成"""
        try:
            logging.info(f"正在播放: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"语音合成错误: {str(e)}")
            # 尝试使用备用声音引擎
            self._fallback_speak(text)

    def run(self):
        """主循环"""
        self.speak("你好，我是AI语音助手，请说话。")
        
        while True:
            try:
                if not self._check_network():
                    self.speak("网络连接不稳定，正在重试...")
                    time.sleep(Config.RETRY_DELAY)
                    continue
                    
                user_input = self.listen()
                if user_input is None:
                    self.speak("抱歉，我没有听清，请再说一遍。")
                    continue
                
                if "再见" in user_input or "退出" in user_input:
                    self.speak("再见！")
                    break
                
                response = self.get_ai_response(user_input)
                self.speak(response)
                
            except Exception as e:
                logging.error(f"运行错误: {str(e)}")
                self.speak("发生错误，正在重试...")

def main_cli():
    """命令行入口点"""
    try:
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # 加载环境变量
        from dotenv import load_dotenv
        load_dotenv()
        
        # 创建并运行助手
        assistant = VoiceAssistant()
        assistant.run()
        
    except KeyboardInterrupt:
        logging.info("用户中断程序")
        sys.exit(0)
    except Exception as e:
        logging.error(f"程序异常退出: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main_cli()