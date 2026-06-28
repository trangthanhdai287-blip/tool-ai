"""LogAnalyzer - Phân tích log hệ thống"""

import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import Counter

class LogAnalyzer:
    """Module phân tích log hệ thống"""
    
    def __init__(self, log_dir: str = "/var/log"):
        self.log_dir = log_dir
        self.analysis_results = {}
    
    def read_log_file(self, filepath: str, lines: int = 1000) -> List[str]:
        """Đọc file log"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.readlines()
                return content[-lines:]
        except Exception as e:
            print(f"[LogAnalyzer] Error reading {filepath}: {str(e)}")
            return []
    
    def analyze_auth_logs(self) -> Dict[str, Any]:
        """Phân tích log xác thực"""
        print("[LogAnalyzer] Analyzing auth logs...")
        auth_log = "/var/log/auth.log"
        
        if not os.path.exists(auth_log):
            return {"error": "auth.log not found"}
        
        logs = self.read_log_file(auth_log, 5000)
        
        failed_logins = [l for l in logs if "Failed password" in l]
        successful_logins = [l for l in logs if "Accepted" in l]
        sudo_usage = [l for l in logs if "sudo" in l]
        
        return {
            "total_lines": len(logs),
            "failed_logins": len(failed_logins),
            "successful_logins": len(successful_logins),
            "sudo_commands": len(sudo_usage),
            "recent_failed": failed_logins[-5:] if failed_logins else [],
            "recent_successful": successful_logins[-5:] if successful_logins else []
        }
    
    def analyze_syslog(self) -> Dict[str, Any]:
        """Phân tích syslog"""
        print("[LogAnalyzer] Analyzing syslog...")
        syslog = "/var/log/syslog"
        
        if not os.path.exists(syslog):
            return {"error": "syslog not found"}
        
        logs = self.read_log_file(syslog, 5000)
        
        errors = [l for l in logs if "error" in l.lower()]
        warnings = [l for l in logs if "warning" in l.lower()]
        critical = [l for l in logs if "critical" in l.lower()]
        
        # Extract process names
        processes = []
        for log in logs:
            match = re.search(r'\[(\w+)\]', log)
            if match:
                processes.append(match.group(1))
        
        process_counts = Counter(processes)
        
        return {
            "total_lines": len(logs),
            "errors": len(errors),
            "warnings": len(warnings),
            "critical": len(critical),
            "top_processes": dict(process_counts.most_common(10)),
            "recent_errors": errors[-5:] if errors else [],
            "recent_critical": critical[-5:] if critical else []
        }
    
    def analyze_apache_logs(self) -> Dict[str, Any]:
        """Phân tích Apache logs (nếu có)"""
        print("[LogAnalyzer] Analyzing Apache logs...")
        apache_log = "/var/log/apache2/access.log"
        
        if not os.path.exists(apache_log):
            return {"error": "Apache logs not found"}
        
        logs = self.read_log_file(apache_log, 5000)
        
        # Phân tích HTTP status codes
        status_codes = []
        ips = []
        
        for log in logs:
            # Extract status code
            match = re.search(r'\" (\d{3}) ', log)
            if match:
                status_codes.append(match.group(1))
            
            # Extract IP
            match = re.search(r'^([\d\.]+) ', log)
            if match:
                ips.append(match.group(1))
        
        status_count = Counter(status_codes)
        ip_count = Counter(ips)
        
        return {
            "total_requests": len(logs),
            "status_codes": dict(status_count),
            "top_ips": dict(ip_count.most_common(10)),
            "errors_4xx": sum(1 for code in status_codes if code.startswith('4')),
            "errors_5xx": sum(1 for code in status_codes if code.startswith('5'))
        }
    
    def find_suspicious_patterns(self, log_file: str) -> Dict[str, List[str]]:
        """Tìm các pattern nghi ngờ trong log"""
        print(f"[LogAnalyzer] Analyzing suspicious patterns in {log_file}...")
        
        logs = self.read_log_file(log_file)
        
        patterns = {
            "sql_injection": [l for l in logs if any(x in l.lower() for x in ["union", "select", "drop", "insert"])],
            "brute_force": [l for l in logs if "Failed" in l or "denied" in l.lower()],
            "file_traversal": [l for l in logs if "../" in l or "..\\" in l],
            "command_injection": [l for l in logs if any(x in l for x in [";", "|", "&", "$("])]
        }
        
        return {k: v[:10] for k, v in patterns.items()}
    
    def generate_summary(self) -> Dict[str, Any]:
        """Tạo báo cáo tóm tắt"""
        print("[LogAnalyzer] Generating summary...")
        summary = {
            "timestamp": datetime.now().isoformat(),
            "analysis": {}
        }
        
        summary["analysis"]["auth"] = self.analyze_auth_logs()
        summary["analysis"]["syslog"] = self.analyze_syslog()
        summary["analysis"]["apache"] = self.analyze_apache_logs()
        
        self.analysis_results = summary
        return summary
