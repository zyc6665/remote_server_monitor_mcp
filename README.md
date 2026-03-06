# Server Monitor MCP

[![测试](https://github.com/zyc6665/remote_server_monitor_mcp/workflows/测试/badge.svg)](https://github.com/zyc6665/remote_server_monitor_mcp/actions/workflows/test.yml)
[![代码质量检查](https://github.com/zyc6665/remote_server_monitor_mcp/workflows/代码质量检查/badge.svg)](https://github.com/zyc6665/remote_server_monitor_mcp/actions/workflows/lint.yml)
[![安全扫描](https://github.com/zyc6665/remote_server_monitor_mcp/workflows/安全扫描/badge.svg)](https://github.com/zyc6665/remote_server_monitor_mcp/actions/workflows/security.yml)
[![Python 版本](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一个基于 MCP (Model Context Protocol) 的远程服务器监测系统。💰 由发财一号出品。

## 功能特性

- 🔍 实时系统监控（CPU、内存、磁盘、网络）
- 📋 进程管理（列表、详情、终止）
- 💻 远程命令执行
- 🌐 多服务器管理
- 🔐 SSH 安全连接

## 技术栈

- Python 3.10+
- MCP SDK
- Paramiko (SSH)
- Pydantic (数据验证)

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或使用 pip install -e . 开发模式
pip install -e .
```

## 配置

编辑 `config/servers.yaml` 添加你的服务器信息：

```yaml
servers:
  - name: production
    host: 192.168.1.100
    port: 22
    username: ubuntu
    private_key_path: ~/.ssh/id_rsa
  - name: staging
    host: 192.168.1.101
    port: 22
    username: deploy
    password: your_password
```

## 运行

```bash
# 直接运行
python -m server_monitor_mcp

# 或使用 MCP 客户端连接
# 在你的 MCP 客户端配置中指定此服务器
```

## MCP 工具

| 工具 | 描述 |
|------|------|
| `get_system_stats` | 获取系统资源使用情况 |
| `list_processes` | 列出运行中的进程 |
| `execute_command` | 执行远程命令 |
| `get_process_info` | 获取进程详细信息 |
| `kill_process` | 终止指定进程 |

## 项目结构

```
server_monitor_mcp/
├── src/server_monitor_mcp/    # 源代码
│   ├── tools/                 # MCP 工具实现
│   ├── ssh/                   # SSH 连接管理
│   └── utils/                 # 工具函数
├── tests/                     # 测试
├── docs/                      # 文档
└── config/                    # 配置文件
```

## License

MIT

## CI/CD

项目使用 GitHub Actions 进行持续集成和持续部署：

- **测试**：在 Python 3.10/3.11/3.12 上运行测试
- **代码质量检查**：Black、Flake8、Mypy 静态分析
- **安全扫描**：CodeQL 自动安全检测
- **构建和发布**：自动构建和发布 GitHub Release

### 本地开发

安装 pre-commit 进行本地代码检查：

```bash
pip install pre-commit
pre-commit install
```

每次提交前会自动运行代码检查。
