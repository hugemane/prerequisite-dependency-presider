from unittest import TestCase


class TestFile(TestCase):

    def test_exists(self):
        from pdp.artifact.repository import ArtifactHost
        artifact_host = ArtifactHost('artifact', 'apache.lxd')
        script_content = artifact_host.get_artifact_file_content('~/repo/script/jvm-run-script.sh')
        print('got it!')
        print(script_content)
        #self.assertTrue(file.exists())
