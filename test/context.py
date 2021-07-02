"""Insert reference to parent directory into module path."""


import sys
import os

parent = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, os.path.abspath(parent))
