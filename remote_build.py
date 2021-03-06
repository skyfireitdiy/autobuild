import os
import uuid
import subprocess

from jinja2 import Template

from env import all_push, all_pop, system_type
from logger import logger
from script_gen import generate_script
from ssh import SSHClient
from vcs import get_code


def remote_build(name, project_config):
    all_push()
    dir_name = name + "_" + uuid.uuid4().hex
    project_dir = os.path.abspath(dir_name)
    if system_type == "Linux":
        project_dir = project_dir.replace("\\", "/")
    else:
        project_dir = project_dir.replace("/", "\\")
    os.makedirs(project_dir)
    os.environ["_PROJECT_DIR"] = project_dir
    os.chdir(project_dir)
    logger.info("project dir: %s", project_dir)

    ssh_client = SSHClient(project_config["ssh"])
    if not ssh_client.connect():
        logger.error("ssh connect error")
        all_pop()
        return False
    remote_root = ssh_client.pwd()
    os.environ["_REMOTE_ROOT"] = remote_root
    project_dir = os.path.join(remote_root, dir_name)
    if project_config["os"] == "Linux":
        project_dir = project_dir.replace("\\", "/")
    else:
        project_dir = project_dir.replace("/", "\\")
    os.environ["_PROJECT_DIR_REMOTE"] = project_dir

    if "env" in project_config:
        for key, value in project_config["env"].items():
            real_value = Template(value).render(os.environ)
            os.environ[key] = real_value
            logger.info("set env: %s = %s", key, real_value)

    if "before" in project_config:
        before_command, _ = generate_script(project_config["before"], system_type, prefix="before_build")
        ret = subprocess.call([before_command], shell=True, env=os.environ)
        if ret != 0:
            all_pop()
            logger.error("pre build error")
            return False
    if "vcs" in project_config:
        vcs_config = project_config["vcs"]
        if "before" in project_config["vcs"]:
            before_command, _ = generate_script(project_config["vcs"]["before"], system_type, prefix="before_get_code")
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
            after_command, _ = generate_script(project_config["vcs"]["after"], system_type, prefix="after_get_code")
            ret = subprocess.call([after_command], shell=True, env=os.environ)
            if ret != 0:
                all_pop()
                logger.error("post get code error")
                return False
    logger.info("uploading project source ...")
    if not ssh_client.upload_file(os.path.join("..", dir_name), project_dir):
        logger.error("upload project source error: %s", os.path.join("..", dir_name))
        all_pop()
        return False

    if "build" in project_config:
        logger.info("generate build command file ...")
        build_cmd, local_file = generate_script(project_config["build"], project_config["os"], remote=True, prefix="build")
        if not ssh_client.upload_file(local_file, build_cmd):
            logger.error("upload build script error")
            all_pop()
            return False

        if project_config["os"] == "Linux":
            if ssh_client.run_command("chmod +x \"" + build_cmd + "\"") != 0:
                logger.error("chmod error")
                all_pop()
                return False

        logger.info("start build ...")
        if ssh_client.run_command(build_cmd) != 0:
            logger.error("Build error")
            all_pop()
            return False

    if "scp" in project_config:
        for remote,local in project_config["scp"].items():
            remote_path = Template(remote).render(os.environ)
            local_path = Template(local).render(os.environ)
            if not ssh_client.download_file(remote_path, local_path):
                logger.error("download file error:%s", remote_path)
                return False

    if "after" in project_config:
        before_command, _ = generate_script(project_config["before"], system_type, prefix="before_build")
        ret = subprocess.call([before_command], shell=True, env=os.environ)
        if ret != 0:
            all_pop()
            logger.error("pre build error")
            return False

    all_pop()
    return True
