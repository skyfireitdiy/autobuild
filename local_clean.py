from script_gen import generate_script
from env import system_type, all_push, all_pop
from jinja2 import Template
import subprocess
import os

def local_clean(clean_config):
    all_push()
    if "env" in clean_config:
        for key, value in clean_config["env"].items():
            real_value = Template(value).render(os.environ)
            os.environ[key] = real_value
    if "cmd" not in clean_config:
        all_pop()
        return
    clean_cmd, _ = generate_script(clean_config["cmd"], system_type, prefix="clean")
    subprocess.call([clean_cmd], shell=True, env=os.environ)
    os.remove(clean_cmd)
    all_pop()
    