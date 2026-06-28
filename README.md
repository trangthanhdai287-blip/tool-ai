# 🔒 tool-ai - AI Security Agent cho Kali Linux

Một AI Agent thông minh được thiết kế để thực hiện quét bảo mật toàn diện trên hệ thống Linux, tích hợp với Ollama (TinyLlama) để cung cấp các khuyến nghị bảo mật dựa trên AI.

## ✨ Tính năng chính

### 📊 Các Module Bảo Mật

1. **SecurityModule** ✅
   - Kiểm tra quyền sudo
   - Kiểm tra trạng thái tường lửa (UFW)
   - Liệt kê các cổng mở
   - Phân tích các lần đăng nhập thất bại
   - Kiểm tra mức sử dụng đĩa
   - Liệt kê các dịch vụ đang chạy

2. **LogAnalyzer** ✅
   - Phân tích auth.log
   - Phân tích syslog
   - Phân tích Apache logs
   - Tìm kiếm các pattern nghi ngờ (SQL injection, brute force, etc.)
   - Tạo báo cáo tóm tắt

3. **VulnerabilityScanner** ✅
   - Kiểm tra các gói phần mềm lỗi thời
   - Kiểm tra quyền truy cập yếu trên các file quan trọng
   - Kiểm tra cấu hình SSH
   - Kiểm tra quy tắc tường lửa
   - Kiểm tra chính sách mật khẩu

4. **NetworkTools** ✅
   - Lấy thông tin giao diện mạng
   - Kiểm tra các cổng lắng nghe
   - Kiểm tra các kết nối đã thiết lập
   - Lấy thông tin định tuyến
   - Quét Nmap tích hợp
   - Kiểm tra phân giải DNS
   - Lấy thống kê giao diện mạng

5. **ReportGenerator** ✅
   - Xuất báo cáo JSON
   - Xuất báo cáo HTML
   - Xuất báo cáo Markdown
   - Xuất báo cáo CSV
   - Tạo báo cáo tóm tắt

### 🤖 AI Integration

- Tích hợp với **Ollama + TinyLlama**
- Phân tích kết quả quét bằng AI
- Cung cấp khuyến nghị bảo mật thông minh
- Chế độ tương tác (Interactive Mode)
- Xử lý các lệnh tùy chỉnh

## 📋 Yêu cầu hệ thống

- **OS**: Linux (Kali Linux, Ubuntu, Debian, etc.)
- **Python**: 3.7+
- **Ollama**: Bản mới nhất
- **Model**: TinyLlama
- **Quyền**: sudo (cho một số lệnh)
- **Công cụ**: nmap, netstat, curl, wget

## 🚀 Cài đặt nhanh

```bash
# Clone repository
git clone https://github.com/trangthanhdai287-blip/tool-ai.git
cd tool-ai

# Chạy script cài đặt
bash install.sh

# Chờ để Ollama tải model và khởi động
# (Lần đầu tiên có thể mất vài phút)
```

## 💻 Cách sử dụng

### 1. Chế độ tương tác

```bash
python3 ai_agent.py
# hoặc
ai
```

Các lệnh:
```
full-scan           - Quét bảo mật toàn diện
check-ports         - Kiểm tra các cổng mở
check-firewall      - Kiểm tra trạng thái tường lửa
check-updates       - Kiểm tra cập nhật khả dụng
analyze-logs        - Phân tích logs hệ thống
scan <target>       - Quét Nmap (vd: scan 192.168.1.1)
export              - Xuất báo cáo
help                - Hiển thị trợ giúp
exit                - Thoát chương trình
```

### 2. Dòng lệnh

```bash
# Gửi yêu cầu tới AI
python3 ai_agent.py "Hộ tôi kiểm tra bảo mật hệ thống"

# Phân tích file
python3 ai_agent.py /path/to/logfile.log

# Alias
ai "Câu hỏi của bạn"
ai-scan
```

### 3. Ví dụ

```bash
# Quét bảo mật toàn diện
python3 ai_agent.py full-scan

# Kiểm tra cổng mở
python3 ai_agent.py check-ports

# Quét Nmap
python3 ai_agent.py "scan 192.168.1.1"

# Hỏi AI
python3 ai_agent.py "Làm thế nào để cải thiện bảo mật SSH?"
```

## 📂 Cấu trúc thư mục

```
tool-ai/
├── ai_agent.py              # Main agent file
├── install.sh               # Cài đặt
├── requirements.txt         # Python dependencies
├── Modelfile_pro            # Ollama model config
├── README.md                # Tài liệu
└── modules/
    ├── __init__.py
    ├── security_module.py   # Quét bảo mật cơ bản
    ├── log_analyzer.py      # Phân tích log
    ├── vulnerability_scanner.py  # Kiểm tra lỗ hổng
    ├── network_tools.py     # Công cụ mạng
    └── report_generator.py  # Tạo báo cáo
└── reports/                 # Thư mục xuất báo cáo
```

## 🔧 Cấu hình

### Model Ollama

Mặc định: `tinyllama` (tối ưu hóa trong `Modelfile_pro`)

```bash
# Thay đổi model
sed -i 's/MODEL_NAME = "ai-pro"/MODEL_NAME = "mistral"/g' ai_agent.py
```

### Tham số

Chỉnh sửa trong `Modelfile_pro`:
- `temperature`: Độ sáng tạo (0.2 = cụ thể, 1.0 = sáng tạo)
- `top_p`: Xác suất hạt nhân
- `top_k`: Top-K sampling
- `num_ctx`: Kích thước ngữ cảnh

## 📊 Output

Báo cáo được lưu trong thư mục `./reports/`:
- `security_report_*.json` - JSON format
- `security_report_*.html` - HTML format
- `security_report_*.md` - Markdown format

## 🔐 Bảo mật

⚠️ **Lưu ý quan trọng:**
- Yêu cầu quyền sudo để một số quét
- Chỉ sử dụng trên hệ thống của chính mình hoặc có sự cho phép
- Không sử dụng cho các mục đích bất hợp pháp
- Dữ liệu quét có thể chứa thông tin nhạy cảm

## 🐛 Troubleshooting

### Ollama không khởi động

```bash
# Khởi động Ollama daemon
ollama serve
```

### Quyền từ chối

```bash
# Cho phép Ollama
sudo usermod -aG ollama $USER
```

### Model không tìm thấy

```bash
# Tải lại model
ollama pull tinyllama
ollama create ai-pro -f Modelfile_pro
```

## 📝 Ghi chú

- Lần quét đầu tiên có thể mất vài phút
- Cần kết nối internet để tải models
- TinyLlama được tối ưu hóa cho tốc độ và hiệu suất

## 🤝 Đóng góp

Cảm ơn vì quan tâm! Vui lòng:
1. Fork repository
2. Tạo branch cho tính năng của bạn
3. Commit thay đổi
4. Push đến branch
5. Mở Pull Request

## 📄 License

MIT License - Xem file LICENSE để chi tiết

## 📞 Liên hệ

- GitHub: [@trangthanhdai287-blip](https://github.com/trangthanhdai287-blip)
- Email: trangthanhdai287@gmail.com

---

**Cảnh báo pháp lý**: Tool này chỉ dành cho mục đích giáo dục và bảo mật hệ thống của chính mình. Cách sử dụng trái phép là bất hợp pháp.
