from pdp.utility.file import File
from pdp.utility.ssh import SSH


class ArtifactHost:

    def __init__(self, user, host, private_key_file=None):
        self.user = user
        self.host = host
        self.private_key_file = private_key_file

    def get_artifact(self, artifact_path):
        ssh = SSH(self.user, self.host, self.private_key_file)
        ssh.connect()
        ssh.pull_file(artifact_path)
        ssh.disconnect()
        return artifact_path.split('/')[-1]

    def get_artifact_file_content(self, artifact_path):
        ssh = SSH(self.user, self.host, self.private_key_file)
        ssh.connect()
        file_content = ssh.pull_file_contents(artifact_path)
        ssh.disconnect()
        return file_content

    def publish_file(self, local_file_path, artifact_file_path):
        file = File(local_file_path)

        if file.exists() is False:
            return

        ssh = SSH(self.user, self.host, self.private_key_file)
        ssh.connect()

        if ssh.does_file_exist(artifact_file_path) is False:
            ssh.push_file(local_file_path, artifact_file_path)

        ssh.disconnect()
