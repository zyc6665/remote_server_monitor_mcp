"""SSH 客户端封装模块。"""

from typing import Optional

import paramiko
from pydantic import BaseModel

from .config import ServerConfig


class SSHResult(BaseModel):
    """SSH 命令执行结果。"""

    stdout: str = Field(description="标准输出")
    stderr: str = Field(description="标准错误")
    exit_code: int = Field(description="退出码")
    success: bool = Field(description="是否成功")

    class Config:
        json_schema_extra = {
            "example": {
                "stdout": "total 8",
                "stderr": "",
                "exit_code": 0,
                "success": True,
            }
        }


class SSHClient:
    """SSH 客户端封装，简化远程服务器操作。"""

    def __init__(self, config: ServerConfig, timeout: int = 10):
        """
        初始化 SSH 客户端。

        Args:
            config: 服务器配置
            timeout: 连接超时时间（秒）
        """
        self.config = config
        self.timeout = timeout
        self.client: Optional[paramiko.SSHClient] = None

    def connect(self) -> None:
        """连接到服务器。"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 准备认证凭据
        auth_kwargs = {
            "hostname": self.config.host,
            "port": self.config.port,
            "username": self.config.username,
            "timeout": self.timeout,
        }

        if self.config.private_key_path:
            # 使用密钥认证
            private_key = paramiko.RSAKey.from_private_key_file(
                self.config.private_key_path
            )
            auth_kwargs["pkey"] = private_key
        elif self.config.password:
            # 使用密码认证
            auth_kwargs["password"] = self.config.password
        else:
            raise ValueError("必须提供 private_key_path 或 password 其中之一")

        self.client.connect(**auth_kwargs)

    def execute(self, command: str, timeout: int = 30) -> SSHResult:
        """
        执行远程命令。

        Args:
            command: 要执行的命令
            timeout: 命令超时时间（秒）

        Returns:
            SSHResult: 执行结果
        """
        if not self.client:
            raise RuntimeError("SSH 客户端未连接")

        stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)

        # 获取输出
        stdout_str = stdout.read().decode("utf-8")
        stderr_str = stderr.read().decode("utf-8")
        exit_code = stdout.channel.recv_exit_status()

        return SSHResult(
            stdout=stdout_str,
            stderr=stderr_str,
            exit_code=exit_code,
            success=exit_code == 0,
        )

    def disconnect(self) -> None:
        """断开连接。"""
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        """上下文管理器入口。"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出。"""
        self.disconnect()
