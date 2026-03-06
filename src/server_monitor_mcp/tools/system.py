"""系统监控工具。"""

from typing import Optional

from pydantic import BaseModel, Field
from mcp.server.models import Tool

from ..ssh.client import SSHClient


class SystemStats(BaseModel):
    """系统统计信息。"""

    cpu_percent: float = Field(description="CPU 使用率 (%)")
    memory_total: int = Field(description="总内存 (MB)")
    memory_used: int = Field(description="已用内存 (MB)")
    memory_percent: float = Field(description="内存使用率 (%)")
    disk_total: int = Field(description="总磁盘空间 (GB)")
    disk_used: int = Field(description="已用磁盘空间 (GB)")
    disk_percent: float = Field(description="磁盘使用率 (%)")
    uptime: str = Field(description="系统运行时间")
    load_average: str = Field(description="平均负载")


def get_system_stats(server_name: str, ssh_client: SSHClient) -> SystemStats:
    """
    获取系统资源使用情况。

    Args:
        server_name: 服务器名称
        ssh_client: SSH 客户端

    Returns:
        SystemStats: 系统统计信息
    """
    # CPU 使用率
    cpu_result = ssh_client.execute(
        "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'",
        timeout=10,
    )
    cpu_percent = float(cpu_result.stdout.strip()) if cpu_result.success else 0.0

    # 内存信息
    mem_result = ssh_client.execute("free -m", timeout=10)
    if mem_result.success:
        lines = mem_result.stdout.split("\n")
        mem_line = lines[1].split()
        mem_total = int(mem_line[1])
        mem_used = int(mem_line[2])
        mem_percent = (mem_used / mem_total) * 100
    else:
        mem_total = mem_used = mem_percent = 0

    # 磁盘信息
    disk_result = ssh_client.execute("df -h / | tail -1", timeout=10)
    if disk_result.success:
        parts = disk_result.stdout.split()
        disk_total = _parse_size(parts[1])
        disk_used = _parse_size(parts[2])
        disk_percent = float(parts[4].rstrip("%"))
    else:
        disk_total = disk_used = disk_percent = 0

    # 系统运行时间
    uptime_result = ssh_client.execute("uptime -p", timeout=10)
    uptime = uptime_result.stdout.strip() if uptime_result.success else "Unknown"

    # 平均负载
    loadavg_result = ssh_client.execute("uptime", timeout=10)
    if loadavg_result.success:
        # 提取负载信息: "load average: 0.01, 0.03, 0.05"
        load_avg = loadavg_result.stdout.split("load average:")[1].strip()
    else:
        load_avg = "Unknown"

    return SystemStats(
        cpu_percent=round(cpu_percent, 2),
        memory_total=mem_total,
        memory_used=mem_used,
        memory_percent=round(mem_percent, 2),
        disk_total=disk_total,
        disk_used=disk_used,
        disk_percent=disk_percent,
        uptime=uptime,
        load_average=load_avg,
    )


def _parse_size(size_str: str) -> float:
    """解析大小字符串（如 50G, 1024M）为 GB。"""
    size_str = size_str.upper()
    if size_str.endswith("G"):
        return float(size_str[:-1])
    elif size_str.endswith("M"):
        return float(size_str[:-1]) / 1024
    elif size_str.endswith("T"):
        return float(size_str[:-1]) * 1024
    elif size_str.endswith("K"):
        return float(size_str[:-1]) / (1024 * 1024)
    else:
        return float(size_str) / (1024 * 1024 * 1024)


def get_system_stats_tool() -> Tool:
    """获取系统监控工具定义。"""
    return Tool(
        name="get_system_stats",
        description="获取远程服务器的系统资源使用情况，包括 CPU、内存、磁盘、运行时间和负载",
        inputSchema={
            "type": "object",
            "properties": {
                "server": {
                    "type": "string",
                    "description": "服务器名称（默认使用配置中的默认服务器）",
                },
            },
        },
    )
