# prerequisite-dependency-presider
PDP - Prerequisite Dependency Presider

# Goal
When deploying micro-services, these services could depend on various dependencies.
Dependencies could be run script, database, cache, other services or libraries.

The general idea is to be efficient with resources. For example when in road warrior location where there is much to be
desired internet connection, deploying bloated services might not be a viable option.

# Deployment Concerns

## Run Script
To start/stop service, this could employ a run script. This run script could be specified as LATEST or specific version.
PDP will check to see if the run script exists, if not deploy the appropriate required version.

## Dependent Libraries
When service depends on multiple libraries, PDP will purge non-required libs and deploy libs that have not
already been deployed on the server. In the same context where no libs have been deployed, all these shall be deployed.

## Dependent Environment Infrastructure
Databases, caches or dependent services that are required for the service to run. PDP will check if these are available.
When these are not, PDP will halt service starting until these are available.

# Install
## Local install (without PiPy)
```
tar --exclude='*.iml' --exclude='./.idea' --exclude='./.git' --exclude='./.gitignore' --exclude='./test' -cvzf /tmp/pdp-0.0.1.tar.gz .
sudo pip3 install /tmp/pdp.tar
```
