from setuptools import setup, find_packages
import os
import sys


# Anchor reference
_here = os.path.abspath(os.path.dirname(__file__))

# Entire package README forms descrioption string
with open(os.path.join(_here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Package version will be read from a custom `version` file
version = {}
with open(os.path.join(_here, "dqstutil", "version.py"), "r", encoding="utf-8") as fh:
    exec(fh.read(), version)

# Declare any multi-use data here
author = "Anthony J. Borla"
author_email = "ajborla@bigpond.com"

# Create setup options
setup(
    name="dqstutil-ajborla",
    version=version["__version__"],
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    description="Collection of utility functions for querying and managing a table-based dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/ajborla/py-lib-dqstutil",
    project_urls={
        "Bug Tracker": "https://github.com/ajborla/py-lib-dqstutil/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("test", "docs", "examples")),
    python_requires=">=3.8",
    test_suite = "test.test_dqstutil_suite",
)
