"""服务器监控 MCP 服务器入口。"""

import asyncio
import sys

from .server import ServerMonitorMCP
from .utils.logger import logger


def main() -> None:
    """主函数。"""
    logger.info("🚀 发财一号的服务器监控 MCP 服务器启动中...")

    # 创建并运行服务器
    mcp_server = ServerMonitorMCP()

    try:
        asyncio.run(mcp_server.run())
    except KeyboardInterrupt:
        logger.info("服务器已停止")
        sys.exit(0)
    except Exception as e:
        logger.error(f"服务器错误: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
