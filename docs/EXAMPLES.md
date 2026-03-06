# MCP 工具使用示例

## 通过 OpenClaw 调用

配置完成后，我可以通过 MCP 调用这些工具：

### 1. 查看系统状态

```python
# 获取生产服务器的系统资源
get_system_stats(server="production")

# 返回示例：
{
  "cpu_percent": 25.5,
  "memory_total": 16384,
  "memory_used": 8192,
  "memory_percent": 50.0,
  "disk_total": 500.0,
  "disk_used": 250.0,
  "disk_percent": 50.0,
  "uptime": "up 5 days, 2 hours",
  "load_average": "0.05, 0.10, 0.08"
}
```

### 2. 列出进程

```python
# 列出 CPU 使用最高的 10 个进程
list_processes(server="production", limit=10)

# 过滤特定进程
list_processes(server="production", filter_name="nginx", limit=5)
```

### 3. 查看进程详情

```python
# 获取特定进程的信息
get_process_info(server="production", pid=1234)

# 返回示例：
{
  "pid": 1234,
  "user": "root",
  "cpu_percent": 2.5,
  "mem_percent": 1.2,
  "command": "nginx",
  "args": "nginx: master process",
  "time": "1:23:45"
}
```

### 4. 终止进程

```python
# 优雅终止（SIGTERM）
kill_process(server="production", pid=1234)

# 强制终止（SIGKILL）
kill_process(server="production", pid=1234, signal=9)
```

### 5. 执行命令

```python
# 执行任意 shell 命令
execute_command(
    server="production",
    command="ls -la /var/log",
    timeout=30
)

# 返回命令执行结果
```

## 直接测试 MCP 服务器

```bash
# 直接运行 MCP 服务器
python -m server_monitor_mcp

# 或者安装后运行
server-monitor-mcp
```

## 常见监控场景

### 场景 1：检查服务器健康状况

```python
# 1. 检查系统资源
stats = get_system_stats(server="production")

# 2. 如果 CPU 过高，检查进程
if stats.cpu_percent > 80:
    processes = list_processes(server="production", limit=20)
    print(f"CPU 过高！Top 进程: {processes}")
```

### 场景 2：重启服务

```python
# 1. 查找进程
processes = list_processes(server="production", filter_name="myapp")

# 2. 终止旧进程
for p in processes:
    kill_process(server="production", pid=p.pid)

# 3. 启动新进程
execute_command(server="production", command="systemctl start myapp")
```

### 场景 3：日志分析

```python
# 查看最近的错误日志
execute_command(
    server="production",
    command="tail -100 /var/log/myapp/error.log | grep ERROR"
)
```
