# 变更日志

本文档记录 Server Monitor MCP 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- WebSocket 实时监控
- 历史数据存储和可视化
- 自定义监控指标
- 告警通知（邮件、Telegram 等）

---

## [0.1.0] - 2026-03-06

### 新增
- 🎉 首次发布
- ✨ 基于 MCP 的远程服务器监控系统
- 🔍 系统资源监控（CPU、内存、磁盘、负载）
- 📋 进程管理（列表、详情、终止）
- 💻 远程命令执行
- 🔐 SSH 安全连接（密钥和密码认证）
- 🌐 多服务器管理
- 📚 完整的文档和示例
- 🧪 单元测试
- 🎨 Black 代码格式化
- 🔍 Flake8 代码风格检查
- 🔒 Mypy 类型检查
- 🛡️ CodeQL 安全扫描
- 🔄 GitHub Actions CI/CD
- 📦 Pre-commit 自动检查
- 📖 快速开始指南
- 📋 部署文档
- 🔍 使用示例

### 技术栈
- Python 3.10+
- MCP SDK
- Paramiko (SSH)
- Pydantic (数据验证)
- PyYAML (配置管理)
- pytest (测试)

---

[未发布]: https://github.com/zyc6665/remote_server_monitor_mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/zyc6665/remote_server_monitor_mcp/releases/tag/v0.1.0
