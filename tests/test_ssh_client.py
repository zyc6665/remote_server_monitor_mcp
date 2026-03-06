"""SSH 客户端测试。"""

import pytest

from server_monitor_mcp.ssh.config import ServerConfig, MonitorConfig


def test_server_config_valid():
    """测试有效的服务器配置。"""
    config = ServerConfig(
        name="test",
        host="192.168.1.1",
        username="user",
    )
    assert config.name == "test"
    assert config.host == "192.168.1.1"
    assert config.port == 22  # 默认值


def test_server_config_with_key():
    """测试带密钥的服务器配置。"""
    config = ServerConfig(
        name="test",
        host="192.168.1.1",
        username="user",
        private_key_path="/home/user/.ssh/id_rsa",
    )
    assert config.private_key_path == "/home/user/.ssh/id_rsa"
    assert config.password is None


def test_monitor_config_empty():
    """测试空的监控配置。"""
    config = MonitorConfig()
    assert len(config.servers) == 0
    assert config.get_default_server() is None


def test_monitor_config_with_servers():
    """测试带服务器的监控配置。"""
    config = MonitorConfig(
        servers=[
            ServerConfig(name="prod", host="10.0.0.1", username="admin"),
            ServerConfig(name="dev", host="10.0.0.2", username="dev"),
        ],
        default_server="prod",
    )
    assert len(config.servers) == 2

    # 获取指定服务器
    prod = config.get_server("prod")
    assert prod is not None
    assert prod.host == "10.0.0.1"

    # 获取默认服务器
    default = config.get_default_server()
    assert default is not None
    assert default.name == "prod"


def test_monitor_config_get_nonexistent():
    """测试获取不存在的服务器。"""
    config = MonitorConfig(servers=[ServerConfig(name="test", host="10.0.0.1", username="user")])
    result = config.get_server("nonexistent")
    assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
