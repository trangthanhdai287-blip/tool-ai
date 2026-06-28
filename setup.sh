#!/bin/bash

# Kiểm tra nếu chưa có venv thì tạo
if [ ! -d "venv" ]; then
    echo "[*] Tạo môi trường ảo..."
    python3 -m venv venv
fi

# Kích hoạt venv và cài đặt thư viện
echo "[*] Cài đặt thư viện..."
source venv/bin/activate
pip install -r requirements.txt

# Kiểm tra Ollama và tạo model
if command -v ollama &> /dev/null; then
    echo "[*] Đang build model ai-vn (TinyLlama)..."
    ollama pull tinyllama
    ollama rm ai-vn 2>/dev/null
    ollama create ai-vn -f Modelfile_pro
    echo "[+] Model đã sẵn sàng!"
else
    echo "[!] Lỗi: Bạn chưa cài đặt Ollama. Hãy cài tại https://ollama.com"
    exit 1
fi

echo "[SUCCESS] Cài đặt hoàn tất! Chạy bằng lệnh: source venv/bin/activate && python3 ai_agent.py"
