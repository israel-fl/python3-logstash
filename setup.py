#!/usr/bin/env python3
import os
from distutils.core import setup

from logstash import __version__

readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
try:
    from m2r import parse_from_file

    long_description = parse_from_file(readme_file)
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        long_description = f.read()

setup(
    name="logstash-sync",
    packages=["logstash"],
    version=__version__,
    description="Python logging handler for Logstash.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sergey Yorsh",
    author_email="myrik260138@tut.by",
    url="https://github.com/MyrikLD/python3-logstash",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
)
