#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as changelog_file:
    changelog = changelog_file.read()

with open("LICENSE") as license_file:
    license = license_file.read()


requirements = [
    "pandas",
	"pyqt>=5.6.0",
	"guanopy"
]

test_requirements = [
    "pytest",
]


setup(
    name="guanomdeditor",
    version="0.0.1",
    description="A simple open-source viewer and editor for Guano Metadata embedded in bat call wav files.",
    long_description=readme + "\n\n" + changelog,
    author="Colin Talbert",
    author_email="talbertc@usgs.gov",
    url="",
    packages=[
        "guanomdeditor",
    ],
    package_dir={"guanomdeditor":
                 "guanomdeditor"},
    include_package_data=True,
    install_requires=requirements,
    license=license,
    zip_safe=False,
    keywords="guanomdeditor",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Natural Language :: English",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    test_suite="tests",
    tests_require=test_requirements
)
