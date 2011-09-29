#!/usr/bin/env python3.1
from distutils.core import setup
import glob

setup(name="nanocut",
      version="0.2",
      description="Cutting out various shapes from crystals",
      author="Florian Uekermann, Sebastian Fiedel, Balint Aradi",
      author_email="baradi09@gmail.com",
      license="MIT",
      platforms="platform independent",
      package_dir={"": "src"},
      packages=["nanocut", ],
      scripts=[ "bin/nanocut" ],
      data_files=[("share/doc/nanocut", ["LICENSE", "README", ] ),
                  ("share/doc/nanocut/examples",
                   glob.glob("doc/srcexamples/*.ini")),
                  ],
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
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
