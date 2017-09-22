from unittest import TestCase
import sys


class TestFile(TestCase):

    def test_api_jvmrunscript_args(self):
        import pdp.cli.api as api
        sys.argv[1:] = ['-pk', '/home/hugemane/.ssh/test_nopass_rsa',
                        '-dh', 'some.host.com',
                        '-du', 'ubuntu',
                        '-djrs', '/var/service/service-run.sh',
                        '-ah', 'archive.com',
                        '-au', 'archiver',
                        '-jrs', '~/repo/scripts/jvm-run-script.sh',
                        '-jsn', 'name-service',
                        '-jjh', '/software/jdk',
                        '-jmm', '512mb',
                        '-jmc', 'me.hugemane.Main']

        options = api.get_api_args()

        self.assertEqual(options.private_key_file, '/home/hugemane/.ssh/test_nopass_rsa')
        self.assertEqual(options.deploy_host, 'some.host.com')
        self.assertEqual(options.deploy_host_user, 'ubuntu')
        self.assertEqual(options.deploy_jvm_run_script, '/var/service/service-run.sh')

        self.assertEqual(options.artifact_host, 'archive.com')
        self.assertEqual(options.artifact_host_user, 'archiver')

        self.assertEqual(options.jvm_run_script, '~/repo/scripts/jvm-run-script.sh')
        self.assertEqual(options.jvm_service_name, 'name-service')
        self.assertEqual(options.jvm_java_home, '/software/jdk')
        self.assertEqual(options.jvm_max_memory, '512mb')
        self.assertEqual(options.jvm_main_class, 'me.hugemane.Main')

    def test_api_debug(self):
        from io import StringIO
        sys.stdout = stdout_capture = StringIO()

        import pdp.cli.api as api
        sys.argv[1:] = ['-d', 'yes', '-dh', 'some.host.com', '-du', 'ubuntu']

        api.get_api_args()

        expected = 'DEPLOYMENT HOST OPTIONS\n' \
                   'private_key_file: !! NOT SET !!\n' \
                   'deploy_host: some.host.com\n' \
                   'deploy_host_user: ubuntu\n' \
                   'deploy_jvm_run_script: !! NOT SET !!\n' \
                   '\n' \
                   'ARTIFACT HOST OPTIONS\n' \
                   'artifact_host: !! NOT SET !!\n' \
                   'artifact_host_user: !! NOT SET !!\n' \
                   '\n' \
                   'JVM RUN SCRIPT OPTIONS\n' \
                   'jvm_run_script: !! NOT SET !!\n' \
                   'jvm_service_name: !! NOT SET !!\n' \
                   'jvm_java_home: !! NOT SET !!\n' \
                   'jvm_max_memory: !! NOT SET !!\n' \
                   'jvm_main_class: !! NOT SET !!\n'

        self.assertEqual(stdout_capture.getvalue(), expected)
