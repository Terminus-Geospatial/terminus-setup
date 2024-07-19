#!/usr/bin/env bash

skip -e

function usage() {
    echo "usage: ${0} <flags>"
    echo ''
    echo 'Installs the tools in this folder to your local workspace'
    echo 
    echo 'By default, the bashrc is modified.  Skip with flag outlined below.'
    echo
    echo '-h          : Print help menu'
    echo '--skip-bash : Do not update bashrc.  Just update scripts.'
    echo
}

SKIP_BASH=0

#  Iterate over arguments
while [ -n "${1}" ]; do
    case "${1}" in

        #  Print usage instructions
        -h)
            usage
            ;;
        
        #  Prevent updating the bashrc
        --skip-bash)
            SKIP_BASH=1
            ;;
        *)
            echo "Unsupported flag: ${1}"
            exit 1
    esac
    shift
done

#  Get the path of this folder
SPATH="`dirname ${0}`"

#  Create destination and install files there
mkdir -p ${HOME}/.local/bin
rsync -avP ${SPATH}/utils/ ${HOME}/.local/bin/

#  Update bashrc
if [ "${SKIP_BASH}" = '0' ]; then

    #  Check if ${HOME}/.local/bin is already on the system path
    if [[ ${PATH} =~ ^${HOME}/.local/bin:|:${HOME}/.local/bin:|:${HOME}/.local/bin$ ]]; then
        echo "${HOME}/.local/bin is already in path."
    else
        echo "${HOME}/.local/bin is not in path; adding"
        echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ${HOME}/.bashrc
    fi

    #  Check if tmns-import is already defined
    if [ "`grep tmns-import ${HOME}/.bashrc`" = '' ]; then 
        echo "tmns-import is not defined.  Adding to ${HOME}/.bashrc"
        
        echo ''                                                          >> ${HOME}/.bashrc
        echo '# Added by terminus-repo-utilities: install-local.bash'    >> ${HOME}/.bashrc
        echo 'function tmns-import() {'                                  >> ${HOME}/.bashrc
        echo '   source ${HOME}/.local/bin/tmns_bash_aliases.bash'       >> ${HOME}/.bashrc
        echo '}'                                                         >> ${HOME}/.bashrc
    else
        echo 'tmns-import already defined. skipping'
    fi

    echo
    echo 'Do not re-run this script until you re-source your bashrc.  Strongly'
    echo 'recommend you exit your session and open a new one.'
fi
