#!/bin/bash
# 在文件开头添加
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

echo "=== AI语音助手安装脚本 ==="
echo "正在检查系统环境..."

# 检查Python版本并尝试使用合适的版本
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "当前Python版本: $python_version"
if (( $(echo "$python_version 3.8" | awk '{print ($1 < $2)}') )) || (( $(echo "$python_version 3.12" | awk '{print ($1 > $2)}') )); then
    echo "当前Python版本 ($python_version) 不兼容"
    echo "正在查找兼容的Python版本..."
    
    # 查找可用的Python版本
    for ver in "3.8" "3.9" "3.10" "3.11"; do
        if command -v "python$ver" &> /dev/null; then
            echo "找到兼容版本: python$ver"
            python_cmd="python$ver"
            break
        fi
    done
    
    if [ -z "$python_cmd" ]; then
        echo "错误: 未找到兼容的Python版本(3.8-3.11)"
        echo "请安装兼容版本后重试"
        exit 1
    fi
else
    python_cmd="python3"
fi

# 检查系统类型并安装系统依赖
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到Linux系统，安装系统依赖..."
    sudo apt-get update
    sudo apt-get install -y python3-pyaudio portaudio19-dev python3-aifc
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到macOS系统，安装系统依赖..."
    brew install portaudio
fi

# 创建虚拟环境
echo "创建虚拟环境..."
$python_cmd -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip并设置超时时间
echo "升级pip..."
pip install --upgrade pip
pip config set global.timeout 1000

# 安装依赖
echo "安装项目依赖..."
# 先安装关键依赖
pip install wheel setuptools
pip install SpeechRecognition PyAudio

# 安装其他依赖
pip install -r requirements.txt || {
    echo "依赖安装失败，尝试使用国内镜像..."
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
}

# 安装项目本身
pip install -e .

# 安装开发依赖（如果指定）
if [ "$1" == "--dev" ]; then
    echo "安装开发依赖..."
    pip install -e .[dev]
fi

# 运行测试
echo "运行测试..."
python -m pytest tests/ || echo "警告: 部分测试未通过"

# 检查安装
echo "验证安装..."
python -c "from chatMe import VoiceAssistant; print('安装成功！')" || echo "警告: 验证安装失败"

echo "=== 安装完成 ==="
echo "使用方法："
echo "1. 激活虚拟环境：source venv/bin/activate"
echo "2. 运行助手：chatMe"
echo "3. 退出虚拟环境：deactivate"

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple