"""Main AI Agent - Tích hợp tất cả modules bảo mật"""

import subprocess
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Import modules
sys.path.insert(0, os.path.dirname(__file__))
from modules import (
    SecurityModule,
    LogAnalyzer,
    VulnerabilityScanner,
    NetworkTools,
    ReportGenerator
)

# Cấu hình
MODEL_NAME = "ai-pro"
LOG_FILE = "ai_agent_history.log"
REPORT_DIR = "./reports"

class SecurityAIAgent:
    """AI Agent cho phân tích bảo mật hệ thống"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.security_module = SecurityModule(verbose=verbose)
        self.log_analyzer = LogAnalyzer()
        self.vulnerability_scanner = VulnerabilityScanner(verbose=verbose)
        self.network_tools = NetworkTools(verbose=verbose)
        self.report_generator = ReportGenerator(output_dir=REPORT_DIR)
        self.all_results = {}
    
    def log(self, message: str):
        """Ghi log thông báo"""
        if self.verbose:
            print(f"[AI Agent] {message}")
    
    def log_interaction(self, prompt: str, response: str):
        """Ghi lại lịch sử chat vào file log"""
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}]\nUSER: {prompt}\nAI: {response}\n{'-'*50}\n")
    
    def run_ai(self, prompt: str) -> str:
        """Gửi yêu cầu tới Ollama và nhận kết quả"""
        try:
            result = subprocess.run(
                ["ollama", "run", MODEL_NAME, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=120
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "Lỗi: Yêu cầu vượt quá thời gian chờ (timeout)"
        except Exception as e:
            return f"Lỗi hệ thống: {str(e)}"
    
    def perform_security_scan(self) -> Dict[str, Any]:
        """Thực hiện quét bảo mật toàn diện"""
        self.log("Performing comprehensive security scan...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "scan_type": "full_security_scan",
            "modules": {}
        }
        
        # Run security module
        self.log("[1/5] Running security checks...")
        results["modules"]["security_checks"] = self.security_module.run_full_scan()
        
        # Run log analyzer
        self.log("[2/5] Analyzing logs...")
        results["modules"]["log_analysis"] = self.log_analyzer.generate_summary()
        
        # Run vulnerability scanner
        self.log("[3/5] Scanning vulnerabilities...")
        results["modules"]["vulnerability_scan"] = self.vulnerability_scanner.run_full_scan()
        
        # Run network tools
        self.log("[4/5] Analyzing network...")
        results["modules"]["network_analysis"] = self.network_tools.run_full_scan()
        
        # Generate summary
        self.log("[5/5] Generating summary report...")
        results["summary"] = self.report_generator.generate_summary_report(results["modules"])
        
        self.all_results = results
        return results
    
    def analyze_with_ai(self, scan_results: Dict[str, Any]) -> str:
        """Phân tích kết quả quét với AI"""
        self.log("Analyzing results with AI...")
        
        # Tạo prompt cho AI
        prompt = f"""Hãy phân tích kết quả quét bảo mật sau đây và cung cấp:
1. Tóm tắt về tình trạng bảo mật
2. Các vấn đề quan trọng cần xử lý ngay lập tức
3. Các khuyến nghị để cải thiện bảo mật
4. Đánh giá mức độ rủi ro chung (Low/Medium/High/Critical)

Kết quả quét:
{json.dumps(scan_results, indent=2, ensure_ascii=False)}

