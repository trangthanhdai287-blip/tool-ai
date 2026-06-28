"""NetworkTools - Tích hợp nmap, netstat, và các công cụ mạng khác"""

import subprocess
import re
from typing import Dict, List, Any
from datetime import datetime

class NetworkTools:
    """Module tích hợp các công cụ mạng"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.scan_results = {}
    
    def log(self, message: str):
        if self.verbose:
            print(f"[NetworkTools] {message}")
    
    def get_network_interfaces(self) -> Dict[str, Any]:
        """Lấy thông tin các giao diện mạng"""
        self.log("Getting network interfaces...")
        try:
            result = subprocess.run(
                ["ip", "addr"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                interfaces = {}
                current_interface = None
                
                for line in result.stdout.split('\n'):
                    if line.startswith(tuple('0123456789')):
                        match = re.search(r'\d+:\s+(\w+):', line)
                        if match:
                            current_interface = match.group(1)
                            interfaces[current_interface] = {"addresses": []}
                    elif current_interface and 'inet' in line:
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            interfaces[current_interface]["addresses"].append(parts[1])
                
                return {"interfaces": interfaces, "count": len(interfaces)}
            return {"error": "ip command failed"}
        except Exception as e:
            return {"error": str(e)}
    
    def check_listening_ports(self) -> Dict[str, Any]:
        """Kiểm tra các cổng đang lắng nghe"""
        self.log("Checking listening ports...")
        try:
            result = subprocess.run(
                ["ss", "-tlnp"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                ports = []
                lines = result.stdout.strip().split('\n')
                
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            local = parts[3]
                            state = parts[1]
                            ports.append({
                                "address": local,
                                "state": state
                            })
                
                return {"listening_ports": ports, "count": len(ports)}
            return {"error": "ss command failed"}
        except Exception as e:
            return {"error": str(e)}
    
    def check_established_connections(self) -> Dict[str, Any]:
        """Kiểm tra các kết nối thiết lập"""
        self.log("Checking established connections...")
        try:
            result = subprocess.run(
                ["ss", "-tpn", "state", "ESTABLISHED"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                connections = []
                lines = result.stdout.strip().split('\n')
                
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            connections.append({
                                "local": parts[3],
                                "remote": parts[4]
                            })
                
                return {"established_connections": connections, "count": len(connections)}
            return {"error": "ss command failed"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_route_info(self) -> Dict[str, Any]:
        """Lấy thông tin định tuyến"""
        self.log("Getting route information...")
        try:
            result = subprocess.run(
                ["ip", "route"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                routes = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        routes.append(line.strip())
                
                return {"routes": routes, "count": len(routes)}
            return {"error": "ip route command failed"}
        except Exception as e:
            return {"error": str(e)}
    
    def nmap_scan(self, target: str, arguments: str = "-sV -p- --top-ports 1000") -> Dict[str, Any]:
        """Chạy quét nmap
        
        Args:
            target: Địa chỉ IP hoặc hostname để quét
            arguments: Các tham số nmap (mặc định: -sV -p- --top-ports 1000)
        """
        self.log(f"Running nmap scan on {target}...")
        try:
            cmd = ["nmap"] + arguments.split() + [target]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                return {
                    "target": target,
                    "status": "success",
                    "output": result.stdout,
                    "arguments": arguments
                }
            return {"error": "nmap command failed", "stderr": result.stderr}
        except FileNotFoundError:
            return {"error": "nmap is not installed"}
        except Exception as e:
            return {"error": str(e)}
    
    def check_dns_resolution(self, hostname: str) -> Dict[str, Any]:
        """Kiểm tra phân giải DNS"""
        self.log(f"Checking DNS resolution for {hostname}...")
        try:
            result = subprocess.run(
                ["dig", hostname]
                ,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                ips = re.findall(r'^[a-zA-Z0-9\.-]+\.\s+\d+\s+IN\s+A\s+([\d\.]+)', result.stdout, re.MULTILINE)
                return {
                    "hostname": hostname,
                    "ips": ips,
                    "resolved": len(ips) > 0
                }
            return {"error": "dig command failed"}
        except FileNotFoundError:
            return {"error": "dig is not installed"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_interface_stats(self) -> Dict[str, Any]:
        """Lấy thống kê giao diện mạng"""
        self.log("Getting interface statistics...")
        try:
            result = subprocess.run(
                ["ifstat", "-i", "eth0,wlan0", "1", "1"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {"stats": result.stdout, "status": "success"}
            
            # Fallback to netstat
            result = subprocess.run(
                ["netstat", "-i"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return {"stats": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    
    def run_full_scan(self) -> Dict[str, Any]:
        """Chạy quét mạng toàn diện"""
        self.log("Running full network scan...")
        results = {
            "timestamp": datetime.now().isoformat(),
            "scan_type": "network_scan",
            "network_info": {}
        }
        
        results["network_info"]["interfaces"] = self.get_network_interfaces()
        results["network_info"]["listening_ports"] = self.check_listening_ports()
        results["network_info"]["established_connections"] = self.check_established_connections()
        results["network_info"]["routes"] = self.get_route_info()
        results["network_info"]["interface_stats"] = self.get_interface_stats()
        
        self.scan_results = results
        self.log("Network scan completed")
        return results
