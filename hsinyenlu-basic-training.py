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

#%%
## 資料結構 - list
## list是有順序且能對list中的元素增減，並允許重複元素存在
## 銜接上面使用的例句，下面以有序的方式在list內添加詞彙做示範

text_token.insert(text_token.index('書局') + 1, '電影院') # 可以使用insert去指定添加詞與位置
print(text_token)
# >>>['今天', '的', '天氣', '很', '好', '，', '我', '的', '心情', '也', '很', '好', '，', '下班', '後', '想', '去', '咖啡', '廳', '、', '書局', '電影院', '，', '但', '時間', '不夠', '，', '只好', '回家']

## 刪除提示詞
stop_words = {'我','的','但','，','也'}  # 可以使用list comprehension刪除停用詞
token_without_stopwords = [words for words in text_token if words not in stop_words]
print(token_without_stopwords)
# >>>['今天', '天氣', '很', '好', '心情', '很', '好', '下班', '後', '想', '去', '咖啡', '廳', '、', '書局', '電影院', '時間', '不夠', '只好', '回家']

## 找出詞頻
text_freq = [text_token.count(freq) for freq in set(text_token)]
print(text_freq)
# >>>[1, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1]

## 可找出詞的順序
## list有序的概念可以使語意更清楚，以下為例
sent1 = "the cat sit on the table".split() # >>>['the', 'cat', 'sit', 'on', 'the', 'table']
sent2 = "the tabel sit on the cat".split() # >>>['the', 'table', 'sit', 'on', 'the', 'cat']
## 上述sent1,sent2的cat與table調換後，是完全不同意思

#%%
## 資料結構 - tuple
## tuple內容是不能被更改的，因此當資料是不能被更動時，可以使用tuple
## 同樣使用上面的text為例

import jieba.posseg as pseg

text_pos_cut = pseg.cut(text)  # 使用jieba對text進行斷詞並分類詞性
text_pos = [(word,pos) for word, pos in text_pos_cut] # 因詞與詞性是固定的，不可做修改，以tuple將兩者打包
print(text_pos)
# >>>[('今天', 't'), ('的', 'uj'), ('天氣', 'n'), ('很', 'd'), ('好', 'a'), ('，', 'x'), ('我', 'r'), ('的', 'uj'), ('心情', 'n'), ('也', 'd'), ('很', 'd'), ('好', 'a'), ('，', 'x'), ('下班', 'v'), ('後', 'nr'), ('想', 'v'), ('去', 'v'), ('咖啡', 'n'), ('廳', 'x'), ('、', 'x'), ('書局', 'n'), ('，', 'x'), ('但', 'c'), ('時間', 'n'), ('不夠', 'v'), ('，', 'x'), ('只好', 'd'), ('回家', 'n')]

## 用於bigram情況下
import nltk
from nltk.util import bigrams

sentence = "I love natural language processing"
tokens = sentence.split()

bigram_list = list(bigrams(tokens))

print(bigram_list)
# >>>[('I', 'love'), ('love', 'natural'), ('natural', 'language'), ('language', 'processing')]
## 可用在以前一個詞預測下個詞出現的機率

#%%
## 資料結構 - dict
## 銜接tuple部分，雖然tuple可以將詞與詞性組合，並保持資料內容，但tuple不好以直觀方式搜查詞所對應的詞性
## 而使用dict的話，可以用key(詞)查詢value(詞性)，更加方便
## 以剛剛的text_pos tuple作為例子
## text_pos [('今天', 't'), ('天氣', 'n'), ('真好', 'd'), ('，', 'x'), ('好', 'a'), ('想', 'v'), ('去', 'v'), ('環球', 'n'), ('影城', 'n'), ('玩', 'v')]

text_pos_dict = dict(text_pos)
print(text_pos_dict)
print('天氣的詞性:', text_pos_dict['天氣']) # 用dict key,value概念去查找'天氣'的詞性
# >>>{'今天': 't', '的': 'uj', '天氣': 'n', '很': 'd', '好': 'a', '，': 'x', '我': 'r', '心情': 'n', '也': 'd', '下班': 'v', '後': 'nr', '想': 'v', '去': 'v', '咖啡': 'n', '廳': 'x', '、': 'x', '書局': 'n', '但': 'c', '時間': 'n', '不夠': 'v', '只好': 'd', '回家': 'n'}
# >>>天氣的詞性: n

## 也可以將詞出現的次數變成dict
text_num_dict = {word:text_token.count(word) for word in text_token}
print(text_num_dict)
# >>>{'今天': 1, '的': 2, '天氣': 1, '很': 2, '好': 2, '，': 4, '我': 1, '心情': 1, '也': 1, '下班': 1, '後': 1, '想': 1, '去': 1, '咖啡': 1, '廳': 1, '、': 1, '書局': 1, '電影院': 1, '但': 1, '時間': 1, '不夠': 1, '只好': 1, '回家': 1}

#%%
## Function - Positional Arguments(*args)
## Positional Arguments強調位置，因此args的位置會影響執行效果，以下面為例，位置調換會導致訊息錯誤

def employee(*args):
    print(f"員工姓名:{args[0]}；員工年齡:{args[1]}；員工年資:{args[2]}年")

employee('Jamie', 30, 5)
# >>> 員工姓名:Jamie；員工年齡:30；員工年資:5年
employee(30,'Jamie',5)
# >>> 員工姓名:30；員工年齡:Jamie；員工年資:5年

## 總結，當程式強調位置概念*args時，例如語料處理，詞的位置就很重要，若隨意對調會使語意表達不一樣

#%%
## Function - Keyword Arguments(**kwargs)
## Keyword Arguments強調關鍵字，與前面*args強調位置不同，keyword arguments只要輸入符合的關鍵字，位置並不影響表達
def employee2(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}:{value}")

employee2(員工年齡 = 30,  員工姓名 = 'Jamie', 員工年資 = 20)
# >>> 員工年齡:30
# >>> 員工姓名:Jamie
# >>> 員工年資:20

## 總結，使用**kwargs強調的不會是位置，而是key所對應到的value