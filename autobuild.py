import os
from datetime import datetime

from jinja2 import Template

from build_config import global_config
from env import all_push, all_reset, system_type
from local_build import local_build
from logger import logger
from remote_build import remote_build
from script_gen import generate_script
import subprocess


def main():
    all_push()
    if system_type == "Windows":
        logger.info("os : Windows")
    elif system_type == "Linux":
        logger.info("os : Linux")
    else:
        logger.error("Unsupport platform:%s", system_type)
        all_reset()
        return
    sln_dir = os.path.abspath(datetime.now().strftime("%Y-%m-%d_%H_%M_%S-build"))
    os.makedirs(sln_dir)
    os.environ["_SLN_DIR"] = sln_dir
    os.chdir(sln_dir)
    logger.info("solution dir: %s", sln_dir)

    build_result = {}

    if "env" in global_config:
        for key, value in global_config["env"].items():
            real_value = Template(value).render(os.environ)
            os.environ[key] = real_value
            logger.info("set env: %s = %s", key, real_value)

    if "before" in global_config:
        before_command, _ = generate_script(global_config["before"], system_type)
        ret = subprocess.call([before_command])
        if ret != 0:
            logger.error("prebuild error")
            return

    project_config = global_config["project"]
    for project_name, project_detail in project_config.items():
        if "skip" in project_detail:
            build_result[project_name] = 1
            continue
        if "before" in global_config:
            before_command, _ = generate_script(global_config["before"], system_type)
            ret = subprocess.call([before_command])
            if ret != 0:
                build_result[project_name] = -1
                logger.error("prebuild project error")
                continue
        if project_detail["type"] == "local":
            logger.info("local build %s ...", project_name)
            if local_build(project_detail):
                build_result[project_name] = 0
            else:
                build_result[project_name] = -1
                continue
        else:
            logger.info("remote build %s ...", project_name)
            if remote_build(project_detail):
                build_result[project_name] = 0
            else:
                build_result[project_name] = -1
                continue
        if build_result[project_name] == 0:
            if "after" in global_config:
                before_command, _ = generate_script(global_config["after"], system_type)
                ret = subprocess.call([before_command])
                if ret != 0:
                    build_result[project_name] = -1
                    logger.error("postbuild project error")
                    continue

    if "after" in global_config:
        before_command, _ = generate_script(global_config["after"], system_type)
        ret = subprocess.call([before_command])
        if ret != 0:
            logger.error("postbuild error")
            return
    all_reset()
    for name, result in build_result.items():
        if result == 0:
            ret_str = "Succeed"
        elif result == 1:
            ret_str = "Skip"
        else:
            ret_str = "Failed"
        logger.info("%20s -> %10s" % (name, ret_str))


if __name__ == "__main__":
    main()
