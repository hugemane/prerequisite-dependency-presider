import os

"""
File - designed to be used with small text files.
Remote deployment config, updating, etc.
"""


class File:
    def __init__(self, file_path):
        self.file_path = file_path

    def exists(self):
        return os.path.isfile(self.file_path)

    def read(self):
        with open(self.file_path, 'r') as content_file:
            return content_file.read()

    def write(self, file_content):
        f = open(self.file_path, 'wt', encoding='utf-8')
        f.write(file_content)
        f.close()

    def write_lines(self, file_lines):
        file_content = ''.join(file_lines)
        self.write(file_content)
