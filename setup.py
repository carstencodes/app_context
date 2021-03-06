#!/usr/bin/env python

#
# Copyright (c) 2020 Carsten Igel.
#
# This file is part of app_context
# (see https://github.com/carstencodes/app_context).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#

from setuptools import setup, find_packages

__VERSION__ = "0.9.0"

long_description: str = ""
with open("README.md", "r") as read_me_file:
    long_description = read_me_file.read()

setup(
    name="app_context",
    version=__VERSION__,
    license="BSD-3-Clause",
    author="Carsten Igel",
    author_email="cig@bite-that-bit.de",
    description="A small wrapper around announcing a data class"
    + " with application information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    url="https://github.com/carstencodes/app_context",
    install_requires=["setuptools", "packaging"],
    package_dir={"": "src"},
    keywords="application, platform, environment, development",
    python_requires=">=3.7, < 4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System",
        "Typing :: Typed",
    ],
)
