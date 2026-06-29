#!/bin/bash

echo "--- BẮT ĐẦU CÀI ĐẶT AI AGENT (Qwen2.5) ---"

# 1. Cài đặt Python3
if ! command -v python3 &> /dev/null; then
    echo "[*] Đang cài đặt Python3..."
    sudo apt update && sudo apt install python3 python3-pip -y
else
    echo "[*] Python3 đã được cài đặt."
fi

# 2. Cài đặt Ollama
if ! command -v ollama &> /dev/null; then
    echo "[*] Đang cài đặt Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "[*] Ollama đã được cài đặt."
fi

# 3. Tải model Qwen2.5 và tạo model ai-vn
echo "[*] Đang khởi tạo AI Model (Qwen2.5:3b)..."
ollama pull qwen2.5:3b

# Xóa model ai-vn cũ
ollama rm ai-vn 2>/dev/null

# Tạo model ai-vn
if [ -f "Modelfile_pro" ]; then
    echo "[*] Đang build model ai-vn từ Modelfile_pro..."
    ollama create ai-vn -f Modelfile_pro
    echo "[+] Model ai-vn đã sẵn sàng!"
else
    echo "[!] Lỗi: File Modelfile_pro không tìm thấy!"
    exit 1
fi

# 4. Tạo alias (Tránh ghi đè trùng lặp nếu đã có)
if ! grep -q "alias ai=" ~/.bashrc; then
    echo "alias ai='ollama run ai-vn'" >> ~/.bashrc
    source ~/.bashrc
    echo "[+] Đã cấu hình lệnh 'ai'."
else
    echo "[*] Alias 'ai' đã tồn tại."
fi

echo "--- CÀI ĐẶT THÀNH CÔNG ---"
