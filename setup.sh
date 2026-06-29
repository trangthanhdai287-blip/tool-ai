#!/bin/bash

# 1. Kiểm tra nếu chưa có venv thì tạo
if [ ! -d "venv" ]; then
    echo "[*] Tạo môi trường ảo..."
    python3 -m venv venv
fi

# 2. Kích hoạt venv và cài đặt thư viện
echo "[*] Cài đặt thư viện..."
source venv/bin/activate
pip install -r requirements.txt

# 3. Kiểm tra Ollama và tạo model
if command -v ollama &> /dev/null; then
    echo "[*] Đang download model qwen2.5:3b..."
    ollama pull qwen2.5:3b
    
    # Xóa model ai-vn cũ (nếu có) để cập nhật mới
    ollama rm ai-vn 2>/dev/null
    
    echo "[*] Đang build model ai-vn từ qwen2.5:3b..."
    ollama create ai-vn -f Modelfile_pro
    echo "[+] Model ai-vn đã sẵn sàng!"
else
    echo "[!] Lỗi: Bạn chưa cài đặt Ollama. Hãy cài tại https://ollama.com"
    exit 1
fi

# 4. Tự động cấu hình Alias 'ai' vào ~/.zshrc
echo "[*] Đang cấu hình lệnh 'ai'..."
if ! grep -q "alias ai=" ~/.zshrc; then
    echo "alias ai='ollama run ai-vn'" >> ~/.zshrc
    echo "[+] Đã thêm lệnh 'ai' vào ~/.zshrc"
else
    echo "[!] Lệnh 'ai' đã tồn tại trong ~/.zshrc, bỏ qua."
fi

# 5. Áp dụng thay đổi
source ~/.zshrc


echo "--------------------------------------------------------"
echo "[SUCCESS] Cài đặt hoàn tất!"
echo "- Để chat với AI (qwen2.5:3b): Gõ lệnh 'ai'"
echo "- Để chạy project: 'source venv/bin/activate' và 'python3 ai_agent.py'"
echo "--------------------------------------------------------"
