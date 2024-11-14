"""
网络管理工具模块
"""

import requests
import aiohttp
import asyncio
from typing import Optional, Dict, Any
import logging
import time
from ..exceptions import NetworkError
from ..config import Config

class NetworkManager:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """配置会话参数"""
        self.session.timeout = self.config.REQUEST_TIMEOUT
        if self.config.PROXY:
            self.session.proxies = self.config.PROXY
        
    def check_connection(self, url: str = "https://api.openai.com") -> bool:
        """
        检查网络连接
        
        Args:
            url: 要检查的URL
            
        Returns:
            bool: 连接是否正常
        """
        try:
            response = self.session.get(
                url,
                timeout=self.config.CONNECTION_CHECK_TIMEOUT
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.warning(f"网络连接检查失败: {str(e)}")
            return False
    
    def request_with_retry(self, method: str, url: str, 
                          max_retries: int = 3, **kwargs) -> requests.Response:
        """
        带重试的请求
        
        Args:
            method: 请求方法
            url: 请求URL
            max_retries: 最大重试次数
            **kwargs: 其他请求参数
            
        Returns:
            Response对象
            
        Raises:
            NetworkError: 请求失败
        """
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise NetworkError(f"请求失败: {str(e)}")
                time.sleep(self.config.RETRY_DELAY * (attempt + 1))
    
    async def async_request(self, method: str, url: str, **kwargs) -> Dict:
        """
        异步请求
        
        Args:
            method: 请求方法
            url: 请求URL
            **kwargs: 其他请求参数
            
        Returns:
            Dict: 响应数据
            
        Raises:
            NetworkError: 请求失败
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, **kwargs) as response:
                    if response.status != 200:
                        raise NetworkError(
                            f"请求失败: HTTP {response.status}"
                        )
                    return await response.json()
            except aiohttp.ClientError as e:
                raise NetworkError(f"异步请求失败: {str(e)}")
    
    def get_network_stats(self) -> Dict[str, Any]:
        """
        获取网络状态统计
        
        Returns:
            Dict: 包含网络状态信息的字典
        """
        stats = {
            'connected': self.check_connection(),
            'proxy_enabled': bool(self.config.PROXY),
            'timeout_settings': {
                'request': self.config.REQUEST_TIMEOUT,
                'connection_check': self.config.CONNECTION_CHECK_TIMEOUT
            }
        }
        return stats