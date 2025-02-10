# %%
## 假設以下程式在hello2.py中
def say_hello():
    print("hello world")
    print(__name__)


if __name__ == '__main__':
    print('你好啊')
    say_hello()

# >>> 你好啊
# >>> hello world
# >>> __main__