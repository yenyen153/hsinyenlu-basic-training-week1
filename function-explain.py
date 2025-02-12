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

# %%
## Function - Keyword Arguments(**kwargs)
## Keyword Arguments強調關鍵字，與前面*args強調位置不同，keyword arguments只要輸入符合的關鍵字，位置並不影響表達
def employee2(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}:{value}")


employee2(員工年齡=30, 員工姓名='Jamie', 員工年資=20)
# >>> 員工年齡:30
# >>> 員工姓名:Jamie
# >>> 員工年資:20

## 總結，使用**kwargs強調的不會是位置，而是key所對應到的value