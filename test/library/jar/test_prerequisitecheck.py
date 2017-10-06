import unittest

from pdp.artifact.repository import ArtifactHost
from pdp.library.jar.prerequisitecheck import JarLibraryPrerequisiteException, JarLibrariesPrerequisite
from pdp.utility.file import File


class TestJarLibrariesPrerequisite(unittest.TestCase):

    def test_check_should_raise_exception_when_some_args_missing(self):
        with self.assertRaises(JarLibraryPrerequisiteException):
            prerequisite = JarLibrariesPrerequisite('user', 'host', None, None, None)
            prerequisite.check()

    def test_generate_artifact_jar_library_dependency_file_jars_should_return_empty_result_when_no_deps_available(self):
        artifact_host = ArtifactHost('artifact', 'artifact.lxd')
        options = {
            'deploy_jar_lib_dir': '--some-remote-deployment-lib-dir--',
            'artifact_jar_lib_dep_file': '--some-artifact-jar-lib-dep-file--'
        }
        prerequisite = JarLibrariesPrerequisite('--deploy-user--', '--deploy-host--',
                                                '--your-private-key', artifact_host, options)

        dep_jar_file_contents = None

        lib_dependency_jars = prerequisite.generate_artifact_jar_library_dependencies(dep_jar_file_contents)
        self.assertEqual(len(list(lib_dependency_jars)), 0)

    def test_generate_artifact_jar_library_dependency_file_jars_as_iterable_jar_dependencies(self):
        artifact_host = ArtifactHost('artifact', 'artifact.lxd')
        options = {
            'deploy_jar_lib_dir': '--some-remote-deployment-lib-dir--',
            'artifact_jar_lib_dep_file': '--some-artifact-jar-lib-dep-file--'
        }
        prerequisite = JarLibrariesPrerequisite('--deploy-user--', '--deploy-host--',
                                                '--your-private-key', artifact_host, options)

        file = File('../../test-resources/prerequisite-libs_2.12.txt')
        dep_jar_file_contents = file.read()

        lib_dependency_jars = prerequisite.generate_artifact_jar_library_dependencies(dep_jar_file_contents)

        top_dep_library_jar = next(lib_dependency_jars)
        last_dep_library_jar = list(lib_dependency_jars)[-1]

        self.assertEqual(top_dep_library_jar[0], 'scala-library-2.12.2.jar')
        self.assertEqual(top_dep_library_jar[1], '/home/hugemane/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.2.jar')

        self.assertEqual(last_dep_library_jar[0], 'scalaj-http_2.12-2.3.0.jar')
        self.assertEqual(last_dep_library_jar[1], '/home/hugemane/.ivy2/cache/org.scalaj/scalaj-http_2.12/jars/scalaj-http_2.12-2.3.0.jar')

    def test_generate_artifact_jar_library_dependency_file_jars_as_iterable_jar_dependencies_with_full_path(self):
        artifact_host = ArtifactHost('artifact', 'artifact.lxd')
        options = {
            'deploy_jar_lib_dir': '--some-remote-deployment-lib-dir--',
            'artifact_jar_lib_dep_file': '--some-artifact-jar-lib-dep-file--'
        }
        prerequisite = JarLibrariesPrerequisite('--deploy-user--', '--deploy-host--',
                                                '--your-private-key', artifact_host, options)

        file = File('../../test-resources/local-home-prerequisite-libs_2.12.txt')
        dep_jar_file_contents = file.read()

        lib_dependency_jars = prerequisite.generate_artifact_jar_library_dependencies(dep_jar_file_contents)

        top_dep_library_jar = next(lib_dependency_jars)
        last_dep_library_jar = list(lib_dependency_jars)[-1]

        self.assertEqual(top_dep_library_jar[0], 'scala-library-2.12.2.jar')
        self.assertEqual(top_dep_library_jar[1], '/home/hugemane/.ivy2/cache/org.scala-lang/scala-library/jars/scala-library-2.12.2.jar')

        self.assertEqual(last_dep_library_jar[0], 'scalaj-http_2.12-2.3.0.jar')
        self.assertEqual(last_dep_library_jar[1], '/home/hugemane/.ivy2/cache/org.scalaj/scalaj-http_2.12/jars/scalaj-http_2.12-2.3.0.jar')

    """
    this is test and should be run manually
    """
    def test_check_should_deploy_dependent_library_jars(self):
        artifact_host = ArtifactHost('artifact', 'artifact.lxd')

        options = {
            'deploy_jar_lib_dir': '/home/ubuntu/service/lib',
            'artifact_jar_lib_dep_file': '--local-ivy-file--/0.0.1-SNAPSHOT/prerequisites/prerequisite-libs_2.12.txt'
        }

        prerequisite = JarLibrariesPrerequisite('ubuntu', 'service-setting.lxd',
                                                '--your-private-key--',
                                                artifact_host,
                                                options)
        prerequisite.check()
