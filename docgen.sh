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

# `markdown-to-html-github-style` checks and tasks
git clone https://github.com/KrauseFx/markdown-to-html-github-style.git >/dev/null 2>&1
cd markdown-to-html-github-style
npm install >/dev/null 2>&1 || { echo Problem installing nodejs support files; exit 1; }
rm -fr ./README.md \
    && cp ${DOCDIR}/README.md .
node convert.js ${TITLE} >/dev/null 2>&1
[ -e ./README.html ] \
    && mv README.html index.html \
    && mv index.html ${DOCDIR}/ \
    || { echo Problem generating README.html; exit 1; }
cd ..
rm -fr markdown-to-html-github-style

# Fix `markdown-to-html-github-style` conversion anomalies
sed -i 's/\(<em>\|<\/em>\)/\_/g' ${DOCDIR}/index.html
