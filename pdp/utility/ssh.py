import os
import paramiko
import scp
import time

from pdp.utility.file import File


class SSH:
    ssh_client = None
    connected = False

    def __init__(self, user, host, key_file=None, port=22):
        self.user = user
        self.host = host
        self.port = port
        self.key_file = key_file

    def is_connected(self):
        return self.connected

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if self.key_file is None:
                self.ssh_client.connect(self.host, username=self.user)
            else:
                self.ssh_client.connect(self.host, username=self.user, key_filename=self.key_file)
        except paramiko.SSHException as e:
            print('SSH Connect Error - configure your SSH key for: ' + self.user + '@' + self.host)
            raise SSHConnectException(e)

        self.connected = False if self.ssh_client.get_transport() is None else True

    def disconnect(self):
        if not self.ssh_client is None:
            self.ssh_client.close()

    def does_file_exist(self, remote_file):
        stdin, stdout, stderr = self.ssh_client.exec_command('test -e ' + remote_file + '; echo $?', get_pty=True)
        result = int(stdout.read())
        return True if result == 0 else False

    def pull_file(self, remote_file, local_dir=''):
        with scp.SCPClient(self.ssh_client.get_transport()) as scp_client:
            scp_client.get(remote_file, local_dir)

    def pull_file_contents(self, remote_file):
        stdin, stdout, stderr = self.ssh_client.exec_command('cat ' + remote_file, get_pty=True)
        return ''.join(stdout.readlines())

    def push_file(self, local_file, remote_file, make_executable=False):
        if '/' in remote_file:
            remote_dir = remote_file[:remote_file.rindex('/')+1]
            self.ssh_client.exec_command('mkdir -p ' + remote_dir, get_pty=True)

        with scp.SCPClient(self.ssh_client.get_transport()) as scp_client:
            scp_client.put(local_file, remote_file)

        if make_executable is True:
            self.ssh_client.exec_command('chmod +x ' + remote_file, get_pty=True)

    def push_file_contents(self, remote_file, file_content, make_executable=False):
        # files are too large, use tmp file
        temp_file_path = self.__create_temp_file(file_content)
        self.push_file(temp_file_path, remote_file, make_executable)
        os.remove(temp_file_path)

    def __create_temp_file(self, file_content):
        file_name = '/tmp/ssh_tmp_file' + time.strftime("%Y%m%d-%H%M%S")
        file = File(file_name)
        file.write(file_content)
        return file_name


class SSHConnectException(Exception):
    pass
