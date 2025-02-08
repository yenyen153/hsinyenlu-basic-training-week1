# %%
## Function - Return
## 在def func()中，print只是把結果展示出，但沒辦法賦予他一個變數，而使用return則是把結果傳回程式，我們可以對這個return的結果賦予一個變數

def num_sum(*args):
    print(sum(args))


num1 = num_sum(13, 5, 267, 7, 45)

num_sum(13, 5, 267, 7, 45)
print(num1)


# >>> 337
# >>> 337
# >>> None
## 並沒有辦法把print的值給予一個變數，因此num1回傳的值是None

# %%
def num_sum2(*args):
    return sum(args)


num2 = num_sum2(13, 5, 267, 7, 45)

num_sum2(13, 5, 267, 7, 45)
print(num2)


# >>> 337
## num_sum2只有把值回傳給程式，並沒有print的概念，因此不會把結果展示出
## 而當賦予一個變數名稱，就可以用在print上

## 因此可以總結，當接下來的程式需要用到function所產生的結果時，可用return回傳數值，並給予變數名稱
## 單純要檢視function產生結果時，用print，或是不確定return值的型態，也可以用print檢查