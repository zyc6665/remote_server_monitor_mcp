"""命令执行工具。"""

from typing import Optional

from mcp.server.models import Tool

from ..ssh.client import SSHClient, SSHResult


def execute_command(
    server_name: str,
    ssh_client: SSHClient,
    command: str,
    timeout: Optional[int] = None,
) -> SSHResult:
    """
    在远程服务器上执行命令。

    Args:
        server_name: 服务器名称
        ssh_client: SSH 客户端
        command: 要执行的命令
        timeout: 超时时间（秒），默认使用配置的默认值

    Returns:
        SSHResult: 执行结果
    """
    if timeout is None:
        timeout = 30

    return ssh_client.execute(command, timeout=timeout)


def execute_command_tool() -> Tool:
    """获取命令执行工具定义。"""
    return Tool(
        name="execute_command",
        description="在远程服务器上执行任意 shell 命令并返回结果",
        inputSchema={
            "type": "object",
            "properties": {
                "server": {
                    "type": "string",
                    "description": "服务器名称（默认使用配置中的默认服务器）",
                },
                "command": {
                    "type": "string",
                    "description": "要执行的 shell 命令",
                },
                "timeout": {
                    "type": "integer",
                    "default": 30,
                    "description": "命令超时时间（秒）",
                },
            },
            "required": ["command"],
        },
    )
