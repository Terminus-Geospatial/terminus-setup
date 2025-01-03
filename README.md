Terminus Setup
==========================

This repo has the necessary tools for setting up the tools required to build and install Terminus.

## Overview

Terminus C++ APIs are designed to be built using Conan.  This is not explicitly required, however Conan offers a few major benefits, specifically around versioning.

---

## Step 1: Setup Conan
If you already have conan installed, then skip this this.  Make sure to enable conan on your system path. 

If you do not have conan installed, run the following:

```bash
pushd scripts
./setup-conan.py
```

This will create a Python virtual environment in `${HOME}/conan` with conan installed. 

## Step 2: Restart your shell or re-source the particular rc file.

```bash
. ~/.zshrc
```

## Step 3: Import Conan

If you use this install script, it adds a command `go-conan` inside your shell RC file. 

* ZSH: `${HOME}/.zshrc`
* BASH: `${HOME}/.bashrc`

Run one of the two following commands to import the conan environment. 

1. `go-conan`
2. `. ${HOME}/conan/bin/activate`

## Step 4: Clone Terminus Repos

This repo packages a command-line tool for cloning all repositories in a single shot. 

```bash
tmns-clone-repos.py -vv --all
```

