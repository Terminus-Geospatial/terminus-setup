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
 # Python Libraries
import argparse
import configparser
import logging
import os

DEFAULT_REPO_LIST = { 'terminus-setup'         : { 'url' :  'git@github.com:Terminus-Geospatial/terminus-setup.git',
                                                   'tags': ['tools'] },
                      'terminus-cmake'         : { 'url' :  'git@github.com:Terminus-Geospatial/terminus-cmake.git',
                                                   'tags': ['tools','cpp'] },
                      'terminus-log'           : { 'url' :  'git@bitbucket.org:msmith81886/terminus-log',
                                                   'tags': ['tools','cpp'] },
                      'terminus-outcome'       : { 'url' :  'git@bitbucket.org:msmith81886/terminus-outcome',
                                                   'tags': ['tools','cpp'] },
                      'terminus-core'          : { 'url' :  'git@bitbucket.org:msmith81886/terminus-core',
                                                   'tags': ['tools','cpp'] },
                      'terminus-math'          : { 'url' :  'git@bitbucket.org:msmith81886/terminus-math',
                                                   'tags': ['tools','cpp'] },
                      'terminus-nitf'          : { 'url' :  'git@bitbucket.org:msmith81886/terminus-nitf',
                                                   'tags': ['tools','cpp'] },
                      'terminus-image'         : { 'url' :  'git@bitbucket.org:msmith81886/terminus-image',
                                                   'tags': ['tools','cpp'] },
                      'terminus-cpp-demos'     : { 'url' :  'git@bitbucket.org:msmith81886/terminus-cpp-demos',
                                                   'tags': ['tools','cpp'] } }

def parse_command_line():

    parser = argparse.ArgumentParser( description='Clone all repos for the primary Terminus "stack".')

    tag_list = []
    for repo in DEFAULT_REPO_LIST:
        for tag in DEFAULT_REPO_LIST[repo]['tags']:
            if not tag in tag_list:
                tag_list.append( tag )

    parser.add_argument( '-v',
                          dest = 'log_severity',
                          default = logging.INFO,
                          required = False,
                          action = 'store_const',
                          const = logging.DEBUG,
                          help = 'Log at debugging level' )

    parser.add_argument( '-l', '--log-path',
                         dest = 'log_file_path',
                         default = None,
                         required = False,
                         help = 'Write output to log path.' )

    parser.add_argument( '--all',
                         dest = 'repo_set',
                         default = 'all',
                         action = 'store_const',
                         const = 'all',
                         help = 'Clone all repos for the project.' )
    
    parser.add_argument( '-t',
                         dest = 'tags',
                         action = 'append',
                         default=[],
                         required= False,
                         help = f'Clone repos with a specific tag. Expected Tags: {tag_list}' )
    
    return parser.parse_args()

def configure_logging( options ):

    if options.log_file_path is None:
        logging.basicConfig( level = options.log_level )
    else:
        logging.basicConfig( level = options.log_level, filename = options.log_file_path )

def main():
    
    #  Load command-line arguments
    cmd_args = parse_command_line()

    #  Setup logging
    configure_logging( cmd_args )

    #  Iterate over repo list
    for repo in DEFAULT_REPO_LIST:
        
        #  Get the repo url
        repo_url = DEFAULT_REPO_LIST[repo]['url']

        #  Build clone command
        clone_cmd = f'git clone {repo_url}'
        logging.debug( f'Command: {clone_cmd}' )
        os.system( clone_cmd )

if __name__ == '__main__':
    main()
