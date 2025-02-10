# %%
## 假設以下程式在goodbye.py中
# hello1.py沒使用if __name__ == '__main__'分割自定義function與主程式情況下
# hello1.py中的主程式也會被goodbye.py引用
from hello1 import say_hello

say_hello()
print('掰掰')
# >>> 你好啊
# >>> hello world
# >>> hello
# >>> hello world
# >>> hello
# >>> 掰掰

# %%
# hello2.py有分割自定義function與主程式情況下
# 僅會引用hello2.py中的自定義function，hello2.py本身並沒有被觸發
# ## 因此if __name__ == '__main__':的條件不成立，接下來的程式不會被執行
from hello2 import say_hello

say_hello()
print('掰掰')


# >>> hello world
# >>> hello
# >>> 掰掰