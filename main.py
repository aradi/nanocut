# -*- coding: utf-8 -*-
'''
Created on Aug 28, 2009

@author: sebastian
'''
import numpy
import input

c=input.read_ini('convex_polyeder_input.ini')

d=input.ini2dict(c)

(lattice_vectors, basis, basis_names, basis_name_idx) = input.geometry_from_dict(d)

print lattice_vectors
print basis
print basis_names
print basis_name_idx