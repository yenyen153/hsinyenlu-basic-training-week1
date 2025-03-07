# 使用 Python 3.11 作為基底映像
FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 複製 `requirements.txt` 先安裝依賴
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有檔案到容器內
COPY . .

# 確保 `uvicorn` 可以執行
RUN pip install uvicorn

# 暴露 FastAPI 端口
EXPOSE 8000

# 預設啟動 FastAPI
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 補充安裝uvicorn
# 補充把windows上的mriadb移到mac