#!/usr/bin/env bash
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

set -e

function usage() {
    echo "usage: ${0} <flags>"
    echo ''
    echo 'Installs the tools in this folder to your local workspace'
    echo 
    echo 'By default, the bashrc is modified.  Skip with flag outlined below.'
    echo
    echo '-h          : Print help menu'
    echo '--skip-shell : Do not update bashrc.  Just update scripts.'
    echo 
    echo 'Shell Options:  Default is whatever it finds on local system.'
    echo '--bash       : Update your ~/.bashrc'
    echo '--zsh        : Update your ~/.zshrc'
    echo
}

function update_shell() {

    SHELL_PATH="${1}"
    echo "Updating ${SHELL_PATH}"

    #  Check if ${HOME}/.local/bin is already on the system path
    if [[ ${PATH} =~ ^${HOME}/.local/bin:|:${HOME}/.local/bin:|:${HOME}/.local/bin$ ]]; then
        echo "${HOME}/.local/bin is already in path."
    else
        echo "${HOME}/.local/bin is not in path; adding"
        echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ${SHELL_PATH}
    fi

    #  Check if tmns-import is already defined
    if [ "`grep tmns-import ${SHELL_PATH}`" = '' ]; then 
        echo "tmns-import is not defined.  Adding to ${SHELL_PATH}"
        
        echo ''                                                          >> ${SHELL_PATH}
        echo '# Added by terminus-repo-utilities: install-local.bash'    >> ${SHELL_PATH}
        echo 'function tmns-import() {'                                  >> ${SHELL_PATH}
        echo '   source ${HOME}/.local/bin/tmns_bash_aliases.bash'       >> ${SHELL_PATH}
        echo '}'                                                         >> ${SHELL_PATH}
    else
        echo 'tmns-import already defined. skipping'
    fi
}

function check_if_conan_installed() {

    if [ "$(which conan)" == '' ]; then 
        echo '1'
    fi
    echo '0'
}

#  Setup logging
# Bring the required utilities into scope
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)/utils"
source "${SCRIPT_DIR}/log.bash"

#  Flag to skip using BASH 
SKIP_BASH=0
SHELL_LIST=()

#  Iterate over arguments
while [ -n "${1}" ]; do
    case "${1}" in

        #  Print usage instructions
        -h)
            usage
            ;;
        
        #  Prevent updating the bashrc
        --skip-shell)
            SKIP_BASH=1
            ;;

        #  Use bash
        --bash)
            SHELL_LIST+=("${HOME}/.bashrc")
            ;;
        
        #  Use zsh
        --zsh)
            SHELL_LIST+=("${HOME}/.zshrc")
            ;;

        *)
            echo "Unsupported flag: ${1}"
            exit 1
    esac
    shift
done

#------------------------------------------------#
#-          Check if Conan Installed            -#
#------------------------------------------------#
if [ "$(check_if_conan_installed)" == '0' ]; then
    log_debug "conan found at `which conan`"
else
    log_error "conan is not installed. Setup Virtual Environment immediately."
fi

SHELL_PATHS=()

#  Resolve which shells to use
if [ "${#SHELL_LIST[@]}" == '0' ]; then
    log_info 'No shells defined, looking for installed options.'

    SHELLS_TO_TEST=("${HOME}/.zshrc" "${HOME}/.bashrc")
    for SHELL_TO_TEST in "${SHELLS_TO_TEST[@]}"; do 
        if [ -e "${SHELL_TO_TEST}" ]; then
            log_debug "Adding: ${SHELL_TO_TEST}"
            SHELL_PATHS+=("${SHELL_TO_TEST}")
        fi
    done
fi


#  Get the path of this folder
SPATH="`dirname ${0}`"

#  Create destination and install files there
mkdir -p ${HOME}/.local/bin
rsync -avP ${SPATH}/utils/ ${HOME}/.local/bin/

#  Update shell
if [ "${SKIP_BASH}" = '0' ]; then

    for SHELL_PATH in "${SHELL_PATHS[@]}"; do

        update_shell "${SHELL_PATH}"

        echo
        echo "Do not re-run this script until you re-source ${SHELL_PATH}.  Strongly"
        echo "recommend you exit your session and open a new one."
    
    done
fi

