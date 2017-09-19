import unittest
from unittest import TestCase


@unittest.skip('configure user, host and remote file to test')
class TestSSH(TestCase):
    test_user = '--your-user--'
    test_host = '--your-host--'
    test_remote_file = '--your-remote-file--'

    def test_connect(self):
        from pdp.utility.ssh import SSH
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        self.assertTrue(ssh.is_connected())
        ssh.disconnect()

    def test_disconnect_should_not_fail_when_not_connected(self):
        from pdp.utility.ssh import SSH
        ssh = SSH(self.test_user, self.test_host)
        self.assertFalse(ssh.is_connected())
        ssh.disconnect()

    def test_copy_file(self):
        from pdp.utility.ssh import SSH
        ssh = SSH(self.test_user, self.test_host)
        ssh.connect()
        ssh.pull_file(self.test_remote_file, '/tmp/')
        ssh.disconnect()
        # verify file was copied
        from pdp.utility.file import File
        local_copied_file = '/tmp/' + self.test_remote_file.split('/')[-1]
        file = File(local_copied_file)
        self.assertTrue(file.exists())

