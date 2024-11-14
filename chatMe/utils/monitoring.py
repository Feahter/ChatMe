"""
性能监控工具模块
"""

import psutil
import time
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from ..config import Config
from functools import wraps

@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    network_bytes_sent: int
    network_bytes_recv: int
    disk_usage_percent: float
    
def performance_monitor(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            duration = end_time - start_time
            memory_used = end_memory - start_memory
            
            logging.info(
                f"函数 {func.__name__} 执行时间: {duration:.2f}秒, "
                f"内存使用: {memory_used:.2f}MB"
            )
            
            return result
            
        except Exception as e:
            logging.error(f"函数 {func.__name__} 执行出错: {str(e)}")
            raise
            
    return wrapper

class PerformanceMonitor:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self.metrics_history: List[PerformanceMetrics] = []
        self.start_time = time.time()
        
        # 初始化网络计数器
        self.last_net_io = psutil.net_io_counters()
        self.last_check_time = self.start_time
    
    def collect_metrics(self) -> PerformanceMetrics:
        """
        收集当前性能指标
        
        Returns:
            PerformanceMetrics: 性能指标数据
        """
        try:
            current_time = time.time()
            
            # 获取CPU使用率
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # 获取内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 获取网络IO
            net_io = psutil.net_io_counters()
            time_diff = current_time - self.last_check_time
            
            bytes_sent = (net_io.bytes_sent - self.last_net_io.bytes_sent) / time_diff
            bytes_recv = (net_io.bytes_recv - self.last_net_io.bytes_recv) / time_diff
            
            # 更新网络计数器
            self.last_net_io = net_io
            self.last_check_time = current_time
            
            # 获取磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            metrics = PerformanceMetrics(
                timestamp=current_time,
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                network_bytes_sent=int(bytes_sent),
                network_bytes_recv=int(bytes_recv),
                disk_usage_percent=disk_percent
            )
            
            # 保存到历史记录
            self.metrics_history.append(metrics)
            
            # 限制历史记录大小
            if len(self.metrics_history) > self.config.MAX_METRICS_HISTORY:
                self.metrics_history = self.metrics_history[-self.config.MAX_METRICS_HISTORY:]
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"性能指标收集失败: {str(e)}")
            raise
    
    def get_average_metrics(self, 
                          duration: Optional[float] = None) -> PerformanceMetrics:
        """
        获取平均性能指标
        
        Args:
            duration: 时间范围（秒），None表示所有历史数据
            
        Returns:
            PerformanceMetrics: 平均性能指标
        """
        if not self.metrics_history:
            return None
            
        if duration:
            current_time = time.time()
            filtered_metrics = [
                m for m in self.metrics_history 
                if current_time - m.timestamp <= duration
            ]
        else:
            filtered_metrics = self.metrics_history
            
        if not filtered_metrics:
            return None
            
        return PerformanceMetrics(
            timestamp=time.time(),
            cpu_percent=sum(m.cpu_percent for m in filtered_metrics) / len(filtered_metrics),
            memory_percent=sum(m.memory_percent for m in filtered_metrics) / len(filtered_metrics),
            network_bytes_sent=sum(m.network_bytes_sent for m in filtered_metrics) / len(filtered_metrics),
            network_bytes_recv=sum(m.network_bytes_recv for m in filtered_metrics) / len(filtered_metrics),
            disk_usage_percent=sum(m.disk_usage_percent for m in filtered_metrics) / len(filtered_metrics)
        )
    
    def get_performance_report(self) -> Dict:
        """
        生成性能报告
        
        Returns:
            Dict: 性能报告数据
        """
        current_metrics = self.collect_metrics()
        avg_metrics = self.get_average_metrics(duration=300)  # 5分钟平均
        
        return {
            'current': {
                'cpu_percent': current_metrics.cpu_percent,
                'memory_percent': current_metrics.memory_percent,
                'network_bytes_sent': current_metrics.network_bytes_sent,
                'network_bytes_recv': current_metrics.network_bytes_recv,
                'disk_usage_percent': current_metrics.disk_usage_percent
            },
            'average_5min': {
                'cpu_percent': avg_metrics.cpu_percent if avg_metrics else None,
                'memory_percent': avg_metrics.memory_percent if avg_metrics else None,
                'network_bytes_sent': avg_metrics.network_bytes_sent if avg_metrics else None,
                'network_bytes_recv': avg_metrics.network_bytes_recv if avg_metrics else None,
                'disk_usage_percent': avg_metrics.disk_usage_percent if avg_metrics else None
            },
            'uptime': time.time() - self.start_time,
            'metrics_count': len(self.metrics_history)
        }