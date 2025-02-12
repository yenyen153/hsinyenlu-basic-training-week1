# %%
## 虛擬環境操作 - 如何確認當前虛擬環境
## 查看目的 : 確保套件安裝在正確的環境中，並確保開發者之間環境一致

# 方法1. 程式執行
import sys

print(sys.executable)

# 方法2. terminal執行
## python --version

# %%
## 虛擬環境操作 - requirements.txt的意義為何，如何建立與使⽤
## requirements.txt是為了使開發者的環境都達到統一，避免version不同導致差異

## 如何建立requirements.txt
# 1. 可以自己手動新增requirements.txt，寫入所需套件與版本
# 2. 如果已經有專案了，可以在terminal中自動生成，輸入pip freeze > requirements.txt(這個方法也可以使用在已經有requirements.txt的情況下，一邊開發一邊新增使用套件)

## 如何讀取requirements.txt
## 在terminal中讀取並安裝 : pip install -r requirements.txt