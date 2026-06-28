import subprocess
import sys
import os
from datetime import datetime

# Cấu hình
MODEL_NAME = "ai-vn"
LOG_FILE = "ai_agent_history.log"

def log_interaction(prompt, response):
    """Ghi lại lịch sử chat vào file log."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}]\nUSER: {prompt}\nAI: {response}\n{'-'*30}\n")

def run_ai(prompt):
    """Gửi yêu cầu tới Ollama và nhận kết quả."""
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Lỗi hệ thống: {str(e)}"

def main():
    if len(sys.argv) > 1:
        # Lấy tham số đầu vào và đóng ngoặc đầy đủ
        input_data = " ".join(sys.argv[1:])
        
        if os.path.isfile(input_data):
            with open(input_data, 'r', encoding='utf-8') as f:
                content = f.read()
            prompt = f"Hãy phân tích nội dung sau: \n{content}"
        else:
            prompt = input_data
            
        print(f"[*] Đang gửi yêu cầu tới {MODEL_NAME}...")
        response = run_ai(prompt)
        
        print("\n--- PHẢN HỒI ---")
        print(response)
        
        log_interaction(prompt, response)
        print(f"\n[*] Đã lưu log vào {LOG_FILE}")
    else:
        print("Sử dụng: python3 ai_agent.py 'Câu hỏi' hoặc 'đường_dẫn_file'")

if __name__ == "__main__":
    main()
