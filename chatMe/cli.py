import click
import os
from pathlib import Path
import yaml
from typing import Dict, Any
from .config import AIConfig
from .core.providers import AIProvider
from .main import VoiceAssistant, ChatMe

class ConfigManager:
    def __init__(self):
        self.config = AIConfig()
    
    def create_provider(self, name: str, settings: Dict[str, Any]):
        """创建新的AI提供者配置"""
        self.config.set_provider_config(name, settings)
        
    def update_provider(self, name: str, settings: Dict[str, Any]):
        """更新现有提供者配置"""
        current = self.config.get_provider_config(name)
        current.update(settings)
        self.config.set_provider_config(name, current)
        
    def remove_provider(self, name: str):
        """删除提供者配置"""
        if "providers" in self.config.config:
            self.config.config["providers"].pop(name, None)
            self.config.save_config()

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.1.0', prog_name='ChatMe')
def cli():
    """ChatMe - AI语音助手命令行工具
    
    配置和管理您的AI语音助手。
    
    基本用法:
      chatme start             # 启动语音助手
      chatme chat             # 启动文字聊天
      chatme init             # 初始化配置
      chatme provider add     # 添加AI提供者
      chatme config           # 设置全局配置
    """
    pass

@cli.group(help="AI提供者配置管理")
def provider():
    """管理AI提供者配置
    
    示例:
      chatme provider add openai    # 添加OpenAI提供者
      chatme provider list          # 查看所有提供者
    """
    pass

