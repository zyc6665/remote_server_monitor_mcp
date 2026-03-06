#!/bin/bash
# 快速安装脚本

set -e

echo "🚀 发财一号的服务器监控 MCP 安装脚本"
echo "======================================"

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python 版本: $python_version"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip install -r requirements.txt

# 创建配置文件
echo ""
echo "⚙️  创建配置文件..."
if [ ! -f "config/servers.yaml" ]; then
    cp config/servers.example.yaml config/servers.yaml
    echo "✓ 已创建 config/servers.yaml"
    echo ""
    echo "⚠️  请编辑 config/servers.yaml 并填入你的服务器信息"
    echo "   vim config/servers.yaml"
else
    echo "✓ 配置文件已存在"
fi

# 运行测试
echo ""
echo "🧪 运行测试..."
python -m pytest tests/ -v || echo "⚠️  测试未通过，请检查"

echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "  1. 编辑 config/servers.yaml 添加服务器"
echo "  2. 运行测试: python -m server_monitor_mcp"
echo "  3. 在 OpenClaw 中集成（见 DEPLOYMENT.md）"
