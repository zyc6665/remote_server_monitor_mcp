# 贡献指南

感谢你考虑为 Server Monitor MCP 做贡献！💰

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请通过 [GitHub Issues](../../issues) 报告，并包含：
- 详细的问题描述
- 复现步骤
- 期望行为 vs 实际行为
- 环境信息（操作系统、Python 版本等）
- 相关的日志或截图

### 提出新功能

在创建 Issue 之前，请先检查是否已有类似的功能请求。如果已有，请在该 Issue 下留言支持。

### 提交代码

#### 1. Fork 仓库

点击右上角的 "Fork" 按钮。

#### 2. 创建分支

```bash
git clone https://github.com/你的用户名/remote_server_monitor_mcp.git
cd remote_server_monitor_mcp
git checkout -b feature/你的功能名
```

#### 3. 安装依赖

```bash
pip install -r requirements-dev.txt
pre-commit install
```

#### 4. 编写代码

- 遵循现有的代码风格
- 编写测试
- 运行 `pre-commit run --all-files` 确保通过所有检查
- 运行 `pytest` 确保所有测试通过

#### 5. 提交代码

```bash
git add .
git commit -m "描述你的更改"
git push origin feature/你的功能名
```

#### 6. 创建 Pull Request

访问原仓库，点击 "New Pull Request"，描述你的更改。

### 代码规范

- 使用 Black 进行代码格式化
- 使用 Flake8 进行代码风格检查
- 使用 Mypy 进行类型检查
- 编写清晰的 commit message
- 为新功能编写测试

### 行为准则

- 尊重所有贡献者
- 使用礼貌和专业的语言
- 欢迎不同意见的讨论

## 许可证

提交代码即表示你同意你的代码将在 [MIT License](LICENSE) 下发布。

## 联系方式

如有问题，请通过 [GitHub Issues](../../issues) 联系。

---

**感谢你的贡献！** 🎉
