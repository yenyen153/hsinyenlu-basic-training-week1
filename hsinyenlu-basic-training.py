# 1. pycharm部分
#%%
## 程式執行方式 - 一般執行

# 1. 點擊pycharm介面右上run<檔名>執行
# 2. 點擊右鍵，選擇run<檔名>執行
# 3. shift + crtl + f10 (有些是shift + f10)
# 另外，使用#%%可分段執行程式，優點在於，需要單看某一部分程式的產出或效果，可以單一執行，避免整份檔案執行

#%%
## 程式執行方式 - 偵錯模式breakpoints

## 有兩種breakpoints : line breakpoints、exception breakpoints
# line breakpoints : 設定在程式碼前的結束點，當程式執行的時候，會依line breakpoints當作程式結束點
# exception breakpoints : 程式有時會有一些錯誤產生，exception breakpoints就是當錯誤發生時會出現的，告知開發者錯誤發生的行數在哪裡
# 也可以設定個別的exception breakpoints給python,jinja2等等

## 斷點設定方法 :
# break point : 點選程式行碼
# exception breakpoints : 按crtl + shift + f8，進入breakpoints選擇，依照自己需求選擇斷點

## 設定斷點的好處，可以快速找到錯誤行數

#%%
## 執行參數設定與使用原因
## 1. 點選右上角專案名稱
## 2. 找到Edit Configurations
## 3. 找到script parameters並輸入指定parameters

## 設定parameters原因:
## 雖然使用terminal也可以指定參數，但每次執行都必須重新輸入，當某些參數可以鎖死不需要每次都輸入時，直接在pycharm設定即可
## 優點在於，使用pycharm鎖死參數，可以避免浪費每次都要重新輸入的時間，若要更改參數時，也可透過pycharm中內部設定做更改，不會直接更改到主程式

## 以下為例
import argparse

parser = argparse.ArgumentParser(description="orders")

parser.add_argument("--food", required=str, help="輸入食物名稱")
parser.add_argument("--drink", required=str, help="輸入飲料名稱")
parser.add_argument("--side", required=str, help="輸入附餐名稱")

args = parser.parse_args()

print(f"我要一份:{args.food}、{args.drink}附餐要{args.side}!")

#%%
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

#%%
# 2. python程式開發

#%%
## 虛擬環境操作 - 如何確認當前虛擬環境
## 查看目的 : 確保套件安裝在正確的環境中，並確保開發者之間環境一致

#方法1. 程式執行
import sys
print(sys.executable)

#方法2. terminal執行
## python --version

#%%
## 虛擬環境操作 - requirements.txt的意義為何，如何建立與使⽤
## requirements.txt是為了使開發者的環境都達到統一，避免version不同導致差異

## 如何建立requirements.txt
#1. 可以自己手動新增requirements.txt，寫入所需套件與版本
#2. 如果已經有專案了，可以在terminal中自動生成，輸入pip freeze > requirements.txt(這個方法也可以使用在已經有requirements.txt的情況下，一邊開發一邊新增使用套件)

## 如何讀取requirements.txt
## 在terminal中讀取並安裝 : pip install -r requirements.txt

#%%
## python基本練習
## 如何執行一隻python程式
## 編輯好程式後，需要一個interpreter來解讀程式給電腦看，類似一種翻譯器，使電腦先讀懂我們的code再做執行
## 在pycharm介面，可以點選右下角，選擇add new interpreter --> add local interpreter --> 可以選擇創造新的(generate new)、或是選擇已經存在的(select existing)

#%%
## 資料結構 - set
## set中不允許相同元素存在、可去除重複元素，以jieba斷詞為例

import jieba

text = '今天的天氣很好，我的心情也很好，下班後想去咖啡廳、書局，但時間不夠，只好回家'

text_token = jieba.lcut(text, cut_all=False)
text_set = set(text_token)  ## 使用set可得出text有那些詞組
print(text_set)
print('共有:',len(text_set),'個詞組')
# >>>{'下班', '，', '但', '時間', '、', '心情', '的', '好', '我', '書局', '只好', '回家', '天氣', '廳', '後', '很', '去', '也', '想', '今天', '不夠', '咖啡'}
# >>>共有: 22 個詞組

## set是無序的，與list或tuple不同，因此set通常有整合的意義
## 也可以充作找交集的工具，例如下面sent1、sent2，透過交集找出可能的stop words

sent1 = "syntax tree是一種句法樹狀圖，可以清楚知道支配與被支配的詞，常見的像是NP、VP、TP"
sent2 = "VP表示動詞片語，基本單元一動詞一受詞、NP表示名詞片語，漢語基本單元是一名詞，以此類推，這些片語組成的圖我們稱syntax tree"

sent1_set = set(jieba.lcut(sent1, cut_all=False))
sent2_set = set(jieba.lcut(sent2, cut_all=False))
common_token = sent1_set & sent2_set

print(common_token)
# >>>{'詞', '的', 'VP', '，', 'syntax', 'tree', ' ', '、', 'NP', '是'}