import subprocess
import os
from jinja2 import Template


def get_code(vcs_config):
    if vcs_config["type"] == "git":
        cmd = ["git", "clone", Template(vcs_config["addr"]).render(os.environ)]
    elif vcs_config["type"] == "svn":
        cmd = ["svn", "export", Template(vcs_config["addr"]).render(os.environ), "--username", Template(vcs_config["username"]).render(os.environ),
               "--password", Template(vcs_config["password"]).render(os.environ), "--trust-server-cert-failures=unknown-ca", "--non-interactive"]
    ret = subprocess.check_call(cmd, shell=True, env=os.environ)
    return ret == 0
