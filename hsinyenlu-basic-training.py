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