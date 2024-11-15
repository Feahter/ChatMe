"""
配置模块
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class Config:
    """配置类"""
    name: str = "AI Assistant"
    language: str = "zh-CN"
    voice_id: Optional[str] = None
    wake_words: List[str] = field(default_factory=lambda: ["你好", "助手"])
    max_conversation_history: int = 10
    auto_adjust_noise: bool = True
    enable_performance_monitoring: bool = False
    
    # 语音参数
    speech_rate: int = 150
    SPEECH_RATE: int = 150
    volume: float = 1.0
    SPEECH_VOLUME: float = 1.0
    energy_threshold: int = 300
    ENERGY_THRESHOLD: int = 300
    ambient_duration: int = 1
    AMBIENT_DURATION: int = 1
    listen_timeout: int = 5
    LISTEN_TIMEOUT: int = 5
    phrase_timeout: int = 3
    PHRASE_TIMEOUT: int = 3
    
    # API参数
    api_timeout: int = 10
    API_TIMEOUT: int = 10
    max_retries: int = 3
    MAX_RETRIES: int = 3
    
    # 缓存参数
    cache_size: int = 100
    CACHE_SIZE: int = 100
    
    # 网络参数
    network_timeout: int = 5
    NETWORK_TIMEOUT: int = 5
    
    # AI模型参数
    AI_MODEL: str = "gpt-3.5-turbo"
    SYSTEM_PROMPT: str = "你是一个智能语音助手"
    MAX_TOKENS: int = 150
    RESPONSE_TIMEOUT: int = 30
    MAX_HISTORY: int = 10
    
    # 语音参数
    SPEECH_LANGUAGE: str = "zh-CN"
    MINIMUM_VOLUME: float = 0.1
    RETRY_DELAY: int = 2
    
    def __post_init__(self):
        """验证配置并同步属性"""
        if self.max_conversation_history < 1:
            raise ValueError("max_conversation_history must be positive")
        if not self.language:
            raise KeyError("language is required")
        if not 0 <= self.volume <= 1:
            raise ValueError("volume must be between 0 and 1")
        if self.cache_size < 1:
            raise ValueError("cache_size must be positive")
            
        # 同步属性
        self.SPEECH_RATE = self.speech_rate
        self.SPEECH_VOLUME = self.volume
        self.ENERGY_THRESHOLD = self.energy_threshold
        self.AMBIENT_DURATION = self.ambient_duration
        self.LISTEN_TIMEOUT = self.listen_timeout
        self.PHRASE_TIMEOUT = self.phrase_timeout
        self.API_TIMEOUT = self.api_timeout
        self.MAX_RETRIES = self.max_retries
        self.CACHE_SIZE = self.cache_size
        self.NETWORK_TIMEOUT = self.network_timeout