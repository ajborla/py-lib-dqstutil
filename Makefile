#
# Makefile for development build of Python 3 package, dqstutil.
#

# Ensure default system shell used
SHELL = /bin/sh

# Check `make` version for `.RECIPEPREFIX` support; bail if < 4.0
VER_OK = $(or $(findstring 4., $(MAKE_VERSION)), $(findstring 5., $(MAKE_VERSION)))
ifeq ($(VER_OK),)
    $(error Version 4.0 or later of `make` required)
endif

# Override use of tab character (\t) as recipe (i.e. action) prefix
.RECIPEPREFIX = >

# Print a help message on default invocation
.DEFAULT_GOAL = help

# Tag `phony` targets to avoid being considered perpetually up-to-date
.PHONY: help build install uninstall clean

# Clear and replace default suffixes
.SUFFIXES:
.SUFFIXES: .py .pyc

# Enforce Python 3 use
PYTHON = python3

# Extract package name from `setup.py`
PACKAGE = $(shell sed -n "s/\s*name=\"\(.*\)\",\$$/\1/p" setup.py)

help:
> @echo "------------------- HELP --------------------"
> @echo ""
> @echo "Type:"
> @echo ""
> @echo "    make ACTION"
> @echo ""
> @echo "to perform an action on this system, where"
> @echo "ACTION is one of:"
> @echo ""
> @echo "    build - build the system"
> @echo "    install - install the system"
> @echo "    uninstall - uninstall the system"
> @echo "    clean - remove generated system artefacts"
> @echo ""
> @echo "NOTE: All operations target the LOCAL system."
> @echo ""
> @echo "---------------------------------------------"

build: clean
> @$(PYTHON) -m build
> @$(PYTHON) -m twine check dist/*

install:
> @$(PYTHON) -m pip install $(shell ls dist/*.tar.gz)

uninstall:
> @$(PYTHON) -m pip uninstall $(PACKAGE)

clean:
> @$(RM) -fr dist build *.egg-info
