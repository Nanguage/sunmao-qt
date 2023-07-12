#!/usr/bin/env python

"""The setup script."""

import re
from setuptools import setup, find_namespace_packages


def get_long_description():
    return "See https://github.com/Nanguage/sunmao-qt"


def get_version():
    with open("sunmao/qt/__init__.py") as f:
        for line in f.readlines():
            m = re.match("__version__ = '([^']+)'", line)
            if m:
                return m.group(1)
        raise IOError("Version information can not found.")


def get_install_requirements():
    requirements = [
    ]
    return requirements


requires_test = ['pytest', 'pytest-cov', 'flake8', 'mypy']
packages_for_dev = ["pip", "setuptools", "wheel", "twine", "ipdb"]

requires_dev = packages_for_dev + requires_test

setup(
    name='sunmao-qt',
    author="Weize Xu",
    author_email='vet.xwz@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Node editor for build computational workflow.",
    license="MIT license",
    install_requires=get_install_requirements(),
    long_description=get_long_description(),
    include_package_data=True,
    packages=find_namespace_packages(include=['sunmao.*']),
    url='https://github.com/Nanguage/sunmao-qt',
    version=get_version(),
    zip_safe=False,
    extras_require={
        'dev': requires_dev,
    }
)
