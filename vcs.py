import subprocess
import os


def get_code(vcs_config):
    if vcs_config["type"] == "git":
        cmd = ["git", "clone", vcs_config["addr"]]
    elif vcs_config["type"] == "svn":
        cmd = ["svn", "export", vcs_config["addr"], "--username", vcs_config["username"],
               "--password", vcs_config["password"], "--trust-server-cert-failures=unknown-ca", "--non-interactive"]
    ret = subprocess.check_call(cmd, shell=True, env=os.environ)
    return ret == 0
