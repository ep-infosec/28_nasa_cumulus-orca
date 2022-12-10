#!/bin/bash
## =============================================================================
## NAME: build_release_package.sh
##
##
## DESCRIPTION
## -----------------------------------------------------------------------------
## Builds the needed ORCA artifacts and creates a distribution zip file that
## includes the lambda (task) zip files, terraform modules, and supporting
## documentation for the release.
##
##
## ENVIRONMENT SETTINGS
## -----------------------------------------------------------------------------
## bamboo_RELEASE_FLAG (boolean) - Determines if the build should occur and be
##                                 released to GitHub release.
##
##
## USAGE
## -----------------------------------------------------------------------------
## bin/build_release_package.sh
##
## This must be called from the (root) git repo directory.
## =============================================================================
## Set this for Debugging only
#set -ex

## Make sure we are calling the script the correct way.
BASEDIR=$(dirname $0)
if [ "$BASEDIR" != "bin" ]; then
  >&2 echo "ERROR: This script must be called from the root directory of the repo [bin/build_release_package.sh]."
  exit 1
fi


## FUNCTIONS
## -----------------------------------------------------------------------------
function check_rc () {
  ## Checks the return code of call and if not equal to 0, emits an error and
  ## exits the script with a failure.
  COMMAND=$1

  echo "INFO: Running '$COMMAND' ..."

  $COMMAND
  let RC=$?

  if [ $RC -ne 0 ]; then
      >&2 echo "ERROR: '$COMMAND' failed with a return code of [$RC]!"
      exit 1
  fi
}


## MAIN
## -----------------------------------------------------------------------------

# Remove the dist directory if it exists.
if [ -d dist ]; then
    check_rc "rm -rf dist"
fi

## Remove the build directory if it exists.
if [ -d build ]; then
    check_rc "rm -rf build"
fi

## Create the build directory
check_rc "mkdir -p build/tasks"


## Copy the static items that do not need to be built
# Terraform Module
check_rc "cp -r modules build"
check_rc "cp *.tf build"

# Documentation
check_rc "cp README.md build"
check_rc "cp LICENSE.txt build"


## Build the Lambdas and copy the zip file to the build directory
# Create the lambda zips
check_rc "bin/build_tasks.sh"

# Crawl through the zip files
##TODO: Do this a better way. Limit it to the task directory for zips
##      and exclude our shared python libraries
for package in $(find . -name *.zip);
do
  filename=$(basename $package)
  base="${filename%.*}"
  destination="build/tasks/$base/"
  check_rc "mkdir -p $destination"
  check_rc "cp -p $package $destination"
done


## Create the distribution package
check_rc "mkdir dist"

# Enter the build directory so the files that are zipped exist at the root level
echo "INFO: Creating distribution ..."
cd build
##TODO: Possibly send normal output to /dev/null and only capture error output
zip -qr "../dist/cumulus-orca-terraform.zip" .
let ZIP_RC=$?
cd -

if [ $ZIP_RC -ne 0 ]; then
    echo "ERROR: 'zip -r ../dist/cumulus-orca-terraform.zip' command failed with error code [$ZIP_RC]"
    exit 1
fi

## Validate that this build and release should occur
## Validate that the release flag is set
## TODO: Pull this code out as a separate step in Release area and use artifacts
##       instead of rebuilding the zip each time.
if [[ ! $bamboo_RELEASE_FLAG == true ]]; then
  >&2 echo "WARN: Skipping Release ORCA code step, PUBLISH_FLAG is [ $bamboo_RELEASE_FLAG ]"
  exit 0
fi

# Create the GitHub release
echo "INFO: Creating GitHub release ..."
check_rc "bin/create_release.sh"
