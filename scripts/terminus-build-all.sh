#!/usr/bin/env bash
#
#    File:    conan-build-all.sh
#    Author:  Marvin Smith
#    Date:    7/21/2023
#

set -e

#  Terminus root
pushd ~/Desktop/Projects/terminus

#  Terminus CMake
pushd terminus-cmake
conan-build.sh -B
popd

#  Terminus Math
pushd terminus-math
conan-build.sh -B
popd

#  Terminus Log
pushd terminus-log
conan-build.sh -B
popd

#  Terminus Outcome
pushd terminus-outcome
conan-build.sh -B
popd

#  Terminus Core
pushd terminus-core
conan-build.sh -B
popd
