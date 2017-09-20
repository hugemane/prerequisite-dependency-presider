from unittest import TestCase


class TestFile(TestCase):

    def test_exists(self):
        from pdp.utility.file import File
        file = File('../template/jvm-run-script.sh')
        self.assertTrue(file.exists())

    def test_read(self):
        from pdp.utility.file import File
        file = File('../template/jvm-run-script.sh')
        file_content = file.read()
        self.assertTrue("exit 0" in file_content)

    def test_write(self):
        from pdp.utility.file import File
        test_file_path = '/tmp/test-file.txt'
        file = File(test_file_path)
        content = 'testing'
        file.write(content)
        # verify the file contents
        verify_file = File(test_file_path)
        self.assertTrue(verify_file.exists())
        file_content = verify_file.read()
        self.assertTrue(content in file_content)

    def test_write_lines(self):
        from pdp.utility.file import File
        test_file_path = '/tmp/test-line-file.txt'
        file = File(test_file_path)
        lines = ['the cat in the hat\r\n', 'is back\r\n', 'the end\r\n', '\r\n']
        file.write_lines(lines)
        # verify the file contents
        verify_file = File(test_file_path)
        self.assertTrue(verify_file.exists())
        file_content = verify_file.read()
        self.assertTrue('the cat in the hat' in file_content)
        self.assertTrue('the end' in file_content)
