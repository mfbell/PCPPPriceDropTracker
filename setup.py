"""Setup module for PCPPPriceDropTracker."""

from setuptools import setup, find_packages
from codecs import open
from os import path

from PCPPPriceDropTracker.tools import PD


here = path.abspath(path.dirname(__file__))

with open(path.join(here, PD["project"]["long_description"]), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, PD["project"]["requirements"]), encoding='utf-8') as f:
    requirements = [line.strip() for line in f]

setup(
    name=PD["project"]["name"],
    version=PD["project"]["version"],
    description=PD["project"]["description"],
    long_description=long_description,
    url=PD["project"]["url"],
    author=", ".join([PD["authors"][a]["name"] + " " + PD["authors"][a]["url"] for a in PD["authors"]]),
    author_email=", ".join([PD["authors"][a][contact] for a in PD["authors"]]),
    license=PD["project"]["license"]["name"],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=PD["project"]["classifiers"],
    keywords=PD["project"]["keywords"], # Need to improve.
    packages=find_packages(exclude=PD["project"]["exclude-packages"]),
    install_requires=requirements,
    entry_points=PD["project"]["entry_points"],
    include_package_data=PD["project"]["include_package_data"]
    )
