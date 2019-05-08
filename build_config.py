import json5

from logger import logger

with open("config.json", "r", encoding="utf-8") as fp:
    global_config = json5.load(fp)
    logger.info("load config complete")
