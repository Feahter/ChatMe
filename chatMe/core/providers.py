'''
Author: Arthur arthur@lwork.com
Date: 2024-11-15 10:35:04
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-15 11:03:55
FilePath: /ChatMe/chatMe/core/providers.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Type
import importlib
import logging
from ..exceptions import ConfigError

class AIProvider(ABC):
    """AI提供者的抽象基类"""
    
    @abstractmethod
    def generate_response(self, 
                         prompt: str,
                         **kwargs) -> str:
        """生成AI回复"""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置是否有效"""
        pass
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'AIProvider':
        """从配置创建提供者实例"""
        provider_type = config.get('type', '').lower()
        if not provider_type:
            raise ConfigError("未指定AI提供者类型")
            
        # 获取提供者类
        provider_class = PROVIDER_REGISTRY.get(provider_type)
        if not provider_class:
            # 尝试动态导入自定义提供者
            try:
                module_path = config.get('module_path', '')
                class_name = config.get('class_name', '')
                if not (module_path and class_name):
                    raise ConfigError(f"未知的提供者类型: {provider_type}")
                    
                module = importlib.import_module(module_path)
                provider_class = getattr(module, class_name)
                
                # 验证类是否正确实现了接口
                if not issubclass(provider_class, AIProvider):
                    raise ConfigError(f"提供者类 {class_name} 必须继承 AIProvider")
                    
            except Exception as e:
                raise ConfigError(f"加载提供者失败: {str(e)}")
        
        # 验证配置
        if not provider_class.validate_config(config):
            raise ConfigError(f"提供者 {provider_type} 配置无效")
            
        # 创建实例
        try:
            return provider_class(**config.get('settings', {}))
        except Exception as e:
            raise ConfigError(f"初始化提供者失败: {str(e)}")

class OpenAIProvider(AIProvider):
    """OpenAI API实现"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", **kwargs):
        import openai
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
        self.kwargs = kwargs
        
    def generate_response(self, prompt: str, **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **{**self.kwargs, **kwargs}
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"OpenAI API调用失败: {str(e)}")
            raise
        
    def validate_config(self, config: Dict[str, Any]) -> bool:
        settings = config.get('settings', {})
        return all(k in settings for k in ['api_key', 'model'])

class AzureProvider(AIProvider):
    """Azure OpenAI实现"""
    
    def __init__(self, api_key: str, endpoint: str, deployment_name: str, **kwargs):
        import openai
        self.client = openai.AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version="2023-05-15"
        )
        self.deployment_name = deployment_name
        self.kwargs = kwargs
        
    def generate_response(self, prompt: str, **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": prompt}],
                **{**self.kwargs, **kwargs}
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Azure API调用失败: {str(e)}")
            raise
            
    def validate_config(self, config: Dict[str, Any]) -> bool:
        settings = config.get('settings', {})
        return all(k in settings for k in ['api_key', 'endpoint', 'deployment_name'])

# 注册内置提供者
PROVIDER_REGISTRY: Dict[str, Type[AIProvider]] = {
    'openai': OpenAIProvider,
    'azure': AzureProvider
}