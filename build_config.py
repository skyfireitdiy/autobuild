import json5


def load_config(file_name):
    global global_config
    with open(file_name, "r", encoding="utf-8") as fp:
        global_config = json5.load(fp)
        return global_config
