Terminus Setup
==========================

This has a few key tools for configuring a system to build the Terminus software repos. 

## Setup Conan
If you already have conan installed, then skip this this.  Make sure to enable conan on your system path. 

If you do not have conan installed, runt he following:

```bash
pushd scripts
./setup-conan.py -p <python-version> 
```

This will create a Python virtual environment in `${HOME}/conan` with conan installed. 

Then, activate the env. 

```bash
. ${HOME}/conan/bin/activate
```

## Setting Up New Linux / MacOS System

1. Navigate to the scripts folder and run the `install-local.bash` script.

This toolchain will do the following:

- Check for all required tools on the command-line
    - `conan`

- The script will setup your `${HOME}/.bashrc` or `${HOME}/.zshrc` file. 

2. Next, restart your shell or re-source the particular rc file.


