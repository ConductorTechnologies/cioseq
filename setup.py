#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools

from setuptools.command.build_py import build_py
from shutil import copyfile

NAME = "cioseq"
DESCRIPTION = "Manage sequences of frame numbers."
URL = "https://github.com/ConductorTechnologies/sequence"
EMAIL = "info@conductortech.com"
AUTHOR = "conductor"
REQUIRED = ["future>=0.18.2"]
HERE = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(HERE, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

long_description = ""
with open(os.path.join(HERE, 'README.md')) as readme:
    long_description = readme.read().strip()
long_description += "\n\n## Changelog\n\n"
with open(os.path.join(HERE, 'CHANGELOG.md')) as changelog:
    long_description += changelog.read().strip()

class BuildCommand(build_py):
    def run(self):
        build_py.run(self)

        if not self.dry_run:
            target_dir = os.path.join(self.build_lib, NAME)
            for fn in ["VERSION", "LICENSE", "README.md"]:
                copyfile(os.path.join(HERE, fn), os.path.join(target_dir,fn))


setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
    ],
    cmdclass={"build_py": BuildCommand},
    description=DESCRIPTION,
    install_requires=REQUIRED,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=NAME,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    options={"bdist_wheel": {"universal": True}},
    include_package_data=True, 
    url=URL,
    version=VERSION,
    zip_safe=False
)
