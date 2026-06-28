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

# 3. Tải model Phi 3.5 và tạo model ai-vn
echo "[*] Đang khởi tạo AI Model..."
ollama pull phi3.5

# Xóa model ai-vn cũ (nếu có) để cập nhật mới
ollama rm ai-vn 2>/dev/null

# Tạo model ai-vn từ Phi 3.5 thông qua Modelfile_pro
if [ -f "Modelfile_pro" ]; then
    echo "[*] Đang build model ai-vn từ Modelfile_pro..."
    ollama create ai-vn -f Modelfile_pro
    echo "[+] Model ai-vn đã sẵn sàng!"
else
    echo "[!] Lỗi: File Modelfile_pro không tìm thấy!"
    exit 1
fi

# 4. Tạo alias
echo "[*] Đang cấu hình lệnh 'ai'..."
echo "alias ai='ollama run ai-vn'" >> ~/.bashrc
source ~/.bashrc

echo "--- CÀI ĐẶT THÀNH CÔNG ---"
echo "Bạn có thể gõ lệnh 'ai' ngay bây giờ để bắt đầu chat."
echo "Ngoài ra, dùng: python3 ai_agent.py 'câu hỏi' hoặc python3 ai_agent.py 'đường_dẫn_file'"
