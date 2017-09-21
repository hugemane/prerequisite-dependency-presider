import unittest

from pdp.artifact.repository import ArtifactHost

"""
this is test should be done manually
"""


class TestJvmRunScriptPrerequisite(unittest.TestCase):
    def test_check_should_deploy_jvm_run_script(self):
        from pdp.script.jvm.prerequisitecheck import JvmRunScriptPrerequisite

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
