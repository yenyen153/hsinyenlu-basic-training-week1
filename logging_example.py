from logging_modules import setup_logger

logger = setup_logger()

# 數學運算：加法和減法
def add(a, b):
    logger.info(f"執行加法運算: {a} + {b}")
    return a + b


def subtract(a, b):
    logger.info(f"執行減法運算: {a} - {b}")
    return a - b


def main():
    logger.info("程式開始執行")

    x, y = 10, 8

    # 計算加法
    result_add = add(x, y)
    logger.info(f"加法結果: {result_add}")

    # 計算減法
    result_sub = subtract(x, y)
    logger.info(f"減法結果: {result_sub}")

    # 大於15警告
    if result_add > 15:
        logger.warning("加法結果過大！")

    logger.info("程式執行完畢")


if __name__ == "__main__":
    main()