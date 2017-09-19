from distutils.core import setup

setup(
    name = 'pdp',
    packages = ['pdp', 'pdp.script', 'pdp.utility'],
    version = '0.0.1',
    description = 'PDP - Prerequisite Dependency Presider, helps your service/code/project have its dependencies',
    author = 'hugemane',
    url = 'https://github.com/hugemane/prerequisite-dependency-presider',
    keywords = ['pdp', 'prerequisite', 'dependency'],
    classifiers = [],
    entry_points = {
        'console_scripts':
            ['jvmRunScript-prerequisite=pdp.script.jvmRunScript:main',
             'huge-prerequisite=pdp.script.jvmRunScript:huge_main'],
    }, requires=['paramiko', 'scp']
)
