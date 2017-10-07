from pathlib import Path
from pdp.utility.ssh import SSH, RemoteHost, SecureRemoteCopy


class JarLibrariesPrerequisite:
    deploy_ssh = None

    def __init__(self, user, host, pkey_file, artifact_host, options):
        self.user = user
        self.host = host
        self.pkey_file = pkey_file
        self.artifact_host = artifact_host
        self.options = options

        if None in (user, host, artifact_host, options):
            print('jar library prerequisite error - missing args')
            raise JarLibraryPrerequisiteException()

        self.deploy_jar_lib_dir = self.options.get('deploy_jar_lib_dir')
        self.artifact_jar_lib_dep_file = self.options.get('artifact_jar_lib_dep_file')
        self.force_deploy_organisation = self.options.get('force_deploy_organisation')

    def check(self):
        self.deploy_ssh = SSH(self.user, self.host, key_file=self.pkey_file)
        self.deploy_ssh.connect()
        self.deploy_dependent_library_jars()
        self.deploy_ssh.disconnect()

    def deploy_dependent_library_jars(self):
        self.create_jar_dependency_library_dir()
        dependent_jar_libraries = list(self.artifact_dependent_jar_libraries())
        self.publish_jar_libraries_to_artifact_host(dependent_jar_libraries)
        self.deploy_artifact_dependent_jar_libraries(dependent_jar_libraries)

    def create_jar_dependency_library_dir(self):
        if self.deploy_ssh.does_file_exist(self.deploy_jar_lib_dir) is False:
            self.deploy_ssh.execute_remote_command('mkdir -p ' + self.deploy_jar_lib_dir)

    def publish_jar_libraries_to_artifact_host(self, dependent_jar_libraries):
        for dependent_jar_library in dependent_jar_libraries:
            self.publish_dependent_jar_library_to_artifact_host(dependent_jar_library)

    def publish_dependent_jar_library_to_artifact_host(self, dependent_jar_lib):
        source_jar_path = dependent_jar_lib[1]
        artifact_jar_path = dependent_jar_lib[2]
        self.artifact_host.publish_file(source_jar_path, artifact_jar_path)

    def deploy_artifact_dependent_jar_libraries(self, dependent_jar_libraries):
        for dependent_jar_library in dependent_jar_libraries:
            self.deploy_dependent_jar_library_from_artifact_host(dependent_jar_library)

    def artifact_dependent_jar_libraries(self):
        pulled_artifact_file_contents = self.artifact_host.get_artifact_file_content(self.artifact_jar_lib_dep_file)
        return self.generate_artifact_jar_library_dependencies(pulled_artifact_file_contents)

    def generate_artifact_jar_library_dependencies(self, dep_jar_file_contents):
        if dep_jar_file_contents is None:
            return []

        dep_jar_file_contents_cleaned = dep_jar_file_contents.replace('\r\n', '\n').replace(' ', '')
        dep_jar_file_lines = dep_jar_file_contents_cleaned.split('\n')

        for dep_jar_line in dep_jar_file_lines:
            if len(dep_jar_line.strip()) > 0:
                values = dep_jar_line.split(',')
                artifact_file = values[0]
                artifact_source_path = self.homeize_file_path(values[1])
                artifact_file_path = values[2]
                yield [artifact_file, artifact_source_path, artifact_file_path]

    def homeize_file_path(self, file_path):
        if file_path.find("~/") == -1:
            return file_path
        home = str(Path.home())
        return home + file_path[1:]

    def deploy_dependent_jar_library_from_artifact_host(self, dependent_jar_lib):
        dependent_jar_lib_file = dependent_jar_lib[0]
        artifact_jar_path = dependent_jar_lib[2]
        deploy_dependent_jar_path = "{0}/{1}".format(self.deploy_jar_lib_dir, dependent_jar_lib_file)

        # always deploy artifacts from organisation (if specified)
        if self.force_deploy_organisation is not None and artifact_jar_path.find(self.force_deploy_organisation) >= 0:
            self.remote_deploy_dependent_jar_library(artifact_jar_path, deploy_dependent_jar_path)

        if self.is_jar_deployed(deploy_dependent_jar_path) is False:
            self.remote_deploy_dependent_jar_library(artifact_jar_path, deploy_dependent_jar_path)

    def is_jar_deployed(self, jar_library_path):
        return self.deploy_ssh.does_file_exist(jar_library_path)

    def remote_deploy_dependent_jar_library(self, artifact_jar_path, deploy_jar_path):
        # deploy from artifact machine -> remote machine (using same key i.e. host must be able to access both)
        artifact_remote_host = RemoteHost(self.artifact_host.user, self.artifact_host.host)
        deploy_remote_host = RemoteHost(self.user, self.host)

        remote_copier = SecureRemoteCopy(artifact_remote_host, deploy_remote_host, self.pkey_file)
        remote_copier.copy_between_hosts(artifact_jar_path, deploy_jar_path)


class JarLibraryPrerequisiteException(Exception):
    pass
