"""
Server Monitor MCP Server

一个基于 MCP 的远程服务器监测系统。

Author: 发财一号
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "发财一号"

from .ssh.client import SSHClient
from .ssh.config import ServerConfig

__all__ = [
    "SSHClient",
    "ServerConfig",
]
