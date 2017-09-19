from pdp.reference import ArtifactReference
from pdp.utility.ssh import SSH


class ArtifactHost:

    def __init__(self, user, host):
        self.user = user
        self.host = host

    def get_artifact(self, artifact_path):
        ssh = SSH(self.user, self.host)
        ssh.connect()
        ssh.copy_file(artifact_path)
        ssh.disconnect()

    def get_reference_artifact(self, reference_artifact_key):
        artifact_path = ArtifactReference.get_artifact_reference_path(reference_artifact_key)
        self.get_artifact(artifact_path)

