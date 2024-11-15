import os
from setuptools import setup, find_packages
from chatMe.version import __version__

# 读取README文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# 开发依赖
dev_requirements = [
    "pytest>=6.2.5",
    "pytest-cov>=2.12.1",
    "pytest-asyncio>=0.16.0",
    "black>=21.12b0",
    "flake8>=4.0.1",
    "mypy>=0.910",
    "sphinx>=4.3.2",
    "sphinx-rtd-theme>=1.0.0"
]

# 可选依赖
extras_require = {
    'dev': dev_requirements,
    'test': [
        "pytest>=6.2.5",
        "pytest-cov>=2.12.1",
        "pytest-asyncio>=0.16.0"
    ],
    'docs': [
        "sphinx>=4.3.2",
        "sphinx-rtd-theme>=1.0.0"
    ],
    'performance': [
        "memory-profiler>=0.58.0",
        "prometheus-client>=0.12.0"
    ]
}

setup(
    name="ai-voice-assistant",
    version=__version__,
    author="Your Name",
    author_email="your.email@example.com",
    description="An intelligent voice assistant powered by AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Feahter/ChatMe.git",
    project_urls={
        "Bug Tracker": "https://github.com/Feahter/ChatMe.git/issues",
        "Documentation": "https://ai-voice-assistant.readthedocs.io/",
        "Source Code": "https://github.com/Feahter/ChatMe.git",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "chatMe=chatMe.main:main_cli",
        ],
    },
    include_package_data=True,
    package_data={
        "chatMe": [
            "config/*.json",
            "data/*.txt",
        ],
    },
    zip_safe=False,
    platforms="any",
    keywords=[
        "ai",
        "voice",
        "assistant",
        "speech recognition",
        "speech synthesis",
        "chatbot",
    ],
    # 测试配置
    test_suite="tests",
    tests_require=extras_require["test"],
    # 构建配置
    setup_requires=[
        "wheel>=0.37.0",
    ],
    # 许可证文件
    license="MIT",
    # 许可证文件路径
    license_files=("LICENSE",),
)

# 在开发模式下安装额外的工具
if os.environ.get("INSTALL_DEV_TOOLS"):
    extras_require["dev"].extend([
        "pre-commit>=2.16.0",
        "commitizen>=2.20.0",
        "black>=21.12b0",
        "isort>=5.10.1",
    ])

# 检查系统依赖
def check_system_dependencies():
    """检查系统依赖"""
    import platform
    system = platform.system().lower()
    
    if system == "linux":
        print("在Linux系统上，你可能需要安装以下依赖：")
        print("sudo apt-get install python3-pyaudio portaudio19-dev")
    elif system == "darwin":
        print("在macOS系统上，你可能需要安装以下依赖：")
        print("brew install portaudio")
    elif system == "windows":
        print("在Windows系统上，通常不需要额外的系统依赖。")

# 如果直接运行setup.py，检查系统依赖
if __name__ == "__main__":
    check_system_dependencies()