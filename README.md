Terminus Repo Utilities
==========================

This has a few key tools for configuring a system to build the Terminus software repos. 

## Setting Up New Linux / MacOS System

1. Navigate to the scripts folder and run the `install-local.bash` script.

This toolchain will do the following:

- Check for all required tools on the command-line
    - `conan`

- If `conan` does not exist, it will give you the chance to setup a virtual environment

- The script will setup your `${HOME}/.bashrc` or `${HOME}/.zshrc` file. 

2. Next, restart your shell or re-source the particular rc file.

