import json5

with open("config.json5", "r", encoding="utf-8") as fp:
    global_config = json5.load(fp)
