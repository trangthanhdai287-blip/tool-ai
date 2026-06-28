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

def run_ai(prompt, ai_name=None):
    """Gửi yêu cầu tới Ollama và nhận kết quả.
    
    Args:
        prompt (str): Câu hỏi/yêu cầu gửi tới model
        ai_name (str): Tên model Ollama (mặc định: MODEL_NAME)
    
    Returns:
        str: Kết quả trả về từ model
    """
    model = ai_name if ai_name else MODEL_NAME
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
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
        # Lấy tham số đầu vào
        input_data = " ".join(sys.argv[1:])
        
        # Kiểm tra nếu có flag --model để chỉ định tên model
        ai_name = None
        if "--model" in sys.argv:
            idx = sys.argv.index("--model")
            if idx + 1 < len(sys.argv):
                ai_name = sys.argv[idx + 1]
                # Loại bỏ flag --model và tên model từ input_data
                input_data = " ".join([arg for i, arg in enumerate(sys.argv[1:]) 
                                      if i < idx - 1 or i > idx])
        
        if os.path.isfile(input_data):
            with open(input_data, 'r', encoding='utf-8') as f:
                content = f.read()
            prompt = f"Hãy phân tích nội dung sau: \n{content}"
        else:
            prompt = input_data
            
        model_display = ai_name if ai_name else MODEL_NAME
        print(f"[*] Đang gửi yêu cầu tới {model_display}...")
        response = run_ai(prompt, ai_name)
        
        print("\n--- PHẢN HỒI ---")
        print(response)
        
        log_interaction(prompt, response)
        print(f"\n[*] Đã lưu log vào {LOG_FILE}")
    else:
        print("Sử dụng: python3 ai_agent.py 'Câu hỏi' hoặc 'đường_dẫn_file'")
        print("Hoặc:    python3 ai_agent.py --model model_name 'Câu hỏi'")

if __name__ == "__main__":
    main()
