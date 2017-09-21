import unittest

from pdp.utility.filetemplate import FileTemplate


class TestFileTemplate(unittest.TestCase):
    def test_replace(self):
        file_template = FileTemplate('$something went to see a man about a horse')
        file_template.replace('something', 'I')
        result = file_template.contents()
        self.assertEqual(result, 'I went to see a man about a horse')

    def test_replace_multiple(self):
        file_template = FileTemplate('$something went to see $entity about a horse')
        file_template.replace('something', 'I')
        file_template.replace('entity', 'a man')
        result = file_template.contents()
        self.assertEqual(result, 'I went to see a man about a horse')

    def test_replace_multiple_same(self):
        file_template = FileTemplate('$something went to see $something about a horse')
        file_template.replace('something', 'I')
        result = file_template.contents()
        self.assertEqual(result, 'I went to see I about a horse')

    def test_replace_with_dict(self):
        values = {'something': 'I', 'entity': 'a man'}
        file_template = FileTemplate('$something went to see $entity about a horse')
        file_template.replace_with_values('something', values)
        file_template.replace_with_values('entity', values)
        result = file_template.contents()
        self.assertEqual(result, 'I went to see a man about a horse')
