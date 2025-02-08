# %%
## 程式執行方式 - 一般執行

# 1. 點擊pycharm介面右上run<檔名>執行
# 2. 點擊右鍵，選擇run<檔名>執行
# 3. shift + crtl + f10 (有些是shift + f10)
# 另外，使用#%%可分段執行程式，優點在於，需要單看某一部分程式的產出或效果，可以單一執行，避免整份檔案執行

# %%
## 程式執行方式 - 偵錯模式breakpoints

## 有兩種breakpoints : line breakpoints、exception breakpoints
# line breakpoints : 設定在程式碼前的結束點，當程式執行的時候，會依line breakpoints當作程式結束點
# exception breakpoints : 程式有時會有一些錯誤產生，exception breakpoints就是當錯誤發生時會出現的，告知開發者錯誤發生的行數在哪裡
# 也可以設定個別的exception breakpoints給python,jinja2等等

## 斷點設定方法 :
# break point : 點選程式行碼
# exception breakpoints : 按crtl + shift + f8，進入breakpoints選擇，依照自己需求選擇斷點

## 設定斷點的好處，可以快速找到錯誤行數