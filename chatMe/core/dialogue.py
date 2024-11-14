'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:38:00
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 18:38:02
FilePath: /ChatMe/ai_voice_assistant/core/dialogue.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
对话管理模块
"""
from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass
from datetime import datetime
from ..exceptions import DialogueError
from ..config import Config

@dataclass
class DialogueContext:
    """对话上下文数据类"""
    user_id: str
    session_id: str
    start_time: datetime
    messages: List[Dict[str, str]]
    metadata: Optional[Dict[str, Any]] = None

class DialogueManager:
    """对话管理器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or Config()
        self.contexts: Dict[str, DialogueContext] = {}
        self.logger = logging.getLogger(__name__)
        
    def create_session(self, user_id: str) -> str:
        """
        创建新的对话会话
        
        Args:
            user_id: 用户ID
            
        Returns:
            session_id: 会话ID
        """
        try:
            session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            self.contexts[session_id] = DialogueContext(
                user_id=user_id,
                session_id=session_id,
                start_time=datetime.now(),
                messages=[]
            )
            self.logger.info(f"创建新会话: {session_id}")
            return session_id
        except Exception as e:
            raise DialogueError(f"创建会话失败: {str(e)}")
        
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """
        添加对话消息
        
        Args:
            session_id: 会话ID
            role: 发言角色 ("user" 或 "assistant")
            content: 消息内容
            
        Raises:
            DialogueError: 添加消息失败
        """
        try:
            if session_id not in self.contexts:
                raise ValueError(f"Session {session_id} not found")
                
            self.contexts[session_id].messages.append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            self.logger.debug(f"添加消息到会话 {session_id}: {role} - {content[:50]}...")
        except Exception as e:
            raise DialogueError(f"添加消息失败: {str(e)}")
        
    def get_context(self, session_id: str) -> DialogueContext:
        """
        获取对话上下文
        
        Args:
            session_id: 会话ID
            
        Returns:
            DialogueContext: 对话上下文
            
        Raises:
            DialogueError: 获取上下文失败
        """
        try:
            if session_id not in self.contexts:
                raise ValueError(f"Session {session_id} not found")
            return self.contexts[session_id]
        except Exception as e:
            raise DialogueError(f"获取上下文失败: {str(e)}")
        
    def get_history(self, session_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        获取对话历史
        
        Args:
            session_id: 会话ID
            limit: 返回的最大消息数量
            
        Returns:
            List[Dict]: 对话历史消息列表
            
        Raises:
            DialogueError: 获取历史记录失败
        """
        try:
            context = self.get_context(session_id)
            messages = context.messages
            if limit:
                messages = messages[-limit:]
            return messages
        except Exception as e:
            raise DialogueError(f"获取历史记录失败: {str(e)}")
        
    def clear_session(self, session_id: str) -> None:
        """
        清除会话数据
        
        Args:
            session_id: 会话ID
            
        Raises:
            DialogueError: 清除会话失败
        """
        try:
            if session_id in self.contexts:
                del self.contexts[session_id]
                self.logger.info(f"清除会话: {session_id}")
        except Exception as e:
            raise DialogueError(f"清除会话失败: {str(e)}")