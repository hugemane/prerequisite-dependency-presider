import unittest

from pdp.artifact.repository import ArtifactHost

"""
this is test should be done manually
replace these variables:
    test_deploy_user = '--your-deploy-host-username--'
    test_deploy_host = '--your-deploy-host--'
    test_deploy_jvm_script_file = '--your-deploy-file--'
    test_artifact_host = configure artifact host
    test_artifact_jvm_script = '--artifact-script-file--'
"""


@unittest.skip('configure user, host and remote file to test')
class TestJvmRunScriptPrerequisite(unittest.TestCase):
    test_deploy_user = 'ubuntu'
    test_deploy_host = 'service-setting.lxd'
    test_deploy_jvm_script_file = '~/service/service-run.sh'

    test_artifact_host = ArtifactHost('artifact', 'artifact.lxd')

    test_artifact_jvm_script = '~/repo/script/jvm-run-script.sh'

    def test_check_should_deploy_jvm_run_script(self):
        from pdp.script.jvm.prerequisitecheck import JvmRunScriptPrerequisite
        prerequisite = JvmRunScriptPrerequisite(self.test_deploy_user, self.test_deploy_host,
                                                self.test_deploy_jvm_script_file,
                                                self.test_artifact_host,
                                                self.test_artifact_jvm_script)
        prerequisite.check()
        # todo: complete
