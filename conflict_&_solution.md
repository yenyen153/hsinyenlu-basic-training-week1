# 衝突conflict
## 是指當檔案合併時版本不一致發生的問題，例如

- A電腦中的hello.py
>print("hello world")

將hello.py上傳至github

- B電腦clone A電腦創造的repository，並新增branch new_one，在new_one中更改hello.py並commit:
>print("no greeting")
- B電腦new_one中另外再新增並commit一個bye.py
>print("byebye")

- B電腦 git push

## 此時將兩個branch於github上merge，會顯示無法merge，表示發生了conflict
### 原因: B電腦更改了hello.py，因此merge時程式並不知道你要以哪個版本的hello.py為主
### 因此最根本方法就是，選擇你要的版本，來解決版本衝突

## 解決步驟
- 1 . 在B電腦中切換到master
>git switch master
- 2 . 透過pull抓取最新的repository
>git pull
- 3 . 切回剛剛的new_one分支，並做rebase
>git rebase master
- 4 . 發生conflict，打開發生conflict的檔案，選擇自己要的版本，刪除不要的
- 5 . 編輯好後，再次add檔案，輸入:
>git rebase --continue
- 6 . 用git log確認一下
- 7 . 重新push到github
- 8 . 重新整理github網頁，即可重新merge檔案

