# -*- coding: utf-8 -*-
'''
Created on Aug 28, 2009

@author: sebastian
'''
import numpy
import input
import geometry
import sphere

c=input.read_ini('sphere_input.ini')

d=input.ini2dict(c)

geo = geometry.geometry.from_dict(d)

sph = sphere.sphere.from_dict(geo, d)

print geo._lattice_vectors
print geo._basis
print geo._basis_names
print geo._basis_names_idx
print sph._radius
print sph._shift_vector