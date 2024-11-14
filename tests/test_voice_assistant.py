'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 17:38:54
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 18:56:59
FilePath: /ChatMe/tests/test_voice_assistant.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
from unittest.mock import Mock, patch
from chatMe.main import VoiceAssistant
from chatMe.exceptions import NetworkError, AudioDeviceError

class TestVoiceAssistant:
    @pytest.fixture
    def assistant(self):
        with VoiceAssistant() as va:
            yield va
    
    def test_initialization(self, assistant):
        assert assistant.state == AssistantState.IDLE
        assert not assistant.is_busy
    
    @patch('requests.get')
    def test_network_check(self, mock_get, assistant):
        # 模拟网络正常
        mock_get.return_value.status_code = 200
        assert assistant._check_network() is True
        
        # 模拟网络异常
        mock_get.side_effect = requests.exceptions.ConnectionError
        assert assistant._check_network() is False
    
    def test_volume_check(self, assistant):
        # 模拟音量过低
        low_volume_data = np.zeros(1000, dtype=np.int16)
        assert assistant._check_volume(low_volume_data) is False
        
        # 模拟正常音量
        normal_volume_data = np.ones(1000, dtype=np.int16) * 1000
        assert assistant._check_volume(normal_volume_data) is True