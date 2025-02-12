 %%
## if __name__ == '__main__'的概念與應用

## if __name__ == '__main__'能用來切割程式內自定義function與主程式
## 之所以能切割，首先要了解__name__代表甚麼
## __name__ 在py檔執行時，會被自動設為 '__main__'，以下面為例，如果執行這分檔案，他會將__name__設為__main__

print(__name__)
# >>> __main__


# %%
## 所以當if __name__ == '__main__'表示，當這個假設被觸發時，代表這份檔案正在被執行，也因此下面的主程式才會跟著執行
## 之所以要切割自定義function與主程式，以hello1.py、hello2.py、goodbye.py舉例
## 參考檔案於"切割主程式展示"branch中展示

## 假設以下程式在hello1.py中
def say_hello():
    print("hello world")
    print(__name__)


print('你好啊')
say_hello()


# >>> 你好啊
# >>> hello world
# >>> __main__