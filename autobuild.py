import logging
import os
import datetime
import subprocess
import argparse

from jinja2 import Template

from build_config import load_config
from env import all_push, all_reset, system_type
from local_build import local_build
from logger import logger
from remote_build import remote_build
from script_gen import generate_script
from local_clean import local_clean
from remote_clean import remote_clean


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', type=str,
                        help='Config file name', default='config.json5')
    args = parser.parse_args()
    config_file = args.config_file
    global_config = load_config(config_file)

    start_time = datetime.datetime.now()
    all_push()

    sln_dir = os.path.abspath(
        datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S-build"))
    os.makedirs(sln_dir)
    os.environ["_SLN_DIR"] = sln_dir
    os.chdir(sln_dir)

    if system_type == "Windows":
        logger.info("os : Windows")
    elif system_type == "Linux":
        logger.info("os : Linux")
    else:
        logger.error("Unsupport platform:%s", system_type)
        all_reset()
        return

    logger.info("solution dir: %s", sln_dir)

    build_result = {}

    if "build" not in global_config:
        logger.error("build nothing")
        all_reset()

    if "env" in global_config:
        for key, value in global_config["env"].items():
            real_value = Template(value).render(os.environ)
            os.environ[key] = real_value
            logger.info("set env: %s = %s", key, real_value)

    if "before" in global_config:
        before_command, _ = generate_script(
            global_config["before"], system_type, prefix="before_sln")
        ret = subprocess.call([before_command], shell=True, env=os.environ)
        if ret != 0:
            logger.error("prebuild error")
            return
    for name in global_config["project"].keys():
        build_result[name] = 1
    for project_name in global_config["build"]:
        project_detail = project_detail = global_config["project"][project_name]
        if "type" not in project_detail or project_detail["type"] == "local":
            logger.info("local build %s ...", project_name)
            if local_build(project_name, project_detail):
                build_result[project_name] = 0
            else:
                build_result[project_name] = -1
                if "stop_on_error" not in global_config or global_config["stop_on_error"]:
                    break
        else:
            logger.info("remote build %s ...", project_name)
            if remote_build(project_name, project_detail):
                build_result[project_name] = 0
            else:
                build_result[project_name] = -1
                if "stop_on_error" not in global_config or global_config["stop_on_error"]:
                    break

    if "after" in global_config:
        before_command, _ = generate_script(
            global_config["after"], system_type, prefix="after_sln")
        ret = subprocess.call([before_command], shell=True, env=os.environ)
        if ret != 0:
            logger.error("postbuild error")
            return
    os.chdir(os.path.join(sln_dir, ".."))
    if "clean" in global_config:
        for clean_config in global_config["clean"]:
            if "type" not in clean_config or clean_config["type"] == "local":
                local_clean(clean_config)
            else:
                remote_clean(clean_config)

    for name, result in build_result.items():
        if result == 0:
            ret_str = "Succeed"
        elif result == 1:
            ret_str = "Skip"
        else:
            ret_str = "Failed"
        logger.info("%20s -> %10s" % (name, ret_str))
    cost = (datetime.datetime.now()-start_time).seconds
    logger.info("Time cost: %dm %ds" % (cost//60, cost % 60))
    all_reset()


if __name__ == "__main__":
    main()
