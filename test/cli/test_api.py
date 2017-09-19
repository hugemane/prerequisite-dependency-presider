from unittest import TestCase
import sys


class TestFile(TestCase):

    def test_api_jvmrunscript_args(self):
        import pdp.cli.api as api
        sys.argv[1:] = ['-dh', 'some.host.com',
                        '-du', 'ubuntu',
                        '-djrs', '/var/service/service-run.sh',
                        '-ah', 'archive.com',
                        '-au', 'archiver',
                        '-ajrs', '~/repo/scripts/jvm-run-script.sh',
                        '-jsn', 'name-service',
                        '-jjh', '/software/jdk',
                        '-jmm', '512mb',
                        '-jmc', 'me.hugemane.Main']

        options = api.get_api_args()

        self.assertEquals(options.deploy_host, 'some.host.com')
        self.assertEquals(options.deploy_host_user, 'ubuntu')
        self.assertEquals(options.deploy_jvm_run_script, '/var/service/service-run.sh')

        self.assertEquals(options.artifact_host, 'archive.com')
        self.assertEquals(options.artifact_host_user, 'archiver')
        self.assertEquals(options.artifact_jvm_run_script, '~/repo/scripts/jvm-run-script.sh')

        self.assertEquals(options.jvm_service_name, 'name-service')
        self.assertEquals(options.jvm_java_home, '/software/jdk')
        self.assertEquals(options.jvm_max_memory, '512mb')
        self.assertEquals(options.jvm_main_class, 'me.hugemane.Main')
