# %%
## 設定環境變數的方法與原因

## 設定環境變數原因:
## 當主程式需用到密碼或API金鑰時，可將這些訊息存放在環境變數中，優點是可以使專案在不同電腦中，都能透過讀取統一的環境變數來操作
## 另外在專案開發時，常會使用DEBUG模式，但正式發布時須將DEBUG關閉，可將DEBUG設為環境變數之一，使專案更好控制DEBUG開關

## 以下為例
import os

api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")

print(f"API Key: {api_key}")
print(f"Debug Mode: {debug_mode}")

## IDE模式
## 1. 點選右上角專案名稱
## 2. 找到Edit Configurations
## 3. 找到 Environment Variables
## 4. 即可進入編輯環境變數

## python-dotenv模式
## 1. 先安裝pip install python-dotenv
## 2. 建立.env檔案，輸入api key、debug模式等資訊
## 3. 另外引用from dotenv import load_dotenv
## 4. 利用load_dotenv()讀取.env檔中的資訊 (如果.env在其他資料夾中，可以去指定讀檔路徑)