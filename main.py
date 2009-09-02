# -*- coding: utf-8 -*-
'''
Created on Aug 28, 2009

@author: sebastian
'''
import numpy
import input
import geometry
import sphere

numpy.seterr(divide='ignore',invalid='ignore')

c=input.read_ini('sphere_input.ini')

d=input.ini2dict(c)

geo = geometry.geometry.from_dict(d)

sph = sphere.sphere.from_dict(geo, d)

#print geo._lattice_vectors
#print geo._basis
#print geo._basis_names
#print geo._basis_names_idx
#print sph._radius
#print sph._shift_vector
#print sph.containing_cuboid()

liste = geo.gen_cuboid_from_body(sph)

print len(liste)+2
print ""
for el in liste:
  print "H", el[0], el[1], el[2]