from pdp.utility.ssh import SSH


class ArtifactHost:

    def __init__(self, user, host):
        self.user = user
        self.host = host

    def get_artifact(self, artifact_path):
        ssh = SSH(self.user, self.host)
        ssh.connect()
        ssh.pull_file(artifact_path)
        ssh.disconnect()
        return artifact_path.split('/')[-1]

    def get_artifact_file_content(self, artifact_path):
        ssh = SSH(self.user, self.host)
        ssh.connect()
        file_content = ssh.pull_file_contents(artifact_path)
        ssh.disconnect()
        return file_content

