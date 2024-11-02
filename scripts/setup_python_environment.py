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

def removing_existing( logger, venv_path, dry_run ):

    logger.info( f'Removing existing environment' )
    cmd = f'rm -rv {venv_path}'
    
    if dry_run:
        logger.info( 'cmd: ', cmd )
    else:
        logger.debug( 'cmd: ', cmd )
        result = subprocess.run( cmd, shell = True, check = True, capture_output = True )
        if result.returncode != 0:
            logger.error( 'Unable to properly delete existing env: ',
                          result.stdout.decode('utf-8') )
            sys.exit(1)

def build_virtual_environment( logger, venv_path, python_path, dry_run ):

    cmd = f'{python_path} -m venv {venv_path}'
    if dry_run:
        logger.info( 'cmd: ', cmd )
    else:
        logger.debug( 'cmd: ', cmd )
        result = subprocess.run( cmd, check=True, shell = True, capture_output=True)
        if result.returncode != 0:
            logger.error( 'Error with creation of venv: ', result.stdout.decode('utf-8') )
            sys.exit(1)

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

if __name__ == '__main__':
    main()
