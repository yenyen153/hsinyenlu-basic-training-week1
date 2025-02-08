# %%
## Function - Positional Arguments(*args)
## Positional Arguments強調位置，因此args的位置會影響執行效果，以下面為例，位置調換會導致訊息錯誤

def employee(*args):
    print(f"員工姓名:{args[0]}；員工年齡:{args[1]}；員工年資:{args[2]}年")


employee('Jamie', 30, 5)
# >>> 員工姓名:Jamie；員工年齡:30；員工年資:5年
employee(30, 'Jamie', 5)


# >>> 員工姓名:30；員工年齡:Jamie；員工年資:5年

## 總結，當程式強調位置概念*args時，例如語料處理，詞的位置就很重要，若隨意對調會使語意表達不一樣