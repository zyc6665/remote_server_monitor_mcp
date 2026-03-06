"""SSH 服务器配置管理模块。"""

from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    """单台服务器配置。"""

    name: str = Field(description="服务器名称")
    host: str = Field(description="服务器 IP 或域名")
    port: int = Field(default=22, description="SSH 端口")
    username: str = Field(description="SSH 用户名")
    private_key_path: Optional[str] = Field(default=None, description="SSH 私钥路径")
    password: Optional[str] = Field(default=None, description="SSH 密码（不推荐）")

    def __str__(self) -> str:
        """友好的字符串表示。"""
        return f"{self.name} ({self.username}@{self.host}:{self.port})"


class MonitorConfig(BaseModel):
    """监控配置文件。"""

    servers: List[ServerConfig] = Field(default_factory=list, description="服务器列表")
    default_server: Optional[str] = Field(default=None, description="默认服务器名称")
    connect_timeout: int = Field(default=10, description="连接超时（秒）")
    command_timeout: int = Field(default=30, description="命令执行超时（秒）")

    def get_server(self, name: str) -> Optional[ServerConfig]:
        """根据名称获取服务器配置。"""
        for server in self.servers:
            if server.name == name:
                return server
        return None

    def get_default_server(self) -> Optional[ServerConfig]:
        """获取默认服务器。"""
        if self.default_server:
            return self.get_server(self.default_server)
        if self.servers:
            return self.servers[0]
        return None


def load_config(config_path: Path) -> MonitorConfig:
    """从 YAML 文件加载配置。"""
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return MonitorConfig(**data)
