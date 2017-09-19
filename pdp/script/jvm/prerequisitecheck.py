from pdp.utility.file import File
from pdp.utility.ssh import SSH


class JvmRunScriptPrerequisite:
    deploy_ssh = None

    def __init__(self, user, host, deploy_run_script, artifact_host, artifact_run_script):
        self.user = user
        self.host = host
        self.deploy_run_script = deploy_run_script
        self.artifact_host = artifact_host
        self.artifact_run_script = artifact_run_script

    def check(self):
        self.deploy_ssh = SSH(self.user, self.host)
        self.deploy_ssh.connect()

        if self.is_jvm_run_script_deployed() is False:
            self.deploy_jvm_run_script()

        self.deploy_ssh.disconnect()

    def is_jvm_run_script_deployed(self):
        # todo: use self.deploy_ssh to execute command to obtain file
        return False

    def deploy_jvm_run_script(self):
        pulled_file = self.artifact_host.get_artifact(self.artifact_run_script)

        pf = File(pulled_file)
        pulled_file_contents = pf.read()

        # replace the file contents
        # todo: where to get the values?
        replaced_file_contents = pulled_file_contents

        pf.write(replaced_file_contents)

        # deploy the updated file to host
        self.deploy_ssh.push_file(pulled_file, self.deploy_run_script)
