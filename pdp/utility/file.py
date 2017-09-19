import os


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
