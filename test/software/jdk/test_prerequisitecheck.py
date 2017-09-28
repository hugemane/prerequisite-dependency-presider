import unittest

from pdp.artifact.repository import ArtifactHost
from pdp.software.jdk.prerequisitecheck import JdkPrerequisite, JdkPrerequisiteException

"""
this is test and should be run manually
"""


class TestJdkPrerequisite(unittest.TestCase):

    def test_check_should_raise_exception_when_some_args_missing(self):
        with self.assertRaises(JdkPrerequisiteException):
            prerequisite = JdkPrerequisite('user', 'host', None, None, None)
            prerequisite.check()

    def test_check_should_deploy_jdk(self):
        artifact_host = ArtifactHost('artifact', 'artifact.lxd')

        options = {
            'deploy_jdk_archive': '/home/ubuntu/software/java/jdk-8u144-linux-x64.tar.gz',
            'deploy_jdk_dir': '/home/ubuntu/software/java/jdk1.8.0_144',
            'artifact_jdk_archive': '/home/artifact/repo/software/java/jdk-8u144-linux-x64.tar.gz'
        }

        prerequisite = JdkPrerequisite('ubuntu', 'service-setting.lxd',
                                       '--your private key--',
                                       artifact_host,
                                       options)
        prerequisite.check()
