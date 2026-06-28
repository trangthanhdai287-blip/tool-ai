#!/bin/bash

echo "--- BẮT ĐẦU CÀI ĐẶT AI SECURITY AGENT ---"

# 1. Cài đặt Python3 nếu chưa có
if ! command -v python3 &> /dev/null; then
    echo "[*] Đang cài đặt Python3..."
    sudo apt update && sudo apt install python3 python3-pip -y
else
    echo "[✓] Python3 đã được cài đặt."
fi

# 2. Cài đặt Ollama nếu chưa có
if ! command -v ollama &> /dev/null; then
    echo "[*] Đang cài đặt Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "[✓] Ollama đã được cài đặt."
fi

# 3. Cài đặt các công cụ bảo mật cần thiết
echo "[*] Đang cài đặt các công cụ bảo mật..."
sudo apt install -y \
    nmap \
    netstat \
    net-tools \
    curl \
    wget \
    git

echo "[✓] Các công cụ bảo mật đã được cài đặt."

# 4. Cài đặt dependencies Python
echo "[*] Đang cài đặt dependencies Python..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    echo "[!] Cảnh báo: requirements.txt không tìm thấy"
fi

# 5. Tải model Ollama
echo "[*] Đang tải model tinyllama..."
ollama pull tinyllama

# 6. Tạo model ai-pro từ Modelfile
echo "[*] Đang tạo model ai-pro..."
if [ -f "Modelfile_pro" ]; then
    ollama create ai-pro -f Modelfile_pro
    echo "[✓] Model ai-pro đã được tạo thành công."
else
    echo "[!] Cảnh báo: Modelfile_pro không tìm thấy"
    echo "[*] Sử dụng model tinyllama mặc định..."
fi

# 7. Tạo thư mục reports
mkdir -p ./reports
echo "[✓] Thư mục reports đã được tạo."

# 8. Tạo alias
echo "[*] Tạo alias 'ai' cho lệnh..."
echo "alias ai='python3 $(pwd)/ai_agent.py'" >> ~/.bashrc
echo "alias ai-scan='python3 $(pwd)/ai_agent.py full-scan'" >> ~/.bashrc
source ~/.bashrc

echo ""
echo "--- CÀI ĐẶT THÀNH CÔNG ---"
echo "✓ Các lệnh có sẵn:"
echo "  - ai 'Câu hỏi'                   # Gửi yêu cầu tới AI"
echo "  - ai                              # Chế độ tương tác"
echo "  - ai-scan                         # Quét bảo mật toàn diện"
echo "  - python3 ai_agent.py full-scan  # Quét và xuất báo cáo"
echo ""
echo "✓ Bạn có thể bắt đầu sử dụng ngay bây giờ!"
echo "✓ Bản báo cáo sẽ được lưu trong thư mục ./reports/"
echo ""
echo "Tài liệu: https://github.com/trangthanhdai287-blip/tool-ai"
echo ""
