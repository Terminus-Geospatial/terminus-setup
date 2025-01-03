#!/bin/sh
#
############################# INTELLECTUAL PROPERTY RIGHTS #############################
##                                                                                    ##
##                           Copyright (c) 2024 Terminus LLC                          ##
##                                All Rights Reserved.                                ##
##                                                                                    ##
##          Use of this source code is governed by LICENSE in the repo root.          ##
##                                                                                    ##
############################# INTELLECTUAL PROPERTY RIGHTS #############################
#
#    File:    conan-utils.bash
#    Author:  Marvin Smith
#    Date:    7/5/2023
#
#    Purpose:  Helper functions for working with Conan in the Integrated Build Process.
#

#  Returns the branch name, either from querying git or from an environment variable.
#  This returns the full branch name.  When running in Jenkins, branch names look like
#      "remotes/origin/hello-world"
#
#  This function will query git directly to get the branch name.  If this fails, just
#  set ${GET_BRANCH} env variable, as Jenkins will often do.
function getFullGitBranchNameFunc() {
    if [[ -z "${GIT_BRANCH}" ]]; then
        local git_ver_available=$(git --version | awk '{print $3}')
        local git_ver_needed="2.22.0"
        local git_ver_newer="$(echo -e "$git_ver_available\n$git_ver_needed" | sort -V | tail -1)"
        if [ "$git_ver_newer" == "$git_ver_available" ]; then
            git branch --show-current
        else
            git name-rev --name-only HEAD
        fi
    else
        echo ${GIT_BRANCH}
    fi
}

# Extracts the app/library name from a Conan recipe.
#
#  Optionally takes a single argument that is the path to a `conanfile.py` or a
#   directory containing one.  If no argument is provided, the function assumes the
#   conanfile.py` exists in the current directory.
function getAppNameFromConanfileFunc() {
    local conanfile="$(realpath "${1:-conanfile.py}")"
    if command -v conan > /dev/null ; then
        conan inspect $conanfile | grep 'name:' | awk '{print $2}'
    else
        cat ${conanfile} | grep 'name = ' | cut -d '"' -f 2
    fi
}

#  Extracts the app/library version from a Conan recipe
#
#  Optionally takes a single argument that is the path to a `conanfile.py` or a
#   directory containing one.  If no argument is provided, the function assumes the
#   conanfile.py` exists in the current directory.
function getAppVersionFromConanfileFunc() {
    local conanfile="$(realpath "${1:-conanfile.py}")"
    if command -v conan > /dev/null ; then
        conan inspect $conanfile | grep 'version:' | awk '{print $2}'
    else
        cat ${conanfile} | grep 'version = ' | cut -d '"' -f 2
    fi
}