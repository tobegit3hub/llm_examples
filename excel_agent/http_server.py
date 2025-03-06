import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

from excel_agent import excel_analysis_with_ai  # 替换为实际模块名

app = Flask(__name__)
CORS(app)  # 允许跨域请求

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze_excel():
    # 检查文件上传
    if 'file' not in request.files:
        return jsonify({"error": "未上传文件"}), 400
        
    file = request.files['file']
    question = request.form.get('question', '')

    # 验证参数
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "仅支持Excel文件（.xlsx/.xls）"}), 400
    if not question:
        return jsonify({"error": "问题参数不能为空"}), 400

    # 保存临时文件
    temp_path = None
    try:
        _, temp_path = tempfile.mkstemp(suffix='.xlsx', dir=UPLOAD_FOLDER)
        file.save(temp_path)
        
        # 调用分析函数
        result_df = excel_analysis_with_ai(temp_path, question)
        
        # 转换结果
        return jsonify({
            "data": result_df.to_dict(orient='records'),
            "columns": list(result_df.columns)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    finally:
        # 清理临时文件
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)
