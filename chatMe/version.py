'''
Author: Arthur arthur@lwork.com
Date: 2024-11-14 18:33:33
LastEditors: Arthur arthur@lwork.com
LastEditTime: 2024-11-14 18:33:36
FilePath: /ChatMe/ai_voice_assistant/version.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
AI Voice Assistant Version
~~~~~~~~~~~~~~~~~~~~~~~~~

版本信息管理。
"""

import re
from typing import NamedTuple, Optional

class Version(NamedTuple):
    major: int
    minor: int
    patch: int
    pre_release: Optional[str] = None
    build: Optional[str] = None

    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            version += f"-{self.pre_release}"
        if self.build:
            version += f"+{self.build}"
        return version

# 当前版本
VERSION = Version(0, 1, 0, "alpha", "dev")

# 版本字符串
__version__ = str(VERSION)

def parse_version(version_str: str) -> Version:
    """
    解析版本字符串为Version对象
    
    Args:
        version_str: 版本字符串 (例如: "1.2.3-alpha+dev")
    
    Returns:
        Version对象
    
    Raises:
        ValueError: 版本字符串格式无效
    """
    pattern = r"""
        ^
        (?P<major>\d+)
        \.
        (?P<minor>\d+)
        \.
        (?P<patch>\d+)
        (?:-(?P<pre_release>[0-9A-Za-z-]+))?
        (?:\+(?P<build>[0-9A-Za-z-]+))?
        $
    """
    match = re.match(pattern, version_str, re.VERBOSE)
    if not match:
        raise ValueError(f"Invalid version string: {version_str}")
    
    return Version(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
        pre_release=match.group("pre_release"),
        build=match.group("build")
    )

def get_version() -> str:
    """获取当前版本字符串"""
    return __version__

def is_stable_version() -> bool:
    """检查当前是否为稳定版本"""
    return VERSION.pre_release is None

def is_development_version() -> bool:
    """检查当前是否为开发版本"""
    return VERSION.build == "dev"

def require_version(min_version: str) -> bool:
    """
    检查当前版本是否满足最低版本要求
    
    Args:
        min_version: 最低版本要求
    
    Returns:
        bool: 是否满足要求
    """
    current = (VERSION.major, VERSION.minor, VERSION.patch)
    required = parse_version(min_version)
    required_tuple = (required.major, required.minor, required.patch)
    return current >= required_tuple