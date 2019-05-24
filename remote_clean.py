from ssh import SSHClient
from jinja2 import Template
from script_gen import generate_script
from env import all_push, all_pop

from logger import logger
import os


def remote_clean(clean_config):
    ssh_client = SSHClient(clean_config["ssh"])
    if not ssh_client.connect():
        logger.error("connect remote host error")
        return

    if "env" in clean_config:
        for key, value in clean_config["env"].items():
            real_value = Template(value).render(os.environ)
            os.environ[key] = real_value

    remote_root = ssh_client.pwd()
    os.environ["_REMOTE_ROOT"] = remote_root

    if "cmd" in clean_config:
        build_cmd, local_file = generate_script(clean_config["cmd"], clean_config["os"], remote=True, prefix="clean")
        if not ssh_client.upload_file(local_file, build_cmd):
            logger.error("upload script error")
            return
        os.remove(local_file)

        if clean_config["os"] == "Linux":
            if ssh_client.run_command("chmod +x \"" + build_cmd + "\"") != 0:
                logger.error("set priv error")
                return 

        if ssh_client.run_command(build_cmd) != 0:
            return 