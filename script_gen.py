import os
import uuid

from jinja2 import Template
from logger import logger


def generate_script(command_list, system_type):
    if system_type == "Windows":
        command = "@echo off\n"
        if "_PROJECT_DIR" in os.environ:
            command += "cd \"" + os.environ["_PROJECT_DIR"] + "\"\n"
        cmd_file = uuid.uuid4().hex + ".bat"
        if "_PROJECT_DIR" in os.environ:
            full_path = os.path.join(os.environ["_PROJECT_DIR"], cmd_file).replace("/", "\\")
        else:
            full_path = os.path.abspath(cmd_file).replace("/", "\\")
    else:
        command = "#!/bin/sh\n"
        if "_PROJECT_DIR" in os.environ:
            command += "cd \"" + os.environ["_PROJECT_DIR"] + "\"\n"
        cmd_file = uuid.uuid4().hex + ".sh"
        if "_PROJECT_DIR" in os.environ:
            full_path = os.path.join(os.environ["_PROJECT_DIR"], cmd_file).replace("\\", "/")
        else:
            full_path = os.path.abspath(cmd_file).replace("\\", "/")
    for cmd in command_list:
        command += Template(cmd).render(os.environ) + "\n"
    with open(cmd_file, "wb") as fp:
        fp.write(command.encode("utf-8"))
    logger.info("generate cmd file:%s", cmd_file)

    return full_path, cmd_file
