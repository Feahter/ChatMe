"""
AI助手模型定义
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any
import json
import time
from ..core.recognition import SpeechRecognizer
from ..core.synthesis import SpeechSynthesizer
from ..core.dialogue import DialogueManager
from ..utils.monitoring import PerformanceMonitor
from ..exceptions import AssistantError
from ..config import Config

class AssistantState(Enum):
    """助手状态枚举"""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    ERROR = "error"
    TERMINATED = "terminated"

@dataclass
class AssistantConfig:
    """助手配置数据类"""
    name: str = "AI助手"
    language: str = "zh-CN"
    voice_id: Optional[str] = None
    wake_words: List[str] = None
    max_conversation_history: int = 10
    auto_adjust_noise: bool = True
    enable_performance_monitoring: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'language': self.language,
            'voice_id': self.voice_id,
            'wake_words': self.wake_words,
            'max_conversation_history': self.max_conversation_history,
            'auto_adjust_noise': self.auto_adjust_noise,
            'enable_performance_monitoring': self.enable_performance_monitoring
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AssistantConfig':
        """从字典创建配置"""
        return cls(**data)
    
    def save_to_file(self, filename: str):
        """保存配置到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'AssistantConfig':
        """从文件加载配置"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

class Assistant:
    """AI助手主类"""
    def __init__(self, config: Optional[AssistantConfig] = None):
        self.config = config or AssistantConfig()
        self.state = AssistantState.INITIALIZING
        self.start_time = time.time()
        
        # 初始化组件
        self._init_components()
        
        # 性能监控
        if self.config.enable_performance_monitoring:
            self.monitor = PerformanceMonitor()
        
        self.state = AssistantState.IDLE
    
    def _init_components(self):
        """初始化各个组件"""
        try:
            self.recognizer = SpeechRecognizer()
            self.synthesizer = SpeechSynthesizer()
            self.dialogue_manager = DialogueManager()
        except Exception as e:
            self.state = AssistantState.ERROR
            raise AssistantError(f"组件初始化失败: {str(e)}")
    
    def start(self):
        """启动助手"""
        try:
            self.synthesizer.speak(f"你好，我是{self.config.name}")
            
            while self.state != AssistantState.TERMINATED:
                if self.config.enable_performance_monitoring:
                    self.monitor.collect_metrics()
                
                self.state = AssistantState.LISTENING
                user_input = self.recognizer.listen()
                
                if user_input is None:
                    continue
                
                if any(word in user_input for word in ['再见', '退出']):
                    self.stop()
                    break
                
                self.state = AssistantState.PROCESSING
                response = self.dialogue_manager.get_response(user_input)
                
                self.state = AssistantState.SPEAKING
                self.synthesizer.speak(response)
                
                self.state = AssistantState.IDLE
                
        except Exception as e:
            self.state = AssistantState.ERROR
            raise AssistantError(f"助手运行错误: {str(e)}")
    
    def stop(self):
        """停止助手"""
        try:
            self.synthesizer.speak("再见！")
            self.state = AssistantState.TERMINATED
            
            # 清理资源
            self.cleanup()
            
        except Exception as e:
            self.state = AssistantState.ERROR
            raise AssistantError(f"助手停止错误: {str(e)}")
    
    def cleanup(self):
        """清理资源"""
        try:
            # 保存对话历史
            self.save_conversation_history()
            
            # 生成性能报告
            if self.config.enable_performance_monitoring:
                self.save_performance_report()
                
        except Exception as e:
            raise AssistantError(f"资源清理失败: {str(e)}")
    
    def save_conversation_history(self, filename: str = "conversation_history.json"):
        """保存对话历史"""
        history = self.dialogue_manager.get_history()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def save_performance_report(self, filename: str = "performance_report.json"):
        """保存性能报告"""
        if self.config.enable_performance_monitoring:
            report = self.monitor.get_performance_report()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
    
    def get_status(self) -> Dict[str, Any]:
        """获取助手状态信息"""
        return {
            'state': self.state.value,
            'uptime': time.time() - self.start_time,
            'config': self.config.to_dict(),
            'performance': self.monitor.get_performance_report() if self.config.enable_performance_monitoring else None
        }
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.cleanup()