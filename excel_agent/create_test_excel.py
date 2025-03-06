import pandas as pd

test_data = {
    "产品类别": ["电子产品", "电子产品", "电子产品", 
             "家居用品", "家居用品", "服装", 
             "服装", "服装", "服装"],
    "销售额（元）": [1000, 1500, 2000, 
                800, 1200, 500, 
                600, 700, 600]
}

df = pd.DataFrame(test_data)
df.to_excel("test_sales_data.xlsx", index=False, engine='openpyxl')
