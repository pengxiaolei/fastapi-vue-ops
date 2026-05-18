import paramiko
import io
import re
from typing import Dict, Optional, Tuple

from app.config import settings
from app.models.machine import AuthType


class SSHClient:
    """SSH客户端工具，用于连接远程机器并执行命令"""

    def __init__(
        self,
        hostname: str,
        username: str,
        port: int = 22,
        auth_type: AuthType = AuthType.PASSWORD,
        password: Optional[str] = None,
        private_key: Optional[str] = None,
        timeout: int = None,
    ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.auth_type = auth_type
        self.password = password
        self.private_key = private_key
        self.timeout = timeout or settings.ssh_timeout
        self.client: Optional[paramiko.SSHClient] = None

    def connect(self) -> Tuple[bool, str]:
        """建立SSH连接"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.auth_type == AuthType.KEY and self.private_key:
                # 使用密钥认证
                private_key_io = io.StringIO(self.private_key)
                pkey = paramiko.RSAKey.from_private_key(private_key_io)
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    pkey=pkey,
                    timeout=self.timeout,
                )
            else:
                # 使用密码认证
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                )

            return True, "连接成功"
        except paramiko.AuthenticationException:
            return False, "认证失败：用户名或密码错误"
        except paramiko.SSHException as e:
            return False, f"SSH连接错误: {str(e)}"
        except TimeoutError:
            return False, "连接超时"
        except Exception as e:
            return False, f"连接失败: {str(e)}"

    def execute_command(self, command: str) -> Tuple[bool, str]:
        """执行远程命令"""
        if not self.client:
            return False, "未建立连接"

        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()

            if exit_status == 0:
                return True, stdout.read().decode("utf-8")
            else:
                return False, stderr.read().decode("utf-8")
        except Exception as e:
            return False, f"执行命令失败: {str(e)}"

    def get_system_info(self) -> Dict:
        """获取系统信息"""
        info = {
            "os_type": None,
            "cpu_cores": None,
            "memory_total": None,
            "disk_total": None,
            "cpu_usage": None,
            "memory_usage": None,
            "disk_usage": None,
        }

        # 获取操作系统类型
        success, output = self.execute_command("uname -s")
        if success:
            info["os_type"] = output.strip()

        # 获取CPU核数
        success, output = self.execute_command("nproc")
        if success:
            try:
                info["cpu_cores"] = int(output.strip())
            except ValueError:
                pass

        # 获取内存信息（Linux）
        success, output = self.execute_command("free -m")
        if success:
            lines = output.strip().split("\n")
            if len(lines) >= 2:
                parts = re.split(r"\s+", lines[1])
                if len(parts) >= 2:
                    try:
                        info["memory_total"] = int(parts[1])
                        if len(parts) >= 3:
                            used = int(parts[2])
                            info["memory_usage"] = round((used / info["memory_total"]) * 100, 2)
                    except (ValueError, ZeroDivisionError):
                        pass

        # 获取磁盘信息
        success, output = self.execute_command("df -BG /")
        if success:
            lines = output.strip().split("\n")
            if len(lines) >= 2:
                parts = re.split(r"\s+", lines[1])
                if len(parts) >= 2:
                    try:
                        info["disk_total"] = int(parts[1].replace("G", ""))
                        if len(parts) >= 5:
                            usage_str = parts[4].replace("%", "")
                            info["disk_usage"] = float(usage_str)
                    except ValueError:
                        pass

        # 获取CPU使用率
        success, output = self.execute_command("top -bn1 | grep 'Cpu(s)'")
        if success:
            try:
                cpu_parts = re.split(r"[\s,]+", output)
                for i, part in enumerate(cpu_parts):
                    if "id" in part:
                        idle_str = cpu_parts[i - 1]
                        idle = float(idle_str.replace("%", ""))
                        info["cpu_usage"] = round(100 - idle, 2)
                        break
            except (ValueError, IndexError):
                pass

        # 备用方案获取CPU使用率
        if info["cpu_usage"] is None:
            success, output = self.execute_command("cat /proc/loadavg")
            if success:
                try:
                    parts = output.strip().split()
                    if info["cpu_cores"] and info["cpu_cores"] > 0:
                        load1 = float(parts[0])
                        info["cpu_usage"] = round((load1 / info["cpu_cores"]) * 100, 2)
                except (ValueError, IndexError, ZeroDivisionError):
                    pass

        return info

    def close(self):
        """关闭连接"""
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        success, msg = self.connect()
        if not success:
            raise Exception(msg)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
