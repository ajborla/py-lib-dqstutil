from setuptools import setup, find_packages
import os
import sys


_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(os.path.join(_here, "LICENSE"), "r", encoding="utf-8") as fh:
    license = fh.read()

version = {}
with open(os.path.join(_here, "dqstutil", "version.py"), "r", encoding="utf-8") as fh:
    exec(fh.read(), version)

setup(
    name="dqstutil-ajborla",
    version=version["__version__"],
    author="Anthony J. Borla",
    author_email="ajborla@bigpond.com",
    description="A small suite of data manipulation routines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license,
    url="https://github.com/ajborla/dqstutil-py",
    project_urls={
        "Bug Tracker": "https://github.com/ajborla/dqstutil-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(exclude=("test", "docs")),
    python_requires=">=3.8",
)
