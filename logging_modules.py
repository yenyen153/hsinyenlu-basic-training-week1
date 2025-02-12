def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("num_logging.log",encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()  