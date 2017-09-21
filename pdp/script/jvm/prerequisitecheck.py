from pdp.utility.filetemplate import FileTemplate
from pdp.utility.ssh import SSH


class JvmRunScriptPrerequisite:
    deploy_ssh = None

    def __init__(self, user, host, deploy_run_script, artifact_host, options):
        self.user = user
        self.host = host
        self.deploy_run_script = deploy_run_script
        self.artifact_host = artifact_host
        self.options = options

    def check(self):
        self.deploy_ssh = SSH(self.user, self.host)
        self.deploy_ssh.connect()

        if self.is_jvm_run_script_deployed() is False:
            self.deploy_jvm_run_script()

        self.deploy_ssh.disconnect()

    def is_jvm_run_script_deployed(self):
        return self.deploy_ssh.does_file_exist(self.deploy_run_script)

    def deploy_jvm_run_script(self):
        pulled_file_contents = self.artifact_host.get_artifact_file_content(self.options['artifact_jvm_script'])

        script_template = FileTemplate(pulled_file_contents)
        script_template.replace_with_values('service_name', self.options)
        script_template.replace_with_values('java_home', self.options)
        script_template.replace_with_values('jvm_max_memory', self.options)
        script_template.replace_with_values('java_main_class', self.options)

        jvm_script_content = script_template.contents()

        print('pushing (a)' + jvm_script_content)

        #todo: push the file contents -> remote server

        #pf.write(replaced_file_contents)

        # deploy the updated file to host
        #self.deploy_ssh.push_file(pulled_file, self.deploy_run_script)
