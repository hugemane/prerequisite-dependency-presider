from string import Template


class FileTemplate:

    def __init__(self, template_string):
        self.template_string = template_string

    def replace(self, template_key, value):
        template = Template(self.template_string)
        replacement = {template_key: value}
        self.template_string = template.safe_substitute(replacement)

    def replace_with_values(self, template_key, values):
        self.replace(template_key, values[template_key])

    def contents(self):
        return self.template_string


