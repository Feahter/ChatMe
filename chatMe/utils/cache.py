
from cachetools import TTLCache, LRUCache

class ResponseCache:
    def __init__(self):
        # 使用TTL缓存，10分钟过期
        self.short_term = TTLCache(
            maxsize=100, 
            ttl=600
        )
        # 使用LRU缓存存储常用响应
        self.long_term = LRUCache(
            maxsize=1000
        )