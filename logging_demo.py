# %%
## logging
# 層級與意義
# 如何輸出⾄console

## Logging類似一種紀錄本，使開發者透過記錄，分析錯誤和記錄關鍵事件

import logging

# 設定日誌格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.INFO表示，從INFO開始的對應數值往上排查，因此dubug 對應數值10不會被檢查
logging.debug("這是debug")  # debug 對應數值10
logging.info("這是info")  # info 對應數值20
logging.warning("這是warning")  # warning 對應數值30
logging.error("這是error")  # error 對應數值40
logging.critical("這是critical")  # critical 對應數值50

# >>>2025-02-10 09:20:53,147 - root - INFO - 這是info
# >>>2025-02-10 09:20:53,154 - root - WARNING - 這是warning
# >>>2025-02-10 09:20:53,154 - root - ERROR - 這是error
# >>>2025-02-10 09:20:53,154 - root - CRITICAL - 這是critical

# %%
# 如何輸出⾄file

import logging

logging.basicConfig(level=logging.INFO,
                    filename='logdemo.log',  # 將日誌記錄在名為logdemo.log的檔案中
                    filemode='w',  # w表示填寫，這樣會使logdemo.log在每次執行後都被重新填寫，如果不要被重新填寫，可以用a(append)添加
                    encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)  # logger的名字

logging.debug("這是debug")  # debug 對應數值10
logging.info("這是info")  # info 對應數值20
logging.warning("這是warning")  # warning 對應數值30
logging.error("這是error")  # error 對應數值40
logging.critical("這是critical")  # critical 對應數值50

## 剛剛上面輸出至console的訊息，就會被記錄在名為logdemo.log的日誌中
# %%
## 想同時輸出在console與logdemo.log中
import logging

# 設定 Handler
console_handler = logging.StreamHandler()  # 輸出到 Console
file_handler = logging.FileHandler("logdemo2.log", "w", encoding='utf-8')  # 輸出到檔案

# 設定 Logger
logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])

logging.info("訊息會出現在Console也會寫入logdemo2.log")