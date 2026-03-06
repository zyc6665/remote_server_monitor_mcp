"""进程管理工具。"""

from typing import List, Optional

from pydantic import BaseModel, Field
from mcp.server.models import Tool

from ..ssh.client import SSHClient


class ProcessInfo(BaseModel):
    """进程信息。"""

    pid: int = Field(description="进程 ID")
    user: str = Field(description="用户")
    cpu_percent: float = Field(description="CPU 使用率 (%)")
    mem_percent: float = Field(description="内存使用率 (%)")
    command: str = Field(description="命令")
    args: str = Field(description="参数")
    time: str = Field(description="CPU 时间")


def list_processes(
    server_name: str,
    ssh_client: SSHClient,
    limit: int = 10,
    filter_name: Optional[str] = None,
) -> List[ProcessInfo]:
    """
    列出运行中的进程。

    Args:
        server_name: 服务器名称
        ssh_client: SSH 客户端
        limit: 返回的最大进程数
        filter_name: 进程名过滤（可选）

    Returns:
        List[ProcessInfo]: 进程列表
    """
    # 使用 ps 命令获取进程信息
    # ps aux 的格式: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
    cmd = "ps aux --sort=-%cpu | head -n 20"
    result = ssh_client.execute(cmd, timeout=15)

    if not result.success:
        return []

    processes = []
    lines = result.stdout.split("\n")[1:]  # 跳过标题行

    for line in lines:
        if not line.strip():
            continue

        parts = line.split(None, 10)  # 最多分割成 11 部分
        if len(parts) < 11:
            continue

        try:
            process = ProcessInfo(
                pid=int(parts[1]),
                user=parts[0],
                cpu_percent=float(parts[2]),
                mem_percent=float(parts[3]),
                command=parts[10].split()[0] if parts[10] else "",
                args=parts[10] if parts[10] else "",
                time=parts[9],
            )

            # 过滤
            if filter_name and filter_name.lower() not in process.command.lower():
                continue

            processes.append(process)

            if len(processes) >= limit:
                break

        except (ValueError, IndexError):
            continue

    return processes


def get_process_info(
    server_name: str, ssh_client: SSHClient, pid: int
) -> Optional[ProcessInfo]:
    """
    获取特定进程的详细信息。

    Args:
        server_name: 服务器名称
        ssh_client: SSH 客户端
        pid: 进程 ID

    Returns:
        Optional[ProcessInfo]: 进程信息，不存在则返回 None
    """
    cmd = f"ps -p {pid} -o user=,pid=,%cpu=,%mem=,etime=,comm=,args="
    result = ssh_client.execute(cmd, timeout=10)

    if not result.success or not result.stdout.strip():
        return None

    parts = result.stdout.strip().split(None, 6)
    if len(parts) < 7:
        return None

    return ProcessInfo(
        pid=int(parts[1]),
        user=parts[0],
        cpu_percent=float(parts[2]),
        mem_percent=float(parts[3]),
        command=parts[5],
        args=parts[6],
        time=parts[4],
    )


def kill_process(
    server_name: str, ssh_client: SSHClient, pid: int, signal: int = 15
) -> bool:
    """
    终止指定进程。

    Args:
        server_name: 服务器名称
        ssh_client: SSH 客户端
        pid: 进程 ID
        signal: 信号（默认 15 = SIGTERM）

    Returns:
        bool: 是否成功
    """
    cmd = f"kill -{signal} {pid}"
    result = ssh_client.execute(cmd, timeout=10)
    return result.success


def list_processes_tool() -> Tool:
    """获取列出进程工具定义。"""
    return Tool(
        name="list_processes",
        description="列出远程服务器上运行中的进程，可按进程名过滤，返回 CPU 使用率最高的进程",
        inputSchema={
            "type": "object",
            "properties": {
                "server": {
                    "type": "string",
                    "description": "服务器名称（默认使用配置中的默认服务器）",
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "返回的最大进程数",
                },
                "filter_name": {
                    "type": "string",
                    "description": "进程名过滤（可选）",
                },
            },
        },
    )


def get_process_info_tool() -> Tool:
    """获取进程详情工具定义。"""
    return Tool(
        name="get_process_info",
        description="获取远程服务器上特定进程的详细信息",
        inputSchema={
            "type": "object",
            "properties": {
                "server": {
                    "type": "string",
                    "description": "服务器名称（默认使用配置中的默认服务器）",
                },
                "pid": {
                    "type": "integer",
                    "description": "进程 ID",
                },
            },
            "required": ["pid"],
        },
    )


def kill_process_tool() -> Tool:
    """获取终止进程工具定义。"""
    return Tool(
        name="kill_process",
        description="终止远程服务器上的指定进程",
        inputSchema={
            "type": "object",
            "properties": {
                "server": {
                    "type": "string",
                    "description": "服务器名称（默认使用配置中的默认服务器）",
                },
                "pid": {
                    "type": "integer",
                    "description": "进程 ID",
                },
                "signal": {
                    "type": "integer",
                    "default": 15,
                    "description": "信号（15=SIGTERM, 9=SIGKILL）",
                },
            },
            "required": ["pid"],
        },
    )
