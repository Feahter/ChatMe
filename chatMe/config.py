'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 17:38:03
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 17:38:06
FilePath: /ChatMe/config.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
class Config:
    # 网络配置
    NETWORK_TIMEOUT = 5
    RETRY_DELAY = 1
    MAX_RETRIES = 3
    
    # 语音配置
    SPEECH_LANGUAGE = 'zh-CN'
    SPEECH_RATE = 150
    SPEECH_VOLUME = 0.9
    MINIMUM_VOLUME = 500
    
    # AI配置
    AI_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 150
    RESPONSE_TIMEOUT = 10
    SYSTEM_PROMPT = "你是一个友好的AI助手，请用简洁的语言回答问题。"
    
    # 缓存配置
    CACHE_SIZE = 100
    MAX_HISTORY = 10