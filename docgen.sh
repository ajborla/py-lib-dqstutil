#!/usr/bin/env sh

# Check for required command utilities
which python3 >/dev/null || { echo python3 not installed; exit 1; }
which node >/dev/null || { echo node not installed; exit 1; }
which git >/dev/null || { echo git not installed; exit 1; }

# Process shell parameters
[ -n "$1" ] \
    && DOCDIR=$(readlink -f "$1") \
    || { echo Missing documents directory; exit 1; }

# Set globals
TITLE='dqstutil - (d)ata (q)uery and (st)atistical (util)ities'

# `doc2md` checks and tasks
python3 -m pip list | grep doc2md >/dev/null \
    && REMOVE_DOC2MD=1 \
    || { python3 -m pip install doc2md; REMOVE_DOC2MD=0; }
python3 -m doc2md -a -t "${TITLE}" dqstutil > ${DOCDIR}/README.md
[ ${REMOVE_DOC2MD} -eq 0 ] \
    && python3 -m pip uninstall doc2md

# Fix `doc2md` conversion anomalies
sed -i 's/^### /## /' ${DOCDIR}/README.md
