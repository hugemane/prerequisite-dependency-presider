from unittest import TestCase


class TestFile(TestCase):

    def test_exists(self):
        from pdp.artifact.repository import ArtifactHost
        artifact_host = ArtifactHost('artifact', 'artifact.lxd')
        script_content = artifact_host.get_artifact_file_content('~/repo/script/jvm-run-script.sh')
        self.assertTrue(len(script_content) > 0)
