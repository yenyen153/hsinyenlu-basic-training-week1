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