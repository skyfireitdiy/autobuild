import paramiko
from itertools import zip_longest
from scp import SCPClient
from jinja2 import Template
import os
from logger import logger


class SSHClient:
    def __init__(self, ssh_config):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh_config = ssh_config
        self.scp_client = None

    def connect(self):
        try:
            self.ssh_client.connect(Template(self.ssh_config["host"]).render(os.environ),
                                    int(Template(self.ssh_config["port"]).render(os.environ)),
                                    Template(self.ssh_config["username"]).render(os.environ),
                                    Template(self.ssh_config["password"]).render(os.environ))
            self.scp_client = SCPClient(self.ssh_client.get_transport())
            return True
        except:
            return False

    def run_command(self, command, callback=print):
        try:
            logger.info("run remote command:%s", command)
            stdin, stdout, stderr = self.ssh_client.exec_command(command, bufsize=1)
            stdout_iter = iter(stdout.readline, '')
            stderr_iter = iter(stderr.readline, '')
            for out, err in zip_longest(stdout_iter, stderr_iter):
                if out:
                    callback(out.strip())
                if err:
                    callback(err.strip())
            channel = stdout.channel
            return channel.recv_exit_status()
        except:
            return -1

    def pwd(self):
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command("pwd")
            return stdout.read().decode("utf-8").strip()
        except:
            return ""

    def upload_file(self, local_file, remote_file):
        try:
            logger.info("upload file:%s -> %s", local_file, remote_file)
            self.scp_client.put(local_file, remote_file, recursive=True)
            return True
        except:
            return False

    def download_file(self, remote_file, local_file):
        try:
            logger.info("download file:%s -> %s", remote_file, local_file)
            self.scp_client.get(remote_file, local_file, recursive=True)
            return True
        except:
            return False
