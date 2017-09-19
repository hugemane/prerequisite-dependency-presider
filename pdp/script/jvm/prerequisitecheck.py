from pdp.utility.ssh import SSH


class JvmRunScriptPrerequisite:
    def __init__(self, user, host, run_script_path, artifact_host):
        self.user = user
        self.host = host
        self.run_script_path = run_script_path
        self.artifact_host = artifact_host

    def check(self):
        ssh = SSH(self.user, self.host)
        ssh.connect()

        if self.is_jvm_run_script_deployed() is False:
            self.deploy_jvm_run_script()

        ssh.disconnect()

    def is_jvm_run_script_deployed(self):
        # todo: does file exist
        return False

    def deploy_jvm_run_script(self):
        self.artifact_host.get_reference_artifact()