@provider.command(name="add", help="添加新的AI提供者")
@click.argument("name")
@click.option("--api-key", prompt=True, hide_input=True, help="API密钥")
@click.option("--model", default="gpt-3.5-turbo", show_default=True, help="模型名称")
@click.option("--temperature", default=0.7, show_default=True, type=float, help="温度参数(0-1)")
@click.option("--max-tokens", default=2000, show_default=True, type=int, help="最大token数")
def add_provider(name: str, api_key: str, model: str, temperature: float, max_tokens: int):
    """添加新的AI提供者配置
    
    参数:
        NAME: 提供者名称(如openai)
    
    示例:
        chatme provider add openai --model gpt-4
        chatme provider add azure --api-key YOUR_KEY
    """
    manager = ConfigManager()
    settings = {
        "api_key": api_key,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    manager.create_provider(name, settings)
    click.echo(f"已添加提供者: {name}")

@provider.command(name="update", help="更新AI提供者配置")
@click.argument("name")
@click.option("--api-key", help="API密钥")
@click.option("--model", help="模型名称")
@click.option("--temperature", type=float, help="温度参数(0-1)")
@click.option("--max-tokens", type=int, help="最大token数")
def update_provider(name: str, **kwargs):
    """更新AI提供者配置
    
    参数:
        NAME: 提供者名称
        
    示例:
        chatme provider update openai --model gpt-4
        chatme provider update azure --api-key NEW_KEY
    """
    manager = ConfigManager()
    settings = {k: v for k, v in kwargs.items() if v is not None}
    manager.update_provider(name, settings)
    click.echo(f"已更新提供者: {name}")

@provider.command(name="remove", help="删除AI提供者")
@click.argument("name")
def remove_provider(name: str):
    """删除AI提供者配置
    
    参数:
        NAME: 提供者名称
        
    示例:
        chatme provider remove openai
    """
    manager = ConfigManager()
    manager.remove_provider(name)
    click.echo(f"已删除提供者: {name}")

@provider.command(name="list", help="列出所有AI提供者")
def list_providers():
    """列出所有配置的提供者
    
    示例:
        chatme provider list
    """
    manager = ConfigManager()
    providers = manager.config.config.get("providers", {})
    if not providers:
        click.echo("当前没有配置任何提供者")
        return
        
    for name, cfg in providers.items():
        click.echo(f"\n{name}:")
        safe_cfg = cfg.copy()
        if 'api_key' in safe_cfg:
            safe_cfg['api_key'] = '****' + safe_cfg['api_key'][-4:]
        for key, value in safe_cfg.items():
            click.echo(f"  {key}: {value}")

@cli.command(help="配置全局设置")
@click.option("--provider", help="设置默认AI提供者")
@click.option("--language", help="设置默认语言(如zh-CN)")
@click.option("--voice-rate", type=int, help="设置语音速率(50-300)")
@click.option("--voice-volume", type=float, help="设置语音音量(0-1)")
def config(provider, language, voice_rate, voice_volume):
    """配置全局设置
    
    示例:
        chatme config --provider openai --language zh-CN
        chatme config --voice-rate 150 --voice-volume 0.8
    """
    manager = ConfigManager()
    if provider:
        manager.config.config["default_provider"] = provider
    if language:
        manager.config.config["language"] = language
    if voice_rate is not None:
        manager.config.config["voice_rate"] = voice_rate
    if voice_volume is not None:
        manager.config.config["voice_volume"] = voice_volume
    
    manager.config.save_config()
    click.echo("全局配置已更新")

@cli.command(help="初始化配置文件")
def init():
    """初始化配置文件
    
    这将在用户目录下创建默认配置文件。
    
    示例:
        chatme init
    """
    manager = ConfigManager()
    click.echo(f"配置文件已创建: {manager.config.config_path}")
    click.echo("\n后续步骤:")
    click.echo("1. 使用 'chatme provider add openai' 添加AI提供者")
    click.echo("2. 使用 'chatme config' 设置全局配置")
    click.echo("3. 运行 'chatme --help' 查看更多命令")

@cli.command(help="启动语音助手")
@click.option('--config', '-c', help="配置文件路径")
def start(config):
    """启动语音助手模式
    
    示例:
        chatme start
        chatme start --config custom_config.yaml
    """
    try:
        assistant = VoiceAssistant(config_path=config)
        click.echo("正在启动语音助手...")
        assistant.start()
    except Exception as e:
        click.echo(f"启动失败: {str(e)}", err=True)

@cli.command(help="启动文字聊天")
@click.option('--config', '-c', help="配置文件路径")
def chat(config):
    """启动文字聊天模式
    
    示例:
        chatme chat
        chatme chat --config custom_config.yaml
    """
    try:
        chat_client = ChatMe(config_path=config)
        click.echo("ChatMe 文字助手 (输入 'exit' 退出)")
        
        while True:
            # 获取用户输入
            user_input = click.prompt('You')
            
            # 检查退出命令
            if user_input.lower() in ['exit', 'quit', '退出', '再见']:
                click.echo("再见！")
                break
                
            # 获取AI响应
            try:
                response = chat_client.chat(user_input)
                click.echo(f"AI: {response}")
            except Exception as e:
                click.echo(f"错误: {str(e)}", err=True)
                
    except Exception as e:
        click.echo(f"启动失败: {str(e)}", err=True)

@cli.command(help="运行诊断测试")
def diagnose():
    """运行系统诊断
    
    检查系统环境和依赖是否正确配置。
    
    示例:
        chatme diagnose
    """
    click.echo("正在进行系统诊断...")
    
    # 检查配置文件
    config_path = Path.home() / ".chatme" / "config.yaml"
    if config_path.exists():
        click.echo("✓ 配置文件存在")
    else:
        click.echo("✗ 配置文件不存在，请运行 'chatme init'")
    
    # 检查API密钥
    if os.getenv("OPENAI_API_KEY"):
        click.echo("✓ 找到OpenAI API密钥")
    else:
        click.echo("✗ 未设置OpenAI API密钥")
    
    # 检查音频设备
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        click.echo(f"✓ 检测到 {device_count} 个音频设备")
        p.terminate()
    except Exception as e:
        click.echo(f"✗ 音频设备检查失败: {str(e)}")
    
    # 检查网络连接
    try:
        import requests
        requests.get("https://api.openai.com", timeout=5)
        click.echo("✓ 网络连接正常")
    except Exception as e:
        click.echo("✗ 网络连接异常")

def main():
    cli()

if __name__ == "__main__":
    main() 