Vui lòng cung cấp phân tích chi tiết và khuyến nghị cụ thể."""
        
        response = self.run_ai(prompt)
        return response
    
    def handle_custom_command(self, command: str) -> str:
        """Xử lý các lệnh tùy chỉnh"""
        self.log(f"Processing custom command: {command}")
        
        if command.startswith("scan "):
            target = command.replace("scan ", "").strip()
            if target:
                self.log(f"Running nmap scan on {target}...")
                result = self.network_tools.nmap_scan(target)
                return json.dumps(result, indent=2, ensure_ascii=False)
        
        elif command == "check-ports":
            return json.dumps(self.network_tools.check_listening_ports(), indent=2, ensure_ascii=False)
        
        elif command == "check-firewall":
            return json.dumps(self.security_module.check_firewall_status(), indent=2, ensure_ascii=False)
        
        elif command == "check-updates":
            return json.dumps(self.vulnerability_scanner.check_outdated_packages(), indent=2, ensure_ascii=False)
        
        elif command == "analyze-logs":
            return json.dumps(self.log_analyzer.generate_summary(), indent=2, ensure_ascii=False)
        
        elif command == "full-scan":
            results = self.perform_security_scan()
            return json.dumps(results["summary"], indent=2, ensure_ascii=False)
        
        else:
            # Truyền lệnh cho AI để xử lý
            return self.run_ai(command)
    
    def export_report(self, report_format: str = "all") -> list:
        """Xuất báo cáo"""
        self.log(f"Exporting report in {report_format} format...")
        
        if report_format == "all":
            files = self.report_generator.export_all_formats(
                self.all_results,
                f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
        elif report_format == "json":
            files = [self.report_generator.generate_json_report(
                self.all_results,
                f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )]
        elif report_format == "html":
            files = [self.report_generator.generate_html_report(
                self.all_results,
                f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )]
        else:
            files = []
        
        return files
    
    def interactive_mode(self):
        """Chế độ tương tác"""
        print("\n" + "="*60)
        print("🔒 AI Security Agent - Interactive Mode")
        print("="*60)
        print("Lệnh có sẵn:")
        print("  full-scan           - Quét bảo mật toàn diện")
        print("  check-ports         - Kiểm tra các cổng mở")
        print("  check-firewall      - Kiểm tra trạng thái tường lửa")
        print("  check-updates       - Kiểm tra cập nhật khả dụng")
        print("  analyze-logs        - Phân tích logs hệ thống")
        print("  scan <target>       - Quét nmap (vd: scan 192.168.1.1)")
        print("  export              - Xuất báo cáo")
        print("  help                - Hiển thị trợ giúp")
        print("  exit                - Thoát chương trình")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("\n[AI Agent] >>> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("[*] Đang thoát chương trình...")
                    break
                
                if user_input.lower() == "help":
                    print("Nhập bất kỳ câu hỏi nào về bảo mật hoặc sử dụng các lệnh có sẵn.")
                    continue
                
                if user_input.lower() == "export":
                    if self.all_results:
                        files = self.export_report("all")
                        print(f"\n✅ Báo cáo được xuất vào:")
                        for f in files:
                            print(f"   - {f}")
                    else:
                        print("❌ Chưa có kết quả quét. Vui lòng chạy full-scan trước.")
                    continue
                
                # Xử lý các lệnh tùy chỉnh hoặc gửi cho AI
                response = self.handle_custom_command(user_input)
                
                print(f"\n--- PHẢN HỒI ---")
                print(response)
                
                self.log_interaction(user_input, response)
                
            except KeyboardInterrupt:
                print("\n[*] Bị gián đoạn bởi người dùng")
                break
            except Exception as e:
                print(f"❌ Lỗi: {str(e)}")

def main():
    """Hàm chính"""
    agent = SecurityAIAgent(verbose=True)
    
    if len(sys.argv) > 1:
        # Chế độ dòng lệnh
        input_data = " ".join(sys.argv[1:])
        
        if os.path.isfile(input_data):
            with open(input_data, 'r', encoding='utf-8') as f:
                content = f.read()
            prompt = f"Hãy phân tích nội dung sau:\n{content}"
        else:
            prompt = input_data
        
        print(f"[*] Đang gửi yêu cầu tới {MODEL_NAME}...")
        response = agent.run_ai(prompt)
        
        print("\n--- PHẢN HỒI ---")
        print(response)
        
        agent.log_interaction(prompt, response)
        print(f"\n[*] Đã lưu log vào {LOG_FILE}")
    else:
        # Chế độ tương tác
        agent.interactive_mode()

if __name__ == "__main__":
    main()
