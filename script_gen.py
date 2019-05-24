import os
import uuid

from jinja2 import Template
from logger import logger


def generate_script(command_list, system_type, remote=False, prefix=""):
    if system_type == "Windows":
        command = "@echo off\r\n"
        if remote and "_PROJECT_DIR_REMOTE" in os.environ:
            command += "cd \"" + os.environ["_PROJECT_DIR_REMOTE"] + "\"\r\n"
        elif "_PROJECT_DIR" in os.environ:
            command += "cd \"" + os.environ["_PROJECT_DIR"] + "\"\r\n"
        for cmd in command_list:
            command += Template(cmd).render(os.environ) + "\r\n"
            command += "if not %errorlevel%==0 exit %errorlevel%\r\n"
        cmd_file = prefix + "_" + uuid.uuid4().hex + ".bat"
        if remote and "_PROJECT_DIR_REMOTE" in os.environ:
            full_path = os.path.join(os.environ["_PROJECT_DIR_REMOTE"], cmd_file).replace("/", "\\")
        elif remote and "_REMOTE_ROOT" in os.environ:
            full_path = os.path.join(os.environ["_REMOTE_ROOT"], cmd_file).replace("/", "\\")
        elif "_PROJECT_DIR" in os.environ:
            full_path = os.path.join(os.environ["_PROJECT_DIR"], cmd_file).replace("/", "\\")
        else:
            full_path = os.path.abspath(cmd_file).replace("/", "\\")
    else:
        command = "#!/bin/sh\n"
        command += "set -e\n"
        if remote and "_PROJECT_DIR_REMOTE" in os.environ:
            command += "cd \"" + os.environ["_PROJECT_DIR_REMOTE"] + "\"\n"
        elif "_PROJECT_DIR" in os.environ:
            command += "cd \"" + os.environ["_PROJECT_DIR"] + "\"\n"
        for cmd in command_list:
            command += Template(cmd).render(os.environ) + "\n"
        cmd_file = prefix + "_" + uuid.uuid4().hex + ".sh"
        if remote and "_PROJECT_DIR_REMOTE" in os.environ:
            full_path = os.path.join(os.environ["_PROJECT_DIR_REMOTE"], cmd_file).replace("\\", "/")
        elif remote and "_REMOTE_ROOT" in os.environ:
            full_path = os.path.join(os.environ["_REMOTE_ROOT"], cmd_file).replace("\\", "/")
        elif "_PROJECT_DIR" in os.environ:
            full_path = os.path.join(os.environ["_PROJECT_DIR"], cmd_file).replace("\\", "/")
        else:
            full_path = os.path.abspath(cmd_file).replace("\\", "/")
    with open(cmd_file, "wb") as fp:
        if system_type == "Windows":
            fp.write(command.encode('gbk'))
        else:
            fp.write(command.encode('utf-8'))
    logger.info("generate cmd file:%s", cmd_file)

    return full_path, cmd_file
