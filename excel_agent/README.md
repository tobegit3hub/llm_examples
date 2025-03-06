# Excel Agent

## Installation

```
pip install -r ./requirements.txt
```

## Local Mode

```
python ./excel_agent.py
```

## HTTP Mode

Start the web server.


```
python ./http_server.py
```

Use the clients.

```
curl -X POST http://localhost:6001/analyze \
  -F "file=@test_sales_data.xlsx" \
  -F "question=请分析各产品类别的销售额平均值"
```

Or use python client.

```
python3 ./python_client.py
```