#!/usr/bin/env python3
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

import argparse
import logging
import os
import subprocess
import sys

DEFAULT_VENV_PATH = os.path.join( os.environ.get("HOME"), 'conan' )

LOG_FORMAT = '%(asctime)s - %(levelname)-8s - %(message)s'

def is_valid_python(string):

    #  If it's a root-relative python version,
    pyversion = subprocess.run([string,'--version'], check=True, capture_output=True).stdout.decode('utf-8')
    logging.info( f'Python ({string}) version: {pyversion.split(" ")[1].strip()}' )
    return string

    
def parse_command_line():

    parser = argparse.ArgumentParser( description = 'Setup Virtual Environment for Terminus Apps.' )
    
    parser.add_argument( '-v', '--verbose',
                         dest = 'log_level',
                         default = logging.INFO,
                         action = 'store_const',
                         const = logging.DEBUG,
                         help = 'Use verbose logging' )
    
    parser.add_argument( '--venv-path',
                         dest = 'venv_path',
                         default = DEFAULT_VENV_PATH,
                         help = 'Where to install Python VENV' )

    parser.add_argument( '-o',
                         '--create-if-exists',
                         dest = 'create_if_exists',
                         default = False,
                         action = 'store_true',
                         help = 'Create environment even if it exists.' )
    
    parser.add_argument( '-p', '--python',
                         dest = 'python_path',
                         default = 'python3',
                         type = is_valid_python,
                         help = 'Python installation' )
    
    parser.add_argument( '--dry-run',
                         dest = 'dry_run',
                         default = False,
                         action = 'store_true',
                         help = 'Print commands which would be executed, then exit.' )
    
    return parser.parse_args()

def run_command( logger, command, desc, dry_run, exit_if_fail = True ):

    if dry_run:
        logger.info( f'command: {command}' )
    else:
        logger.debug( f'command: {command}' )
        result = subprocess.run( command, shell = True, check = True, capture_output = True )
        if result.returncode != 0:
            logger.error( f'Unable to properly {desc}: ',
                          result.stdout.decode('utf-8') )
            if exit_if_fail:
                sys.exit(1)
        logger.debug( result.stdout.decode('utf-8'))

def removing_existing( logger, venv_path, dry_run ):

    logger.info( f'Removing existing environment' )
    cmd = f'rm -rv {venv_path}'
    run_command( logger, cmd, 'delete existing environment', dry_run )


def build_virtual_environment( logger, venv_path, python_path, dry_run ):

    logger.info( f'Building new Virtual Environment' )
    cmd = f'{python_path} -m venv {venv_path}'
    run_command( logger, cmd, 'creating new venv', dry_run )

def setup_virtual_environment( logger, python_path, venv_path, dry_run ):

    cmd = f'. {venv_path}/bin/activate && pip install --upgrade pip'
    run_command( logger, cmd, 'updating pip', dry_run )

    cmd = f'. {venv_path}/bin/activate && pip install conan'
    run_command( logger, cmd, 'installing conan', dry_run )

def update_shell_scripts( logger, venv_path, dry_run ):

    #  Iterate over available scripts
    for shell_rc in [ f'{os.environ.get("HOME")}/.bashrc', f'{os.environ.get("HOME")}/.zshrc' ]:

        if os.path.exists( shell_rc ):
            print( f'Updating: {shell_rc}' )

            #  Check if shell script has the import function already
            add_command = False
            with open( shell_rc, 'r' ) as fin:
                text = fin.read()
                if 'go-conan' in text:
                    logger.warning( f'The command "go-conan" already in {shell_rc}' )
                else:
                    add_command = True

            if add_command:
                cmd  = f'\necho "# This function added by Terminus setup-conan script." >> {shell_rc}\n'
                cmd += f'echo "function go-conan() {{" >> {shell_rc}\n'
                cmd += f"echo '    . ${{HOME}}/conan/bin/activate' >> {shell_rc}\n"
                cmd += f"echo '}}' >> {shell_rc}"
                run_command( logger, cmd, 'adding conan alias', dry_run )

def main():

    logging.basicConfig( level = logging.INFO, format = LOG_FORMAT )
    logger = logging.getLogger( 'setup_python_environment' )

    cmd_args = parse_command_line()

    #  Setup logging
    logger.setLevel( cmd_args.log_level )
    logger.debug( 'Installing Python Virtual Environment' )

    build_venv = True

    #  Check if environment already is setup
    venv_path = cmd_args.venv_path
    env_activate_path = os.path.join( venv_path, 'bin/activate' )
    logger.debug( f'Checking venv activate script: {env_activate_path}' )

    if os.path.exists( env_activate_path ):
        logger.warning( f'Environment path already exists at {venv_path}' )
        if cmd_args.create_if_exists:
            removing_existing( logger, venv_path, cmd_args.dry_run )
        else:
            build_venv = False

    if build_venv:
        build_virtual_environment( logger, 
                                   venv_path,
                                   cmd_args.python_path,
                                   cmd_args.dry_run )
        
    setup_virtual_environment( logger, 
                               cmd_args.python_path,
                               venv_path, 
                               cmd_args.dry_run )

    update_shell_scripts( logger, 
                          venv_path,
                          cmd_args.dry_run )

if __name__ == '__main__':
    main()
