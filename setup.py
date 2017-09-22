from distutils.core import setup

setup(
    name = 'pdp',
    packages = ['pdp', 'pdp.artifact', 'pdp.cli', 'pdp.script', 'pdp.script.jvm', 'pdp.utility'],
    version = '0.0.1',
    description = 'PDP - Prerequisite Dependency Presider, helps your deployed code control its dependencies',
    author = 'hugemane',
    url = 'https://github.com/hugemane/prerequisite-dependency-presider',
    keywords = ['pdp', 'prerequisite', 'dependency'],
    classifiers = [],
    entry_points = {
        'console_scripts':
            ['jvm-run-script-prerequisite=pdp.cli.api:jvm_run_script_prerequisite_check'],
    }, requires=['paramiko', 'scp']
)
