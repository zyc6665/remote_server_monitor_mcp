# MCP 服务器部署指南

## 1. 安装依赖

```bash
cd /Users/zyccc/Desktop/small_project
pip install -r requirements.txt
```

或使用开发模式：

```bash
pip install -e .
```

## 2. 配置服务器

```bash
# 复制示例配置
cp config/servers.example.yaml config/servers.yaml

# 编辑配置，填入你的服务器信息
vim config/servers.yaml
```

## 3. 测试 MCP 服务器

```bash
# 直接运行测试
python -m server_monitor_mcp
```

## 4. 在 OpenClaw 中集成

编辑 OpenClaw 配置文件（通常在 `~/.openclaw/config.yml`）：

```yaml
mcp:
  servers:
    server-monitor:
      command: python -m server_monitor_mcp
      working_directory: /Users/zyccc/Desktop/small_project
```

重启 OpenClaw Gateway：

```bash
openclaw gateway restart
```

## 5. 使用 MCP 工具

重启后，我就能通过 MCP 调用这些工具了！

```python
# 例如：查看系统状态
await call_tool("get_system_stats", {"server": "production"})

# 查看进程列表
await call_tool("list_processes", {"server": "production", "limit": 10})
```

## 6. 常见问题

### 配置文件找不到
确保 `config/servers.yaml` 存在且格式正确。

### SSH 连接失败
- 检查服务器 IP、端口、用户名
- 确认私钥路径正确，或使用密码
- 测试 SSH 连接：`ssh user@host`

### 权限问题
确保私钥文件权限正确：
```bash
chmod 600 ~/.ssh/id_rsa
```
