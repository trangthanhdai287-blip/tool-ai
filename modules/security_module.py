"""SecurityModule - Hàm quét bảo mật cơ bản"""

import os
import subprocess
import json
from datetime import datetime
from typing import Dict, List, Any

class SecurityModule:
    """Module quét bảo mật cơ bản cho hệ thống"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.scan_results = {}
        self.timestamp = datetime.now().isoformat()
    
    def log(self, message: str):
        """Log thông báo"""
        if self.verbose:
            print(f"[SecurityModule] {message}")
    
    def check_sudo_permissions(self) -> Dict[str, Any]:
        """Kiểm tra quyền sudo của người dùng hiện tại"""
        self.log("Checking sudo permissions...")
        try:
            result = subprocess.run(
                ["sudo", "-l"],
                capture_output=True,
                text=True,
                timeout=5
            )
            has_sudo = result.returncode == 0
            return {
                "has_sudo": has_sudo,
                "status": "OK" if has_sudo else "NO_SUDO",
                "message": "User has sudo privileges" if has_sudo else "User does not have sudo privileges"
            }
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}
    
    def check_firewall_status(self) -> Dict[str, Any]:
        """Kiểm tra trạng thái firewall"""
        self.log("Checking firewall status...")
        try:
            # Kiểm tra UFW
            result = subprocess.run(
                ["sudo", "ufw", "status"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {
                    "firewall": "UFW",
                    "status": result.stdout.strip(),
                    "active": "active" in result.stdout.lower()
                }
            return {"firewall": "UNKNOWN", "status": "NOT_FOUND"}
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}
    
    def check_open_ports(self) -> Dict[str, Any]:
        """Kiểm tra các cổng mở"""
        self.log("Checking open ports...")
        try:
            result = subprocess.run(
                ["netstat", "-tlnp"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                ports = []
                for line in lines[2:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            ports.append({
                                "proto": parts[0],
                                "local_address": parts[3],
                                "state": parts[5] if len(parts) > 5 else "UNKNOWN"
                            })
                return {"ports": ports, "count": len(ports)}
            return {"error": "netstat not available"}
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}
    
    def check_failed_logins(self) -> Dict[str, Any]:
        """Kiểm tra số lần đăng nhập thất bại"""
        self.log("Checking failed login attempts...")
        try:
            result = subprocess.run(
                ["grep", "Failed password", "/var/log/auth.log"],
                capture_output=True,
                text=True,
                timeout=5
            )
            lines = result.stdout.strip().split('\n') if result.stdout else []
            return {
                "failed_attempts": len([l for l in lines if l]),
                "recent_attempts": lines[-5:] if lines else []
            }
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}
    
    def check_disk_usage(self) -> Dict[str, Any]:
        """Kiểm tra mức sử dụng đĩa"""
        self.log("Checking disk usage...")
        try:
            result = subprocess.run(
                ["df", "-h", "/"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    return {
                        "filesystem": parts[0],
                        "size": parts[1],
                        "used": parts[2],
                        "available": parts[3],
                        "percent": parts[4]
                    }
            return {"error": "Unable to get disk usage"}
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}
    
    def check_running_services(self) -> Dict[str, Any]:
        """Kiểm tra các dịch vụ đang chạy"""
        self.log("Checking running services...")
        try:
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                services = [line.split()[0] for line in lines[1:] if line.strip()]
                return {
                    "count": len(services),
                    "services": services[:20]  # Lấy 20 dịch vụ đầu tiên
                }
            return {"error": "systemctl not available"}
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}
    
    def run_full_scan(self) -> Dict[str, Any]:
        """Chạy quét bảo mật toàn diện"""
        self.log("Running full security scan...")
        results = {
            "timestamp": self.timestamp,
            "scan_type": "full_security_scan",
            "checks": {}
        }
        
        results["checks"]["sudo_permissions"] = self.check_sudo_permissions()
        results["checks"]["firewall"] = self.check_firewall_status()
        results["checks"]["open_ports"] = self.check_open_ports()
        results["checks"]["failed_logins"] = self.check_failed_logins()
        results["checks"]["disk_usage"] = self.check_disk_usage()
        results["checks"]["running_services"] = self.check_running_services()
        
        self.scan_results = results
        self.log("Full scan completed")
        return results
    
    def get_results_json(self) -> str:
        """Lấy kết quả dưới dạng JSON"""
        return json.dumps(self.scan_results, indent=2, ensure_ascii=False)
