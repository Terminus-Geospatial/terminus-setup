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

#  Python Libraries
import argparse
import collections
import datetime
import logging


CPP_BASE_TEMPLATE = '''/**************************** INTELLECTUAL PROPERTY RIGHTS ****************************/
/*                                                                                    */
/*                           Copyright (c) __YEAR__ Terminus LLC                          */
/*                                                                                    */
/*                                All Rights Reserved.                                */
/*                                                                                    */
/*          Use of this source code is governed by LICENSE in the repo root.          */
/*                                                                                    */
/***************************# INTELLECTUAL PROPERTY RIGHTS ****************************/
/**
 * @file    __PATHNAME__
 * @author  __AUTHOR__
 * @date    __HEADER_DATE____PURPOSE__
 */

namespace __NAMESPACE__ {

__CONTENT__

} // End of __NAMESPACE__ namespace
'''

def format_purpose( args ):
    
    CPP_FORMAT   = '\n *\n * @details __PURPOSE__'
    PY_FORMAT    = '\n#\n#    Purpose: __PURPOSE__'
    CMAKE_FORMAT = PY_FORMAT

    lang_options = { 'cpp'   : CPP_FORMAT,
                     'hpp'   : CPP_FORMAT,
                     'py'    : PY_FORMAT,
                     'cmake' : CMAKE_FORMAT }
    
    if args["purpose"] is None:
        return ''
    return lang_options[args["file_type"]].replace( '__PURPOSE__',args["purpose"])

def format_class_name( args ):

    CPP_FORMAT = f'/**\n * @class {args["class_name"]}\n */\nclass {args["class_name"]}\n{{\n    public:\n\n    private:\n\n}};// End of {args["class_name"]} class'
    PY_FORMAT  = f'class {args["class_name"]}:\n\n    def __init__(self):\n        pass\n\n'

    if args["class_name"] is None:
        return '__CONTENT__'
    
    choices = { 'cpp': CPP_FORMAT,
                'hpp': CPP_FORMAT,
                'py' : PY_FORMAT }
    
    return choices[args["file_type"]] + '__CONTENT__' 

def write_file( args, content ):

    with open( args["output_path"], 'w' ) as fout:

        fout.write( content )
        

def parse_command_line():

    parser = argparse.ArgumentParser(description='Create empty files for TMNS projects.')

    parser.add_argument( '-t',
                         dest='file_type',
                         required = False,
                         choices = ['cpp','hpp','py','cmake'],
                         help = 'Type of file to generate. Not required if interactive mode.' )
    
    parser.add_argument( '-i','--interactive',
                         dest = 'interactive',
                         default = False,
                         action = 'store_true',
                         help = 'Force interactive on optional parameters.' )
    
    parser.add_argument( '--ns',
                         dest = 'cpp_namespace',
                         required = False,
                         default = 'tmns',
                         help = 'C++ namespace (C++ only)' )
    
    parser.add_argument( '--author',
                         dest = 'author',
                         default = 'Marvin Smith',
                         required = False,
                         help = 'Author name to use for writing file.' )
    
    parser.add_argument( '--purpose',
                         dest = 'purpose',
                         default = None,
                         required = False,
                         help = 'Add description of what file contains.' )
    
    parser.add_argument( '--class',
                         dest = 'class_name',
                         required = False,
                         default = None,
                         help = 'Class name to use, if provided.' )

    parser.add_argument( dest = 'output_path',
                         help = 'Where to write the new file' )

    return parser.parse_args()

    
def interactive_menu( args, keyname, choices = None, skip_if_set = True ):

    #  Skip if file type already specified
    if skip_if_set and keyname in args and not args[keyname] is None:
        return args
    
    result = None
    prompt = [f'Enter value for {keyname}.']

    if not choices is None:
        prompt = []
        for c in choices:
            prompt.append( f'{c}. {choices[c]["desc"]}')

    while True:

        for p in prompt:
            print(p)
        res = input( 'Type result and press enter: ' )

        try:

            if not choices is None:
                result = choices[str(res).strip()]['result']
                args[keyname] = result
            else:
                args[keyname] = str(res).strip()
            break
        except Exception as e:
            logging.error( f'Invalid Input: {e}')
            pass

    return args


def run_interactive( args ):

    args = vars(args)
    
    #  Process file-type
    choices = choices = { '1': { 'desc': 'C++ Header File',     'result': 'hpp' },
                          '2': { 'desc': 'C++ Source File',     'result': 'cpp' },
                          '3': { 'desc': 'Python File',         'result': 'py' },
                          '4': { 'desc': 'CMakeLists.txt File', 'result': 'cmake' },
                          '5': { 'desc': 'Cancel and Exit',     'result': None }  }
    args = interactive_menu( args, 'file_type',
                             choices = choices,
                             skip_if_set = True )
    
    #  Process Author
    args = interactive_menu( args, 'cpp_namespace', skip_if_set = True )

    return args

def print_args( args ):

    for arg in args:
        print( f'{arg}   -> {args[arg]}')

def main():

    args = parse_command_line()

    args = run_interactive( args )
    if args is None:
        logging.error('Exiting application')

    print_args(args)

    #  Create base template
    template = None
    if args['file_type'] == 'cpp' or args['file_type'] == 'hpp':
        template = CPP_BASE_TEMPLATE
    else:
        logging.error( 'Unsupported file type: ' + args['file_type'] )
        return 1
    
    #-----------------------------------------------#
    #-              Setup Information              -#
    #-----------------------------------------------#
    
    #   File Pathname
    template = template.replace( '__PATHNAME__', args['output_path'] )

    #   Date
    date_string = datetime.datetime.now().strftime("%m/%d/%Y")
    template = template.replace('__HEADER_DATE__',date_string)
    template = template.replace('__YEAR__',datetime.datetime.now().strftime("%Y"))

    #  Author Name
    if 'author' in args.keys():
        template = template.replace( '__AUTHOR__', args['author'] )

    #  Purpose
    template = template.replace( '__PURPOSE__', format_purpose( args ) )

    #  Namespace (CPP Only)
    template = template.replace( '__NAMESPACE__', args["cpp_namespace"] )

    #  CPP Class
    template = template.replace( '__CONTENT__', format_class_name( args ))


    #  This must always be the last section prior to writing file.  That way, the content can get removed
    #  if it is still there.
    template = template.replace( '__CONTENT__', '' )

    #  Write file to disk
    write_file( args, template )

if __name__ == '__main__':
    main()