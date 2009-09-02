# -*- coding: utf-8 -*-
'''
Created on Aug 28, 2009

@author: sebastian
'''
import numpy
import input
import geometry
import sphere
import output

numpy.seterr(divide='ignore',invalid='ignore')

c=input.read_ini('sphere_input.ini')

d=input.ini2dict(c)

geo = geometry.geometry.from_dict(d)

sph = sphere.sphere.from_dict(geo, d)

atoms = geo.gen_cuboid_from_body(sph)
#atoms = []
#for el in geo.gen_atoms(numpy.array([0,0,0])):
#  atoms.append(el)
#for el in geo.gen_atoms(numpy.array([5,0,0])):
#  atoms.append(el)
#for el in geo.gen_atoms(numpy.array([2.5,2.5,0])):
#  atoms.append(el)
#for el in geo.gen_atoms(numpy.array([2.5,0,2.5])):
#  atoms.append(el)
  
#atoms=numpy.array(atoms)
in_out_array = sph.sorting(atoms)

output.write_structure_to_file(geo, atoms, in_out_array, 'file')