# 快速开始指南

## 5 分钟快速部署

### 1️⃣ 安装依赖

```bash
cd /Users/zyccc/Desktop/small_project
pip install -r requirements.txt
```

### 2️⃣ 配置服务器

```bash
# 复制示例配置
cp config/servers.example.yaml config/servers.yaml

# 编辑配置（替换成你的服务器信息）
vim config/servers.yaml
```

**最小配置示例：**

```yaml
servers:
  - name: myserver
    host: 192.168.1.100
    port: 22
    username: ubuntu
    private_key_path: ~/.ssh/id_rsa

default_server: myserver
```

### 3️⃣ 测试运行

```bash
python -m server_monitor_mcp
```

如果看到 "🚀 发财一号的服务器监控 MCP 服务器启动中..."，说明成功了！

### 4️⃣ 在 OpenClaw 中集成

编辑 `~/.openclaw/config.yml`，添加 MCP 服务器配置：

```yaml
mcp:
  servers:
    server-monitor:
      command: python -m server_monitor_mcp
      working_directory: /Users/zyccc/Desktop/small_project
```

重启 Gateway：

```bash
openclaw gateway restart
```

### 5️⃣ 开始使用

重启后，你就可以让我调用这些工具了！

```
你：查看一下服务器的系统状态
我：[调用 get_system_stats 工具]
```

## 验证安装

运行测试：

```bash
python -m pytest tests/ -v
```

或使用快速安装脚本：

```bash
./scripts/setup.sh
```

## 下一步

- 查看 [DEPLOYMENT.md](./DEPLOYMENT.md) 了解详细部署
- 查看 [EXAMPLES.md](./docs/EXAMPLES.md) 了解使用示例
- 查看 [PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md) 了解项目结构

## 常见问题

### Q: 如何连接多台服务器？
A: 在 `config/servers.yaml` 中添加多个服务器配置即可。

### Q: 支持密码认证吗？
A: 支持，但不推荐生产环境使用。在配置中添加 `password` 字段即可。

### Q: 如何自定义监控指标？
A: 添加新工具到 `src/server_monitor_mcp/tools/` 目录。

---

**大财主，现在你可以开始监控你的服务器了！** 💰🚀
