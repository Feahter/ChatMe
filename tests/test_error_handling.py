'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 17:41:06
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 17:41:33
FilePath: /ChatMe/test_error_handling.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
def test_error_recovery():
    assistant = VoiceAssistant()
    
    # 模拟网络错误
    with patch('requests.get', side_effect=NetworkError):
        response = assistant.get_ai_response("测试")
        assert "网络连接不稳定" in response
    
    # 模拟音频设备错误
    with patch.object(assistant, '_check_audio_devices', 
                     side_effect=AudioDeviceError):
        with pytest.raises(AudioDeviceError):
            assistant.listen()