import argparse

from pdp.artifact.repository import ArtifactHost
from pdp.library.jar.prerequisitecheck import JarLibrariesPrerequisite
from pdp.script.jvm.prerequisitecheck import JvmRunScriptPrerequisite
from pdp.software.jdk.prerequisitecheck import JdkPrerequisite


def get_api_args(argv=None):
    parser = argparse.ArgumentParser(description='PDP - handles prerequisites')

    parser.add_argument('-d', '--debug', dest='debug', help='debug to help diagnose issues')

    parser.add_argument('-pk', '--private-key-file', dest='private_key_file', help='private key file for host connect')
    parser.add_argument('-dh', '--deploy-host', dest='deploy_host', help='deploy host')
    parser.add_argument('-du', '--deploy-host-user', dest='deploy_host_user', help='deploy host user')
    parser.add_argument('-djrs', '--deploy-jvm-run-script', dest='deploy_jvm_run_script', help='deploy jvm run script')

    parser.add_argument('-ah', '--artifact-host', dest='artifact_host', help='artifact host')
    parser.add_argument('-au', '--artifact-host-user', dest='artifact_host_user', help='artifact host user')

    parser.add_argument('-jrs', '--jvm-run-script', dest='jvm_run_script', help='artifact jvm run script')
    parser.add_argument('-jsn', '--jvm-service-name', dest='jvm_service_name', help='jvm service name')
    parser.add_argument('-jjh', '--jvm-java-home', dest='jvm_java_home', help='jvm java home')
    parser.add_argument('-jmm', '--jvm-max-memory', dest='jvm_max_memory', help='jvm max memory')
    parser.add_argument('-jmc', '--jvm-main-class', dest='jvm_main_class', help='jvm main class')
    parser.add_argument('-jsj', '--jvm_service_jar', dest='jvm_service_jar', help='jvm service jar')

    parser.add_argument('-dja', '--deploy_jdk_archive', dest='deploy_jdk_archive', help='deploy jdk archive')
    parser.add_argument('-djd', '--deploy_jdk_dir', dest='deploy_jdk_dir', help='deploy_jdk_dir')
    parser.add_argument('-aja', '--artifact_jdk_archive', dest='artifact_jdk_archive', help='artifact jdk archive')

    parser.add_argument('-djld', '--deploy_jar_lib_dir', dest='deploy_jar_lib_dir', help='deploy jar library dir')
    parser.add_argument('-ajldf', '--artifact_jar_lib_dep_file', dest='artifact_jar_lib_dep_file', help='artifact jar library dependency file')
    parser.add_argument('-fdo', '--force_deploy_organisation', dest='force_deploy_organisation', help='force deploy organisation depdendences')

    args = parser.parse_args(argv)

    if args.debug is not None:
        __debug_api_args(args)

    return args


def jvm_run_script_prerequisite_check():
    args = get_api_args()

    artifact_repo = ArtifactHost(args.artifact_host_user, args.artifact_host, args.private_key_file)

    jvm_script_options = {
        'artifact_jvm_script': args.jvm_run_script,
        'service_name': args.jvm_service_name,
        'java_home': args.jvm_java_home,
        'jvm_max_memory': args.jvm_max_memory,
        'java_main_class': args.jvm_main_class,
        'jvm_service_jar': args.jvm_service_jar
    }

    prerequisite = JvmRunScriptPrerequisite(args.deploy_host_user, args.deploy_host, args.private_key_file,
                                            args.deploy_jvm_run_script,
                                            artifact_repo,
                                            jvm_script_options)
    prerequisite.check()


def __debug_api_args(args):
    print('DEPLOYMENT HOST OPTIONS')
    print('private_key_file: ' + __debug_option(args.private_key_file))
    print('deploy_host: ' + __debug_option(args.deploy_host))
    print('deploy_host_user: ' + __debug_option(args.deploy_host_user))
    print('deploy_jvm_run_script: ' + __debug_option(args.deploy_jvm_run_script))
    print('')
    print('ARTIFACT HOST OPTIONS')
    print('artifact_host: ' + __debug_option(args.artifact_host))
    print('artifact_host_user: ' + __debug_option(args.artifact_host_user))
    print('')
    print('JVM RUN SCRIPT OPTIONS')
    print('jvm_run_script: ' + __debug_option(args.jvm_run_script))
    print('jvm_service_name: ' + __debug_option(args.jvm_service_name))
    print('jvm_java_home: ' + __debug_option(args.jvm_java_home))
    print('jvm_max_memory: ' + __debug_option(args.jvm_max_memory))
    print('jvm_main_class: ' + __debug_option(args.jvm_main_class))
    print('jvm_service_jar: ' + __debug_option(args.jvm_service_jar))
    print('')
    print('JDK SOFTWARE OPTIONS')
    print('deploy_jdk_archive: ' + __debug_option(args.deploy_jdk_archive))
    print('deploy_jdk_dir: ' + __debug_option(args.deploy_jdk_dir))
    print('artifact_jdk_archive: ' + __debug_option(args.artifact_jdk_archive))
    print('')
    print('DEPENDENT JAR LIBRARIES OPTIONS')
    print('deploy_jar_lib_dir: ' + __debug_option(args.deploy_jar_lib_dir))
    print('artifact_jar_lib_dep_file: ' + __debug_option(args.artifact_jar_lib_dep_file))
    print('force_deploy_organisation: ' + __debug_option(args.force_deploy_organisation))


def __debug_option(option):
    return '!! NOT SET !!' if option is None else option


def jdk_prerequisite_check():
    args = get_api_args()

    artifact_repo = ArtifactHost(args.artifact_host_user, args.artifact_host, args.private_key_file)

    jdk_options = {
        'deploy_jdk_archive': args.deploy_jdk_archive,
        'deploy_jdk_dir': args.deploy_jdk_dir,
        'artifact_jdk_archive': args.artifact_jdk_archive
    }

    prerequisite = JdkPrerequisite(args.deploy_host_user, args.deploy_host, args.private_key_file,
                                   artifact_repo,
                                   jdk_options)
    prerequisite.check()


def dependent_jar_libraries_check():
    args = get_api_args()

    artifact_repo = ArtifactHost(args.artifact_host_user, args.artifact_host, args.private_key_file)

    jar_libraries_options = {
        'deploy_jar_lib_dir': args.deploy_jar_lib_dir,
        'artifact_jar_lib_dep_file': args.artifact_jar_lib_dep_file,
        'force_deploy_organisation': args.force_deploy_organisation,
    }

    prerequisite = JarLibrariesPrerequisite(args.deploy_host_user, args.deploy_host, args.private_key_file,
                                            artifact_repo,
                                            jar_libraries_options)
    prerequisite.check()
