from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Cho phép web Vercel gọi API này

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get("prompt")
    mode = data.get("mode") # 'local' hoặc 'cloud'

    if mode == 'local':
        # Gọi mô hình Ollama
        result = subprocess.run(['ollama', 'run', 'ai-vn', query], capture_output=True, text=True)
        return jsonify({"answer": result.stdout})
    else:
        # Gọi Gemini Flash 3.5
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query)
        return jsonify({"answer": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
