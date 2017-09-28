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

    def execute_remote_command(self, remote_command, pseudo_terminal=True):
        return self.ssh_client.exec_command(remote_command, pseudo_terminal)

    def execute_remote_process_command(self, remote_command):
        ssh_transport = self.ssh_client.get_transport()
        out_data, err_data = b'', b''
        ssh_channel = ssh_transport.open_session()
        ssh_channel.setblocking(0)
        ssh_channel.exec_command(remote_command)
        while True:
            while ssh_channel.recv_ready():
                out_data += ssh_channel.recv(1000)
            while ssh_channel.recv_stderr_ready():
                err_data += ssh_channel.recv_stderr(1000)
            if ssh_channel.exit_status_ready():
                break
            time.sleep(0.001)
        return_code = ssh_channel.recv_exit_status()
        return return_code

    def does_file_exist(self, remote_file):
        stdin, stdout, stderr = self.execute_remote_command('test -e ' + remote_file + '; echo $?')
        result = int(stdout.read())
        return True if result == 0 else False

    def does_dir_exist(self, remote_dir):
        stdin, stdout, stderr = self.execute_remote_command('test -d ' + remote_dir + '; echo $?')
        result = int(stdout.read())
        return True if result == 0 else False

    def pull_file(self, remote_file, local_dir=''):
        with scp.SCPClient(self.ssh_client.get_transport()) as scp_client:
            scp_client.get(remote_file, local_dir)

    def pull_file_contents(self, remote_file):
        stdin, stdout, stderr = self.execute_remote_command('cat ' + remote_file)
        return ''.join(stdout.readlines())

    def push_file(self, local_file, remote_file, make_executable=False):
        if '/' in remote_file:
            remote_dir = remote_file[:remote_file.rindex('/')+1]
            self.execute_remote_command('mkdir -p ' + remote_dir)

        with scp.SCPClient(self.ssh_client.get_transport()) as scp_client:
            scp_client.put(local_file, remote_file)

        if make_executable is True:
            self.execute_remote_command('chmod +x ' + remote_file)

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


class RemoteHost:

    def __init__(self, user, host):
        self.user = user
        self.host = host


class SecureRemoteCopy:

    def __init__(self, source_remote_host, target_remote_host, key_file):
        self.source_remote_host = source_remote_host
        self.target_remote_host = target_remote_host
        self.key_file = key_file

    def copy_between_hosts(self, remote_source_file, remote_target_file):
        remote_copy_command = "scp -i {0} -3 {1}@{2}:{3} {4}@{5}:{6}".format(self.key_file,
                                                                             self.source_remote_host.user,
                                                                             self.source_remote_host.host,
                                                                             remote_source_file,
                                                                             self.target_remote_host.user,
                                                                             self.target_remote_host.host,
                                                                             remote_target_file)
        os.system(remote_copy_command)


class SSHConnectException(Exception):
    pass
