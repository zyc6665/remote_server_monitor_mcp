"""MCP 服务器主模块。"""

from pathlib import Path
from typing import Any, Dict

from mcp.server.models import InitializationOptions
from mcp.server.server import NotificationOptions, Server
from mcp.types import Tool, TextContent

from .ssh.config import load_config, MonitorConfig
from .ssh.client import SSHClient
from .tools import (
    get_system_stats_tool,
    list_processes_tool,
    get_process_info_tool,
    kill_process_tool,
    execute_command_tool,
    get_system_stats,
    list_processes,
    get_process_info,
    kill_process,
    execute_command,
)
from .utils.logger import logger


class ServerMonitorMCP:
    """服务器监控 MCP 服务器。"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化 MCP 服务器。

        Args:
            config_path: 配置文件路径，默认为 config/servers.yaml
        """
        if config_path is None:
            # 默认配置路径
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "servers.yaml"

        # 检查配置文件
        if not config_path.exists():
            logger.warning(f"配置文件不存在: {config_path}")
            logger.info("请复制 config/servers.example.yaml 为 config/servers.yaml 并配置")
            self.config = MonitorConfig(servers=[])
        else:
            self.config = load_config(config_path)

        # 创建 MCP 服务器实例
        self.server = Server("server-monitor-mcp")

        # 注册处理器
        self._register_handlers()

        logger.info("MCP 服务器已初始化")
        logger.info(f"已配置 {len(self.config.servers)} 台服务器")

    def _register_handlers(self) -> None:
        """注册 MCP 服务器处理器。"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """列出可用的工具。"""
            return [
                get_system_stats_tool(),
                list_processes_tool(),
                get_process_info_tool(),
                kill_process_tool(),
                execute_command_tool(),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
            """调用工具。"""
            try:
                # 获取服务器名称
                server_name = arguments.get("server") or self.config.get_default_server()
                if not server_name:
                    return [
                        TextContent(
                            type="text",
                            text="错误：未指定服务器且没有配置默认服务器",
                        )
                    ]

                # 获取服务器配置
                server_config = self.config.get_server(server_name)
                if not server_config:
                    return [TextContent(type="text", text=f"错误：找不到服务器 '{server_name}'")]

                # 连接 SSH
                with SSHClient(server_config, timeout=self.config.connect_timeout) as client:
                    # 根据工具名称执行相应操作
                    if name == "get_system_stats":
                        stats = get_system_stats(server_name, client)
                        return [TextContent(type="text", text=stats.model_dump_json(indent=2))]

                    elif name == "list_processes":
                        limit = arguments.get("limit", 10)
                        filter_name = arguments.get("filter_name")
                        processes = list_processes(server_name, client, limit, filter_name)
                        result = {
                            "server": server_name,
                            "count": len(processes),
                            "processes": [p.model_dump() for p in processes],
                        }
                        return [TextContent(type="text", text=str(result))]

                    elif name == "get_process_info":
                        pid = arguments.get("pid")
                        process = get_process_info(server_name, client, pid)
                        if process:
                            return [
                                TextContent(type="text", text=process.model_dump_json(indent=2))
                            ]
                        else:
                            return [TextContent(type="text", text=f"未找到 PID {pid} 的进程")]

                    elif name == "kill_process":
                        pid = arguments.get("pid")
                        signal = arguments.get("signal", 15)
                        success = kill_process(server_name, client, pid, signal)
                        return [
                            TextContent(
                                type="text",
                                text=f"{'成功' if success else '失败'}终止 PID {pid}",
                            )
                        ]

                    elif name == "execute_command":
                        command = arguments.get("command")
                        timeout = arguments.get("timeout")
                        result = execute_command(server_name, client, command, timeout)
                        output = (
                            f"命令: {command}\n退出码: {result.exit_code}\n\n"
                            f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
                        )
                        return [TextContent(type="text", text=output)]

                    else:
                        return [TextContent(type="text", text=f"未知工具: {name}")]

            except Exception as e:
                logger.error(f"工具调用失败: {e}", exc_info=True)
                return [TextContent(type="text", text=f"错误: {str(e)}")]

    async def run(self) -> None:
        """启动 MCP 服务器。"""
        logger.info("启动 MCP 服务器...")
        async with self.server.stdio_transport() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="server-monitor-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
