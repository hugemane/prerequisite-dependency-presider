from pathlib import Path
from pdp.utility.ssh import SSH


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

        self.deploy_jar_lib_dir = self.options['deploy_jar_lib_dir']
        self.artifact_jar_lib_dep_file = self.options['artifact_jar_lib_dep_file']

    def check(self):
        self.deploy_ssh = SSH(self.user, self.host, key_file=self.pkey_file)
        self.deploy_ssh.connect()
        self.deploy_dependent_library_jars()
        self.deploy_ssh.disconnect()

    def deploy_dependent_library_jars(self):
        self.create_jar_dependency_library_dir()
        self.deploy_artifact_dependent_jar_libraries()

    def create_jar_dependency_library_dir(self):
        if self.deploy_ssh.does_file_exist(self.deploy_jar_lib_dir) is False:
            self.deploy_ssh.execute_remote_command('mkdir -p ' + self.deploy_jar_lib_dir)

    def deploy_artifact_dependent_jar_libraries(self):
        dependent_jar_libraries = self.artifact_dependent_jar_libraries()
        for dependent_jar_library in dependent_jar_libraries:
            self.deploy_dependent_jar_library(dependent_jar_library)

    def artifact_dependent_jar_libraries(self):
        pulled_artifact_file_contents = self.artifact_host.get_artifact_file_content(self.artifact_jar_lib_dep_file)
        return self.generate_artifact_jar_library_dependencies(pulled_artifact_file_contents)

    def generate_artifact_jar_library_dependencies(self, dep_jar_file_contents):
        if dep_jar_file_contents is None:
            return []

        dep_jar_file_contents_cleaned = dep_jar_file_contents.replace('\r\n', '\n').replace(' ', '')
        dep_jar_file_lines = dep_jar_file_contents_cleaned.split('\n')

        for dep_jar_line in dep_jar_file_lines:
            values = dep_jar_line.split(',')
            artifact_file = values[0]
            artifact_full_path = self.homeize_file_path(values[1])
            yield [artifact_file, artifact_full_path]

    def homeize_file_path(self, file_path):
        if file_path.find("~/") == -1:
            return file_path
        home = str(Path.home())
        return home + file_path[1:]

    def deploy_dependent_jar_library(self, dependent_jar_lib):
        dependent_jar_lib_file = dependent_jar_lib[0]
        artifact_dependent_jar_path = dependent_jar_lib[1]
        deploy_dependent_jar_path = "{0}/{1}".format(self.deploy_jar_lib_dir, dependent_jar_lib_file)

        if self.is_jar_deployed(deploy_dependent_jar_path) is False:
            self.remote_deploy_dependent_jar_library(artifact_dependent_jar_path, deploy_dependent_jar_path)

    def is_jar_deployed(self, jar_library_path):
        return self.deploy_ssh.does_file_exist(jar_library_path)

    def remote_deploy_dependent_jar_library(self, dependent_jar, deploy_dependent_jar):
        # deploy from local machine -> remote machine
        self.deploy_ssh.push_file(dependent_jar, deploy_dependent_jar)


class JarLibraryPrerequisiteException(Exception):
    pass
