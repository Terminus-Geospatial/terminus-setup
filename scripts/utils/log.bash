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
#    File:    log.bash
#    Author:  Marvin Smith
#    Date:    7/5/2023
#
#    Purpose:  Logging Utilities
#

if [ "$TERMINUS_NO_COLOR" != 'true' ]; then
    __color_grey='\033[38;5;8m'
    __color_purple='\033[38;5;13m'
    __color_yellow='\033[38;5;3m'
    __color_blue='\033[38;5;33m'
    __color_red='\033[38;5;9m'
    __color_reset='\033[0m'
fi

declare -A _terminus_log_levels
_terminus_log_levels=(
    [debug]=0
    [trace]=1
    [info]=2
    [warn]=3
    [error]=4
)

if [ ! -z "$TERMINUS_VERBOSE" ]; then
    _terminus_log_level=${_terminus_log_levels[debug]}
elif [ ! -z "$TERMINUS_LOG_LEVEL" ]; then
    _terminus_log_level=${_terminus_log_levels[$TERMINUS_LOG_LEVEL]}
else
    _terminus_log_level=${_terminus_log_levels[info]}
fi

function _should_log() {
    test "$_terminus_log_level" -le "${_terminus_log_levels[$1]}"
}

function log_debug() {
    _should_log debug && echo -e "${__color_purple}debug:${__color_reset}" $@ || true
}

function log_trace() {
    _should_log trace && echo -e "${__color_blue}trace:${__color_reset}" $@ || true
}

function log_info() {
    _should_log info && echo -e "${__color_blue}info:${__color_reset}" $@ || true
}

function log_warn() {
    _should_log warn && echo -e "${__color_yellow}warning:${__color_reset}" $@ || true
}

function log_error() {
    _should_log error && echo -e "${__color_red}error:${__color_reset}" $@ || true
}


