import unittest

from pdp.artifact.repository import ArtifactHost
from pdp.script.jvm.prerequisitecheck import JvmRunScriptPrerequisite, JvmRunScriptPrerequisiteException

"""
this is test and should be run manually
"""


class TestJvmRunScriptPrerequisite(unittest.TestCase):

    def test_check_should_raise_exception_when_some_args_missing(self):
        with self.assertRaises(JvmRunScriptPrerequisiteException):
            prerequisite = JvmRunScriptPrerequisite('user', 'host', '~/service/service-run.sh', None, None)
            prerequisite.check()

    def test_check_should_deploy_jvm_run_script(self):
        artifact_host = ArtifactHost('artifact', 'artifact.lxd')

        options = {
            'artifact_jvm_script': '~/repo/script/jvm-run-script.sh',
            'service_name': 'setting-service',
            'java_home': '/var/lib/java',
            'jvm_max_memory': '512mb',
            'java_main_class': 'com.hugemane.service.Main'
        }

        prerequisite = JvmRunScriptPrerequisite('ubuntu', 'service-setting.lxd',
                                                '~/service/service-run.sh',
                                                artifact_host,
                                                options)
        prerequisite.check()
