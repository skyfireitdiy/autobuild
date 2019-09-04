from env import all_push, all_pop, system_type
from jinja2 import Template
import os
from logger import logger
from vcs import get_code
import uuid
from script_gen import generate_script
import subprocess


def local_build(name, project_config):
    all_push()
    project_dir = os.path.abspath(name + "_" + uuid.uuid4().hex)
    if system_type == "Linux":
        project_dir = project_dir.replace("\\", "/")
    else:
        project_dir = project_dir.replace("/", "\\")
    os.makedirs(project_dir)
    os.environ["_PROJECT_DIR"] = project_dir
    os.chdir(project_dir)
    logger.info("project dir: %s", project_dir)
    if "env" in project_config:
        for key, value in project_config["env"].items():
            real_value = Template(value).render(os.environ)
            os.environ[key] = real_value
            logger.info("set env: %s = %s", key, real_value)

    if "before" in project_config:
        before_command, _ = generate_script(
            project_config["before"], system_type, prefix="before_build")
        ret = subprocess.call([before_command], shell=True, env=os.environ)
        if ret != 0:
            all_pop()
            logger.error("pre build error")
            return False
    if "vcs" in project_config:
        vcs_config = project_config["vcs"]
        if "before" in project_config["vcs"]:
            before_command, _ = generate_script(
                project_config["vcs"]["before"], system_type, prefix="before_get_code")
            ret = subprocess.call([before_command], shell=True, env=os.environ)
            if ret != 0:
                all_pop()
                logger.error("pre get code error")
                return False

        if not get_code(vcs_config):
            logger.error("get code error")
            all_pop()
            return False

        if "after" in project_config["vcs"]:
            after_command, _ = generate_script(
                project_config["vcs"]["after"], system_type, prefix="after_get_code")
            ret = subprocess.call([after_command], shell=True, env=os.environ)
            if ret != 0:
                all_pop()
                logger.error("post get code error")
                return False
    else:
        logger.info("Skip get code ...")
    if "build" in project_config:
        logger.info("generate build command file ...")
        build_cmd, _ = generate_script(
            project_config["build"], system_type, prefix="build")
        logger.info("start build ...")
        ret = subprocess.call([build_cmd], shell=True, env=os.environ)
        if ret != 0:
            logger.error("Build error")
            all_pop()
            return False

    if "after" in project_config:
        before_command, _ = generate_script(
            project_config["before"], system_type, prefix="before_build")
        ret = subprocess.call([before_command], shell=True, env=os.environ)
        if ret != 0:
            all_pop()
            logger.error("pre build error")
            return False

    all_pop()
    return True
