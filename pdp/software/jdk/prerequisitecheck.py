from pdp.utility.ssh import SSH, RemoteHost, SecureRemoteCopy


class JdkPrerequisite:
    deploy_ssh = None

    def __init__(self, user, host, pkey_file, artifact_host, options):
        self.user = user
        self.host = host
        self.pkey_file = pkey_file
        self.artifact_host = artifact_host
        self.options = options

        if None in (user, host, artifact_host, options):
            print('jdk prerequisite error - missing args')
            raise JdkPrerequisiteException()

        self.deploy_jdk_dir = self.options['deploy_jdk_dir']
        self.deploy_jdk_archive = self.options['deploy_jdk_archive']
        self.artifact_jdk_archive = self.options['artifact_jdk_archive']

    def check(self):
        self.deploy_ssh = SSH(self.user, self.host, key_file=self.pkey_file)
        self.deploy_ssh.connect()

        if self.is_jdk_deployed() is False:
            self.deploy_jdk()

        self.deploy_ssh.disconnect()

    def is_jdk_deployed(self):
        return self.deploy_ssh.does_dir_exist(self.deploy_jdk_dir)

    def deploy_jdk(self):
        self.remote_create_jdk_dir()
        self.remote_deploy_jdk_archive()
        self.remote_extract_jdk_software()
        self.remote_remove_jdk_archive()

    def remote_create_jdk_dir(self):
        self.deploy_ssh.execute_remote_command('mkdir -p ' + self.deploy_jdk_dir)

    def remote_deploy_jdk_archive(self):
        artifact_remote_host = RemoteHost(self.artifact_host.user, self.artifact_host.host)
        deploy_remote_host = RemoteHost(self.user, self.host)

        remote_copier = SecureRemoteCopy(artifact_remote_host, deploy_remote_host, self.pkey_file)
        remote_copier.copy_between_hosts(self.artifact_jdk_archive, self.deploy_jdk_archive)

    def remote_extract_jdk_software(self):
        extract_software_command = "tar -zxvf {0}".format(self.deploy_jdk_archive)

        if '/' in self.deploy_jdk_archive:
            deploy_jdk_archive_dir = self.deploy_jdk_archive[:self.deploy_jdk_archive.rindex('/')]
            deploy_jdk_archive_file = self.deploy_jdk_archive[self.deploy_jdk_archive.rindex('/')+1:]
            extract_software_command = "cd {0}; tar -zxvf {1}".format(deploy_jdk_archive_dir, deploy_jdk_archive_file)

        self.deploy_ssh.execute_remote_process_command(extract_software_command)

    def remote_remove_jdk_archive(self):
        delete_jdk_archive = "rm -f {0}".format(self.deploy_jdk_archive)
        self.deploy_ssh.execute_remote_process_command(delete_jdk_archive)


class JdkPrerequisiteException(Exception):
    pass
