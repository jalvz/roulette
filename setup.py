#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="roulette",
    version="0.0.1",
    description="Utility to repeat tests given customized constraints and success criteria",
    author="Juan Alvarez",
    author_email="juan.afernandez@ymail.com",
    platforms=["any"],
    packages=find_packages(exclude="test"),
    keywords=["test", "unit test"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)