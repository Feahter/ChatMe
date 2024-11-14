from speech_recognition import Recognizer, Microphone
import pyttsx3
import openai
import requests
import numpy as np
from functools import lru_cache
from pathlib import Path
import time
import logging
from .config import Config
from .utils import filter_sensitive_info
import speech_recognition as sr

class VoiceAssistant:
    def __init__(self):
        self._init_logging()
        self._check_environment()
        
        # 初始化组件
        self.recognizer = Recognizer()
        self.engine = pyttsx3.init()
        self._setup_voice_engine()
        
        self.conversation_history = []
        
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
            raise AssistantError(f"语音引擎初始化失败: {str(e)}")

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
            return False

    def _check_audio_devices(self):
        """检查音频设备"""
        try:
            Microphone.list_microphone_names()
        except Exception as e:
            logging.error(f"麦克风检查失败: {str(e)}")
            raise RuntimeError("请确保麦克风已正确连接")

    def _setup_voice_engine(self):
        """配置语音引擎"""
        self.engine.setProperty('rate', Config.SPEECH_RATE)
        self.engine.setProperty('volume', Config.SPEECH_VOLUME)

    def _check_volume(self, audio_data):
        """检查音量级别"""
        if np.abs(audio_data).mean() < Config.MINIMUM_VOLUME:
            return False
        return True

    @lru_cache(maxsize=Config.CACHE_SIZE)
    def _cached_ai_response(self, user_input: str):
        """缓存AI响应"""
        return self._get_ai_response_impl(user_input)

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