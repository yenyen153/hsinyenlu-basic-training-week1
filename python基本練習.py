## 如何執行一隻python程式
## 編輯好程式後，需要一個interpreter來解讀程式給電腦看，類似一種翻譯器，使電腦先讀懂我們的code再做執行
## 在pycharm介面，可以點選右下角，選擇add new interpreter --> add local interpreter --> 可以選擇創造新的(generate new)、或是選擇已經存在的(select existing)

# %%
## 資料結構 - set
## set中不允許相同元素存在、可去除重複元素，以jieba斷詞為例

import jieba

text = '今天的天氣很好，我的心情也很好，下班後想去咖啡廳、書局，但時間不夠，只好回家'

text_token = jieba.lcut(text, cut_all=False)
text_set = set(text_token)  ## 使用set可得出text有那些詞組
print(text_set)
print('共有:', len(text_set), '個詞組')
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

# %%
## 資料結構 - list
## list是有順序且能對list中的元素增減，並允許重複元素存在
## 銜接上面使用的例句，下面以有序的方式在list內添加詞彙做示範

text_token.insert(text_token.index('書局') + 1, '電影院')  # 可以使用insert去指定添加詞與位置
print(text_token)
# >>>['今天', '的', '天氣', '很', '好', '，', '我', '的', '心情', '也', '很', '好', '，', '下班', '後', '想', '去', '咖啡', '廳', '、', '書局', '電影院', '，', '但', '時間', '不夠', '，', '只好', '回家']

## 刪除提示詞
stop_words = {'我', '的', '但', '，', '也'}  # 可以使用list comprehension刪除停用詞
token_without_stopwords = [words for words in text_token if words not in stop_words]
print(token_without_stopwords)
# >>>['今天', '天氣', '很', '好', '心情', '很', '好', '下班', '後', '想', '去', '咖啡', '廳', '、', '書局', '電影院', '時間', '不夠', '只好', '回家']

## 找出詞頻
text_freq = [text_token.count(freq) for freq in set(text_token)]
print(text_freq)
# >>>[1, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1]

## 可找出詞的順序
## list有序的概念可以使語意更清楚，以下為例
sent1 = "the cat sit on the table".split()  # >>>['the', 'cat', 'sit', 'on', 'the', 'table']
sent2 = "the tabel sit on the cat".split()  # >>>['the', 'table', 'sit', 'on', 'the', 'cat']
## 上述sent1,sent2的cat與table調換後，是完全不同意思

# %%
## 資料結構 - tuple
## tuple內容是不能被更改的，因此當資料是不能被更動時，可以使用tuple
## 同樣使用上面的text為例

import jieba.posseg as pseg

text_pos_cut = pseg.cut(text)  # 使用jieba對text進行斷詞並分類詞性
text_pos = [(word, pos) for word, pos in text_pos_cut]  # 因詞與詞性是固定的，不可做修改，以tuple將兩者打包
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

# %%
## 資料結構 - dict
## 銜接tuple部分，雖然tuple可以將詞與詞性組合，並保持資料內容，但tuple不好以直觀方式搜查詞所對應的詞性
## 而使用dict的話，可以用key(詞)查詢value(詞性)，更加方便
## 以剛剛的text_pos tuple作為例子
## text_pos [('今天', 't'), ('天氣', 'n'), ('真好', 'd'), ('，', 'x'), ('好', 'a'), ('想', 'v'), ('去', 'v'), ('環球', 'n'), ('影城', 'n'), ('玩', 'v')]

text_pos_dict = dict(text_pos)
print(text_pos_dict)
print('天氣的詞性:', text_pos_dict['天氣'])  # 用dict key,value概念去查找'天氣'的詞性
# >>>{'今天': 't', '的': 'uj', '天氣': 'n', '很': 'd', '好': 'a', '，': 'x', '我': 'r', '心情': 'n', '也': 'd', '下班': 'v', '後': 'nr', '想': 'v', '去': 'v', '咖啡': 'n', '廳': 'x', '、': 'x', '書局': 'n', '但': 'c', '時間': 'n', '不夠': 'v', '只好': 'd', '回家': 'n'}
# >>>天氣的詞性: n

## 也可以將詞出現的次數變成dict
text_num_dict = {word: text_token.count(word) for word in text_token}
print(text_num_dict)


# >>>{'今天': 1, '的': 2, '天氣': 1, '很': 2, '好': 2, '，': 4, '我': 1, '心情': 1, '也': 1, '下班': 1, '後': 1, '想': 1, '去': 1, '咖啡': 1, '廳': 1, '、': 1, '書局': 1, '電影院': 1, '但': 1, '時間': 1, '不夠': 1, '只好': 1, '回家': 1}
