import argparse

from pdp.artifact.repository import ArtifactHost
from pdp.script.jvm.prerequisitecheck import JvmRunScriptPrerequisite


def get_api_args(argv=None):
    parser = argparse.ArgumentParser(description='PDP - handles prerequisites')

    parser.add_argument('-dh', '--deploy-host', dest='deploy_host', help='deploy host')
    parser.add_argument('-du', '--deploy-host-user', dest='deploy_host_user', help='deploy host user')
    parser.add_argument('-djrs', '--deploy-jvm-run-script', dest='deploy_jvm_run_script', help='deploy jvm run script')

    parser.add_argument('-ah', '--artifact-host', dest='artifact_host', help='artifact host')
    parser.add_argument('-au', '--artifact-host-user', dest='artifact_host_user', help='artifact host user')
    parser.add_argument('-ajrs', '--artifact-jvm-run-script', dest='artifact_jvm_run_script', help='artifact jvm run script')

    parser.add_argument('-jsn', '--jvm-service-name', dest='jvm_service_name', help='jvm service name')
    parser.add_argument('-jjh', '--jvm-java-home', dest='jvm_java_home', help='jvm java home')
    parser.add_argument('-jmm', '--jvm-max-memory', dest='jvm_max_memory', help='jvm max memory')
    parser.add_argument('-jmc', '--jvm-main-class', dest='jvm_main_class', help='jvm main class')

    args = parser.parse_args(argv)

    return args

def jvm_run_script_prerequisite_check():
    args = get_api_args()

    artifact_repo = ArtifactHost(args.artifact_host_user, args.artifact_host)

    prerequisite = JvmRunScriptPrerequisite(args.deploy_host_user, args.deploy_host, args.deploy_jvm_run_script,
                                            artifact_repo, args.artifact_jvm_run_script)
    prerequisite.check()

