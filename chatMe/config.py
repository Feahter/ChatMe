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
    volume: float = 1.0
    energy_threshold: int = 300
    ambient_duration: int = 1
    listen_timeout: int = 5
    phrase_timeout: int = 3
    
    # API参数
    api_timeout: int = 10
    max_retries: int = 3
    
    # 缓存参数
    cache_size: int = 100
    CACHE_SIZE: int = 100
    
    # 网络参数
    NETWORK_TIMEOUT: int = 5
    
    def __post_init__(self):
        """验证配置"""
        if self.max_conversation_history < 1:
            raise ValueError("max_conversation_history must be positive")
        if not self.language:
            raise KeyError("language is required")
        if not 0 <= self.volume <= 1:
            raise ValueError("volume must be between 0 and 1")
        if self.cache_size < 1:
            raise ValueError("cache_size must be positive")
        self.CACHE_SIZE = self.cache_size