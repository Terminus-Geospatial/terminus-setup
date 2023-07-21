#!/bin/bash
#    File:    check_all_repos_for_diffs.bash
#    Author:  Marvin Smith
#    Date:    7/16/2023
#

#------------------------------------------------#
#-          Check the repo for changes          -#
#------------------------------------------------#
function Check_Repo()
{
    repo_path="${1}"

    pushd ${repo_path}

    echo "Repo: `dirname .`"
    git status

    popd
}

terminus_base=$1

pushd ${terminus_base}

#-----------------------------#
#-      Check Each Repo      -#
#-----------------------------#
Check_Repo terminus-cmake
Check_Repo terminus-outcome
Check_Repo terminus-math
Check_Repo terminus-core
Check_Repo terminus-image
Check_Repo terminus-repo-utilities
Check_Repo terminus-warpcore-demos

