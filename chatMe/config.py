"""
配置模块
"""
from typing import Dict, Any, Optional
from pathlib import Path
import yaml
import json

class Config:
    """基础配置类"""
    # 系统配置
    SPEECH_LANGUAGE = "zh-CN"
    AI_MODEL = "gpt-3.5-turbo"
    SYSTEM_PROMPT = "你是一个智能助手"
    
    # 性能配置
    MAX_TOKENS = 2000
    RESPONSE_TIMEOUT = 30
    RETRY_DELAY = 1
    MAX_RETRIES = 3
    NETWORK_TIMEOUT = 5
    
    # 音频配置
    MINIMUM_VOLUME = 100
    MAX_HISTORY = 10
    
    def __init__(self, **kwargs):
        # 允许通过kwargs覆盖默认配置
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # 语音配置
        self.speech_rate = kwargs.get('speech_rate', 150)
        self.volume = kwargs.get('volume', 0.8)
        self.language = kwargs.get('language', self.SPEECH_LANGUAGE)
        self.name = kwargs.get('name', 'AI Assistant')

class AIConfig:
    """AI配置管理类"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or str(Path.home() / ".chatme" / "config.yaml")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_file = Path(self.config_path)
        
        # 如果配置文件不存在，创建默认配置
        if not config_file.exists():
            default_config = {
                "default_provider": "openai",
                "providers": {
                    "openai": {
                        "api_key": "",
                        "model": "gpt-3.5-turbo",
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                },
                "language": "zh-CN",
                "speech_rate": 150,
                "volume": 0.8
            }
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                yaml.dump(default_config, f)
            return default_config
            
        # 加载现有配置
        with open(config_file) as f:
            return yaml.safe_load(f)
    
    def save_config(self):
        """保存配置到文件"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)
    
    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """获取指定提供者的配置"""
        return self.config.get("providers", {}).get(provider_name, {})
    
    def set_provider_config(self, provider_name: str, config: Dict[str, Any]):
        """设置提供者配置"""
        if "providers" not in self.config:
            self.config["providers"] = {}
        self.config["providers"][provider_name] = config
        self.save_config()