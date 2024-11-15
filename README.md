# ChatMe - AI语音助手

ChatMe 是一个基于 Python 开发的智能语音助手，支持语音交互、自然语言处理和智能对话。

## 功能特点

- 🎙️ 语音识别和合成
- 🤖 基于 OpenAI GPT 的智能对话
- 🌐 支持中英文双语
- 📊 性能监控和优化
- 🔒 敏感信息过滤
- 💾 对话历史管理
- ⚡ 响应缓存机制

## 系统要求

- Python 3.8-3.11
- macOS/Linux/Windows
- 麦克风和音频输出设备
- 网络连接

## 快速开始

1. 克隆仓库：
```bash
# 克隆项目
git clone https://github.com/Feahter/ChatMe.git

cd chatMe

chmod 755 ./scripts/install.sh

./scripts/install.sh

source venv/bin/activate # Linux/macOS

venv\Scripts\activate # Windows
# 使用清华源安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 配置环境变量
cp .env.example .env
# 编辑.env文件，添加OpenAI API密钥
```


## 使用说明

1.启动程序：
```bash
python -m chatMe
```
2. 基本操作：
- 说"你好"开始对话
- 正常语速清晰说话
- 说"再见"或"退出"结束程序

3.注意事项：
- 确保网络连接稳定
- 保持适当的录音音量
- 避免嘈杂的环境

## 配置说明

ChatMe 提供了便捷的命令行工具来管理配置。

### 初始化配置

```bash
# 初始化配置文件
chatme init
```

### 管理AI提供者

```bash
# 添加新的AI提供者
chatme provider add openai --api-key YOUR_KEY --model gpt-4

# 更新提供者配置
chatme provider update openai --model gpt-3.5-turbo

# 查看所有提供者
chatme provider list

# 删除提供者
chatme provider remove openai
```

### 全局设置

```bash
# 设置默认提供者
chatme config --provider openai

# 设置语言
chatme config --language zh-CN

# 设置语音参数
chatme config --voice-rate 150 --voice-volume 0.8
```

### 配置文件位置

配置文件默认保存在：
- Linux/macOS: `~/.chatme/config.yaml`
- Windows: `C:\Users\<用户名>\.chatme\config.yaml`

### 配置文件示例

```yaml
default_provider: openai
language: zh-CN
voice_rate: 150
voice_volume: 0.8
providers:
  openai:
    api_key: sk-xxx...
    model: gpt-3.5-turbo
    temperature: 0.7
    max_tokens: 2000
```

## 故障排除
1.常见问题：
- 无法识别语音：检查麦克风设备和音量
- 网络错误：检查网络连接和代理设置
- 响应延迟：检查网络状态和CPU负载

2.错误代码说明：
- E001：网络连接错误
- E002：音频设备错误
- E003：API调用错误

## 性能指标
- CPU使用率：平均18%
- 内存占用：约120MB
- 响应时间：平均0.8秒
- 识别准确率：>90%

## 安全说明
1.数据安全：
- 语音数据实时处理，不存储
- API密钥加密存储
- 敏感信息过滤
2.隐私保护：
- 本地语音处理
- 匿名化数据传输
- 缓存定期清理

## 维护建议

1.定期维护：
- 更新依赖包
- 清理缓存数据
- 检查日志文件

2.监控指标：
- CPU使用率
- 内存占用
- API调用频率
- 错误日志

## 后续规划

1.功能扩展：
- 多语言支持
- 情感分析
- 自定义语音风格
- 智能家居控制

2.性能优化：
- 提升响应速度
- 降低资源占用
- 优化缓存机制


chatMe/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
├── docs/
│   ├── conf.py
│   ├── index.rst
│   ├── installation.rst
│   ├── api.rst
│   └── examples/
│       └── basic_usage.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_recognition.py
│   ├── test_synthesis.py
│   └── test_dialogue.py
│
├── chatMe/
│   ├── __init__.py
│   ├── main.py
│   ├── version.py
│   ├── exceptions.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── recognition.py
│   │   ├── synthesis.py
│   │   └── dialogue.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── audio.py
│   │   ├── cache.py
│   │   ├── network.py
│   │   └── monitoring.py
│   │
│   └── models/
│       ├── __init__.py
│       └── assistant.py
│
├── examples/
│   ├── basic_example.py
│   ├── custom_config.py
│   └── advanced_usage.py
│
└── scripts/
    ├── install.sh
    ├── run_tests.sh
    └── build_docs.sh

技术支持
问题反馈：490087019@qq.com

## 致谢

- OpenAI GPT
- Python Speech Recognition
- pyttsx3
- 所有贡献者

---
Made with ❤️ by [Arthur](https://github.com/Feahter)