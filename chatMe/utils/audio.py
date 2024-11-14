"""
音频处理工具模块
"""

import numpy as np
import wave
import pyaudio
import audioop
from typing import Optional, Tuple
import logging
from ..exceptions import AudioDeviceError
from ..config import Config

class AudioProcessor:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self.pyaudio = pyaudio.PyAudio()
        
    def __del__(self):
        """清理音频资源"""
        self.pyaudio.terminate()
    
    def get_input_devices(self) -> list:
        """获取所有输入设备"""
        devices = []
        for i in range(self.pyaudio.get_device_count()):
            device_info = self.pyaudio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                devices.append(device_info)
        return devices
    
    def analyze_audio(self, audio_data: bytes) -> dict:
        """
        分析音频数据
        
        Args:
            audio_data: 原始音频数据
            
        Returns:
            dict: 包含音频分析结果的字典
        """
        # 转换为numpy数组
        data = np.frombuffer(audio_data, dtype=np.int16)
        
        # 计算音量
        rms = np.sqrt(np.mean(np.square(data)))
        
        # 计算频率特征
        fft_data = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(data))
        
        return {
            'volume': float(rms),
            'max_frequency': float(abs(frequencies[np.argmax(abs(fft_data))])),
            'sample_count': len(data)
        }
    
    def normalize_audio(self, audio_data: bytes) -> bytes:
        """
        标准化音频数据
        
        Args:
            audio_data: 原始音频数据
            
        Returns:
            bytes: 标准化后的音频数据
        """
        try:
            # 转换为PCM数据
            pcm_data = np.frombuffer(audio_data, dtype=np.int16)
            
            # 标准化
            normalized = pcm_data / np.max(np.abs(pcm_data))
            
            # 调整音量
            normalized *= self.config.AUDIO_NORMALIZE_FACTOR
            
            # 转回bytes
            return normalized.astype(np.int16).tobytes()
        except Exception as e:
            raise AudioDeviceError(f"音频标准化失败: {str(e)}")
    
    def save_wav(self, audio_data: bytes, filename: str, 
                 channels: int = 1, rate: int = 16000):
        """
        保存音频数据为WAV文件
        
        Args:
            audio_data: 音频数据
            filename: 输出文件名
            channels: 声道数
            rate: 采样率
        """
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(2)  # 16位采样
                wf.setframerate(rate)
                wf.writeframes(audio_data)
        except Exception as e:
            raise AudioDeviceError(f"保存WAV文件失败: {str(e)}")
    
    def detect_silence(self, audio_data: bytes, 
                      silence_threshold: int = 500) -> bool:
        """
        检测是否为静音
        
        Args:
            audio_data: 音频数据
            silence_threshold: 静音阈值
            
        Returns:
            bool: 是否为静音
        """
        rms = audioop.rms(audio_data, 2)  # 2表示16位采样
        return rms < silence_threshold