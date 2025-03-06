import os
import pandas as pd
import openai
from openai import OpenAI

def excel_analysis_with_ai(excel_path, user_question):
    """
    通过OpenAI API分析Excel文件并返回DataFrame格式结果
    
    参数:
        excel_path (str): Excel文件路径
        user_question (str): 用户分析问题
    
    返回:
        pd.DataFrame: 分析结果DataFrame
    """
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        raise ValueError(f"读取Excel文件失败: {str(e)}")

    # 构建数据预览
    data_preview = f"""
    数据概览：
    - 共 {len(df)} 行 {len(df.columns)} 列
    - 列名：{', '.join(df.columns)}
    - 前3行样例：
    {df.head(3).to_string(index=False)}
    """

    # 构建系统提示词
    system_prompt = """你是一个专业数据分析助手。请根据提供的Excel数据结构和用户问题进行数据分析，
    并严格遵循以下要求：
    1. 结果必须使用CSV格式返回
    2. 第一行为列标题
    3. 只返回数据表格，不要包含额外解释
    4. 确保数值精度
    5. 如果需要进行计算，保留2位小数
    示例：
    Category,Average_Value
    A,123.45
    B,678.90
    """

    # 构造完整prompt
    full_prompt = f"{data_preview}\n用户问题：{user_question}"

    # 初始化OpenAI客户端
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 调用ChatGPT API
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.1,
            timeout=600
        )
    except Exception as e:
        raise ConnectionError(f"API请求失败: {str(e)}")

    # 解析结果
    result_content = response.choices[0].message.content.strip()
    
    # 清洗数据并转换为DataFrame
    try:
        # 移除可能的代码块标记
        cleaned_content = result_content.replace("```csv", "").replace("```", "")
        # 使用StringIO读取CSV数据
        from io import StringIO
        result_df = pd.read_csv(StringIO(cleaned_content))
    except Exception as e:
        raise ValueError(f"结果解析失败: {str(e)}\n原始返回内容：{result_content}")

    return result_df

# 使用示例
if __name__ == "__main__":
    # 设置环境变量（或在代码中直接设置）
    # os.environ["OPENAI_API_KEY"] = "your-api-key"
    
    excel_path = "./test_sales_data.xlsx"
    question = "请分析各产品类别的销售额平均值"
    
    try:
        result = excel_analysis_with_ai(excel_path, question)
        print("分析结果：")
        print(result)
    except Exception as e:
        print(f"处理失败: {str(e)}")
