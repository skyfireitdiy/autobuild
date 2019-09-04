import json5

global_config = None


def load_config(file_name):
    with open(file_name, "r", encoding="utf-8") as fp:
        global_config = json5.load(fp)
