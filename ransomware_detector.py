import re

def detect_malicious_crypto(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        # Tìm các thư viện và hàm thường dùng trong ransomware
        if "cryptography.fernet" in content and "encrypt" in content:
            return True, "Cảnh báo: Phát hiện logic mã hóa Ransomware!"
    return False, "An toàn"
