#!/bin/bash

echo "--- BẮT ĐẦU CÀI ĐẶT AI AGENT ---"

# 1. Cài đặt Python3 nếu chưa có
if ! command -v python3 &> /dev/null; then
    echo "[*] Đang cài đặt Python3..."
    sudo apt update && sudo apt install python3 python3-pip -y
else
    echo "[*] Python3 đã được cài đặt."
fi

# 2. Cài đặt Ollama nếu chưa có
if ! command -v ollama &> /dev/null; then
    echo "[*] Đang cài đặt Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "[*] Ollama đã được cài đặt."
fi

# 3. Tải model ai-pro (Giả sử bạn đã có Modelfile trên repo)
echo "[*] Đang khởi tạo AI Model..."
ollama pull tinyllama
# Tạo model nếu bạn đã có file Modelfile trong cùng thư mục
if [ -f "Modelfile_pro" ]; then
    ollama create ai-pro -f Modelfile_pro
fi

# 4. Tạo alias
echo "alias ai='python3 $(pwd)/ai_agent.py'" >> ~/.bashrc
source ~/.bashrc

echo "--- CÀI ĐẶT THÀNH CÔNG ---"
echo "Bạn có thể gõ lệnh 'ai' ngay bây giờ."

