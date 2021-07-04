#!/usr/bin/env sh

# Check for required command utilities
which python3 >/dev/null || { echo python3 not installed; exit 1; }
which node >/dev/null || { echo node not installed; exit 1; }
which git >/dev/null || { echo git not installed; exit 1; }
