#!/usr/bin/env bash


function tmns-build-clean() {
    find . -name 'build' -type 'd' -exec rm -rvf {} \;
}
