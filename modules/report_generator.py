"""ReportGenerator - Xuất báo cáo bảo mật"""

import json
import csv
from datetime import datetime
from typing import Dict, Any, List
import os

class ReportGenerator:
    """Module tạo báo cáo bảo mật"""
    
    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.reports = []
    
    def log(self, message: str):
        print(f"[ReportGenerator] {message}")
    
    def generate_json_report(self, data: Dict[str, Any], report_name: str = None) -> str:
        """Tạo báo cáo JSON"""
        self.log("Generating JSON report...")
        
        if not report_name:
            report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.output_dir, f"{report_name}.json")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.log(f"JSON report saved: {filepath}")
            self.reports.append(filepath)
            return filepath
        except Exception as e:
            self.log(f"Error generating JSON report: {str(e)}")
            return None
    
    def generate_csv_report(self, data: List[Dict[str, Any]], report_name: str = None) -> str:
        """Tạo báo cáo CSV"""
        self.log("Generating CSV report...")
        
        if not report_name:
            report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.output_dir, f"{report_name}.csv")
        
        try:
            if not data:
                self.log("No data to generate CSV report")
                return None
            
            keys = data[0].keys()
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            
            self.log(f"CSV report saved: {filepath}")
            self.reports.append(filepath)
            return filepath
        except Exception as e:
            self.log(f"Error generating CSV report: {str(e)}")
            return None
    
    def generate_html_report(self, data: Dict[str, Any], report_name: str = None) -> str:
        """Tạo báo cáo HTML"""
        self.log("Generating HTML report...")
        
        if not report_name:
            report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.output_dir, f"{report_name}.html")
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Security Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #555;
                    margin-top: 30px;
                }}
                .timestamp {{
                    color: #999;
                    font-size: 12px;
                }}
                .high {{
                    color: #dc3545;
                    font-weight: bold;
                }}
                .medium {{
                    color: #ffc107;
                    font-weight: bold;
                }}
                .low {{
                    color: #28a745;
                    font-weight: bold;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #007bff;
                    color: white;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔒 Security Report</h1>
                <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
            </div>
        </body>
        </html>
        """
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.log(f"HTML report saved: {filepath}")
            self.reports.append(filepath)
            return filepath
        except Exception as e:
            self.log(f"Error generating HTML report: {str(e)}")
            return None
    
    def generate_markdown_report(self, data: Dict[str, Any], report_name: str = None) -> str:
        """Tạo báo cáo Markdown"""
        self.log("Generating Markdown report...")
        
        if not report_name:
            report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.output_dir, f"{report_name}.md")
        
        md_content = f"""# 🔒 Security Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

```json
{json.dumps(data, indent=2, ensure_ascii=False)}
```

---

*Report generated by AI Security Agent*
        """
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            self.log(f"Markdown report saved: {filepath}")
            self.reports.append(filepath)
            return filepath
        except Exception as e:
            self.log(f"Error generating Markdown report: {str(e)}")
            return None
    
    def generate_summary_report(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo báo cáo tóm tắt từ kết quả quét"""
        self.log("Generating summary report...")
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_vulnerabilities": 0,
            "critical_issues": 0,
            "high_issues": 0,
            "medium_issues": 0,
            "low_issues": 0,
            "details": scan_results
        }
        
        # Count vulnerabilities by severity
        def count_by_severity(obj):
            if isinstance(obj, dict):
                for value in obj.values():
                    if isinstance(value, dict):
                        if "severity" in value:
                            severity = value["severity"]
                            if severity == "critical":
                                summary["critical_issues"] += 1
                            elif severity == "high":
                                summary["high_issues"] += 1
                            elif severity == "medium":
                                summary["medium_issues"] += 1
                            elif severity == "low":
                                summary["low_issues"] += 1
                            summary["total_vulnerabilities"] += 1
                        if "vulnerabilities" in value and isinstance(value["vulnerabilities"], list):
                            for vuln in value["vulnerabilities"]:
                                summary["total_vulnerabilities"] += 1
                        elif isinstance(value, dict):
                            count_by_severity(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                count_by_severity(item)
        
        count_by_severity(scan_results)
        return summary
    
    def export_all_formats(self, data: Dict[str, Any], report_name: str = None) -> List[str]:
        """Xuất báo cáo theo tất cả định dạng"""
        self.log("Exporting report in all formats...")
        
        if not report_name:
            report_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        files = []
        files.append(self.generate_json_report(data, report_name))
        files.append(self.generate_html_report(data, report_name))
        files.append(self.generate_markdown_report(data, report_name))
        
        return [f for f in files if f]
    
    def list_reports(self) -> List[str]:
        """Liệt kê tất cả các báo cáo đã tạo"""
        return self.reports
