import unittest

from pdp.utility.file import File
from pdp.utility.ssh import SSH, SSHConnectException

"""
this is test should be done manually
replace these variables:
    test_user = '--your-remote-username--'
    test_host = '--your-remote-host--'
    test_remote_file = '--your-remote-file--'
"""


#@unittest.skip('configure user, host and remote file to test')
class TestSSH(unittest.TestCase):
    test_user = 'artifact'
    test_host = 'artifact.lxd'
    test_remote_file = '~/repo/script/jvm-run-script.sh'

    def test_connect(self):
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        self.assertTrue(ssh.is_connected())
        ssh.disconnect()

    def test_connect_raise_exception_when_host_keys_not_configured(self):
        ssh = SSH('unknown-user', self.test_host)
        with self.assertRaises(SSHConnectException):
            ssh.connect()

    def test_disconnect_should_not_fail_when_not_connected(self):
        ssh = SSH(self.test_user, self.test_host)
        self.assertFalse(ssh.is_connected())
        ssh.disconnect()

    def test_does_file_exist(self):
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        file_exists = ssh.does_file_exist(self.test_remote_file)
        ssh.disconnect()
        self.assertTrue(file_exists)

    def test_does_file_exist_not(self):
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        file_exists = ssh.does_file_exist(self.test_remote_file + '.not-found')
        ssh.disconnect()
        self.assertFalse(file_exists)

    def test_pull_file(self):
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        ssh.pull_file(self.test_remote_file, '/tmp/')
        ssh.disconnect()
        # verify file was copied
        local_copied_file = '/tmp/' + self.test_remote_file.split('/')[-1]
        file = File(local_copied_file)
        self.assertTrue(file.exists())

    def test_pull_file_contents(self):
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        file_content = ssh.pull_file_contents(self.test_remote_file)
        ssh.disconnect()
        self.assertGreater(len(file_content), 1)

    def test_push_file(self):
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        ssh.push_file('../template/jvm-run-script.sh', self.test_remote_file)
        # pull remote file contents for verification
        file_content = ssh.pull_file_contents(self.test_remote_file)
        ssh.disconnect()
        # verify file contents
        self.assertTrue('run script for service' in file_content)

    def test_push_file_contents(self):
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        ssh.push_file_contents(self.test_remote_file, 'test 1')
        file_content = ssh.pull_file_contents(self.test_remote_file)
        ssh.disconnect()
        self.assertTrue('test 1' in file_content)

    def test_push_file_contents_and_create_file_dir(self):
        new_remote_dir_file = '~/test/create/file.txt'
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        ssh.push_file_contents(new_remote_dir_file, 'test 2')
        # pull remote file contents for verification
        file_content = ssh.pull_file_contents(new_remote_dir_file)
        ssh.disconnect()
        self.assertTrue('test 2' in file_content)

