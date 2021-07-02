#
# Makefile for development build of Python 3 package, dqstutil.
#

# Ensure default system shell used
SHELL = /bin/sh

# Override use of tab character (\t) as recipe (i.e. action) prefix
.RECIPEPREFIX = >

# Tag `phony` targets to avoid being considered perpetually up-to-date
.PHONY: help build install uninstall clean

# Clear and replace default suffixes
.SUFFIXES:
.SUFFIXES: .py .pyc

# Enforce Python 3 use
PYTHON = python3

help:
> @echo $@

build:
> @echo $@

install:
> @echo $@

uninstall:
> @echo $@

clean:
> @echo $@
