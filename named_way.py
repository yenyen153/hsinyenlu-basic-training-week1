# %%
## 命名規則
## 命名規則的產生，是為了讓開發者都能有統一的命名方式，互相能快速了解變數、函式等功用

# Package : 全小寫，避免 _ 、 特殊符號 --> tools
# Module : 全小寫，可用 _ 分隔，避免和標準庫名稱重複 --> tool.py
## Package & Module參考project資料夾展示 (至於Package & Module branch中)

## 可以參考branch:Package&Module的檔案

# Class : PascalCase，像駝峰一樣，有高低大小寫，每個單字首字母大寫，不要使用_ --> AccountManager
class AccountManger:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.balance = 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError('must be positive')
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            raise RuntimeError('balance not enough')


acct1 = AccountManger('123-456-789', 'Justin')
acct1.deposit(100)
acct1.withdraw(30)
print(acct1.balance)