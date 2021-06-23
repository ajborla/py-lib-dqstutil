from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "r", encoding="utf-8") as fh:
    license = fh.read()

setup(
    name="dqstutil-ajborla",
    version="1.0.0",
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
    packages=find_packages(exclude=("test", "docs")),
    python_requires=">=3.8",
)
