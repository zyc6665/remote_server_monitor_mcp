# 项目结构说明

```
small_project/
├── README.md                    # 项目说明文档
├── DEPLOYMENT.md               # 部署指南
├── pyproject.toml             # Python 项目配置
├── requirements.txt           # Python 依赖列表
├── .gitignore                # Git 忽略文件
│
├── config/                   # 配置文件目录
│   └── servers.example.yaml  # 服务器配置示例
│
├── src/                     # 源代码目录
│   └── server_monitor_mcp/  # MCP 服务器包
│       ├── __init__.py      # 包初始化
│       ├── __main__.py      # 入口文件
│       ├── server.py        # MCP 服务器核心逻辑
│       │
│       ├── ssh/            # SSH 连接管理
│       │   ├── __init__.py
│       │   ├── config.py   # 配置管理（ServerConfig, MonitorConfig）
│       │   └── client.py   # SSH 客户端封装（SSHClient, SSHResult）
│       │
│       ├── tools/          # MCP 工具实现
│       │   ├── __init__.py
│       │   ├── system.py   # 系统监控（CPU/内存/磁盘）
│       │   ├── process.py  # 进程管理（列表/详情/终止）
│       │   └── command.py  # 命令执行
│       │
│       └── utils/          # 工具模块
│           ├── __init__.py
│           └── logger.py   # 日志工具
│
├── tests/                   # 测试目录
│   ├── __init__.py
│   └── test_ssh_client.py   # SSH 客户端测试
│
└── docs/                    # 文档目录
    └── PROJECT_STRUCTURE.md # 本文件
```

## 模块说明

### server.py
MCP 服务器的核心入口，负责：
- 工具注册（list_tools）
- 工具调用（call_tool）
- 与 OpenClaw 的 MCP 协议通信

### ssh/
SSH 连接管理模块：
- **config.py**: 使用 Pydantic 进行配置验证
- **client.py**: 封装 Paramiko，提供上下文管理器支持

### tools/
MCP 工具实现，每个文件对应一类功能：
- **system.py**: `get_system_stats` - 获取系统资源
- **process.py**: `list_processes`, `get_process_info`, `kill_process`
- **command.py**: `execute_command` - 执行任意命令

### utils/
通用工具：
- **logger.py**: 带颜色的日志记录器，支持文件和控制台

## 设计原则

1. **模块化**: SSH、工具、工具分离，职责清晰
2. **类型安全**: 使用 Pydantic 模型进行数据验证
3. **企业级**: 完整的文档、测试、配置管理
4. **可扩展**: 易于添加新的监控工具
