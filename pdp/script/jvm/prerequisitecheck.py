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
        print('checking if jvm run script is deployed...')
        return self.deploy_ssh.does_file_exist(self.deploy_run_script)

    def deploy_jvm_run_script(self):
        print('deploying jvm run script!!!!')

        pulled_file_contents = self.artifact_host.get_artifact_file_content(self.artifact_run_script)

        # replace the file contents
        # todo: where to get the values?
        replaced_file_contents = pulled_file_contents

        #todo: push the file contents -> remote server

        #pf.write(replaced_file_contents)

        # deploy the updated file to host
        #self.deploy_ssh.push_file(pulled_file, self.deploy_run_script)
