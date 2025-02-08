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