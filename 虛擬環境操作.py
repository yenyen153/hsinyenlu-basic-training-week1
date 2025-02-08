# %%
## 虛擬環境操作 - 如何確認當前虛擬環境
## 查看目的 : 確保套件安裝在正確的環境中，並確保開發者之間環境一致

# 方法1. 程式執行
import sys

print(sys.executable)

# 方法2. terminal執行
## python --version