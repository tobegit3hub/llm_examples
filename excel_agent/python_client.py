#!/usr/bin/env python3

import requests
import pandas as pd
import os

def analyze_excel_via_api(file_path, question, api_url="http://localhost:5000/analyze"):
    """
    通过HTTP API分析Excel文件
    
    参数:
        file_path (str): Excel文件路径
        question (str): 分析问题
        api_url (str): 服务端API地址
    
    返回:
        pd.DataFrame: 解析后的分析结果
    """
    try:
        # 验证文件存在性
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        # 准备请求数据
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            data = {'question': question}

            # 发送POST请求
            response = requests.post(
                api_url,
                files=files,
                data=data,
                timeout=30  # 设置超时时间
            )

        # 处理HTTP错误状态码
        response.raise_for_status()

        # 解析JSON响应
        result = response.json()
        
        if 'error' in result:
            raise RuntimeError(f"服务返回错误：{result['error']}")

        # 转换为DataFrame
        df = pd.DataFrame(
            data=result['data'],
            columns=result.get('columns', [])
        )
        
        return df

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API请求失败: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"处理失败: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 配置参数
    test_file = "test_sales_data.xlsx"
    test_question = "请分析各产品类别的销售额平均值"
    server_url = "http://localhost:6001/analyze"

    try:
        # 调用客户端
        result_df = analyze_excel_via_api(test_file, test_question, server_url)
        
        # 打印结果
        print("\n分析结果：")
        print(result_df.to_string(index=False))
        
        # 可选：保存结果到CSV
        # result_df.to_csv('analysis_result.csv', index=False)
        
    except Exception as e:
        print(f"错误发生: {str(e)}")