#
# Makefile for development build of Python 3 package, dqstutil.
#

# Ensure default system shell used
SHELL = /bin/sh

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
> @echo "---------------------------------------------"

build:
> @echo $@

install:
> @echo $@

uninstall:
> @echo $@

clean:
> @echo $@
