#!/bin/bash

curl -X POST http://localhost:6001/analyze \
  -F "file=@test_sales_data.xlsx" \
  -F "question=请分析各产品类别的销售额平均值"