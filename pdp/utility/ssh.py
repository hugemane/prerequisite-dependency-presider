import paramiko
import scp


class SSH:
    ssh_client = None
    connected = False

    def __init__(self, user, host, port=22):
        self.user = user
        self.host = host
        self.port = port

    def is_connected(self):
        return self.connected

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.host, username=self.user)
        self.connected = False if self.ssh_client.get_transport() is None else True

    def disconnect(self):
        if not self.ssh_client is None:
            self.ssh_client.close()

    def pull_file(self, remote_file, local_dir=''):
        with scp.SCPClient(self.ssh_client.get_transport()) as scp_client:
            scp_client.get(remote_file, local_dir)

    def push_file(self, local_file, remote_file):
        with scp.SCPClient(self.ssh_client.get_transport()) as scp_client:
            scp_client.put(local_file, remote_file)
