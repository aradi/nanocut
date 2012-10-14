#!/usr/bin/env python3.2
from distutils.core import setup

setup(name="nanocut",
      version="12.10",
      description="Cutting out various shapes from crystals",
      author="Florian Uekermann, Sebastian Fiedel, Bálint Aradi",
      author_email="baradi09@gmail.com",
      url="http://bitbucket.org/aradi/nanocut",
      license="BSD",
      platforms="platform independent",
      package_dir={ "": "src"},
      packages=[ "nanocut", ],
      scripts=[ "bin/nanocut" ],
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.2",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        ],
      long_description="""
Cutting out various shapes from crystals
----------------------------------------

This tool provides you the possibility to cut out various forms from crystal
structures. You can create dots, wires, surfaces or any arbitrary periodic
or non-periodic structures, by specifying the crystal structure and the bounding
surfaces of the object to be cut out.
""")
