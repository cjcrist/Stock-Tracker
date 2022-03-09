# Reads the contents of the README file
from os import path
from setuptools import setup, find_packages


# Variables
NAME = "stock_tracker"
VERSION = "1.0.0"
SUMMARY = "Retrieves stock data.  More functionality to be added."

# Find and open README
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    try:
        long_description = f.read()
    except IOError:
        long_description = SUMMARY

# Find and open requirements
with open(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=SUMMARY,
    long_description=long_description,
    author='Chris Crist',
    author_email="ChrisCrist@protonmail.com",
    license='MIT',
    install_requires=requirements,
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    scripts=['stocktracker.py']
)
