import os
import json5
import platform
from logger import logger

_env_stack = []
_dir_stack = []

_default_env = json5.dumps(os.environ)
_default_dir = os.path.abspath(os.curdir)

system_type = platform.system()


def env_push():
    logger.info("env push")
    _env_stack.append(json5.dumps(os.environ))


def env_pop():
    logger.info("env pop")
    os.environ = json5.loads(_env_stack.pop(-1))


def env_reset():
    logger.info("env reset")
    os.environ = json5.loads(_default_env)


def dir_push():
    logger.info("dir push:%s", os.path.abspath(os.curdir))
    _dir_stack.append(os.path.abspath(os.curdir))


def dir_pop():
    os.chdir(_dir_stack.pop(-1))
    logger.info("dir pop:%s", os.path.abspath(os.curdir))


def dir_reset():
    os.chdir(_default_dir)
    logger.info("dir reset:%s", os.path.abspath(os.curdir))


def all_push():
    dir_push()
    env_push()


def all_pop():
    env_pop()
    dir_pop()


def all_reset():
    env_reset()
    dir_reset()
