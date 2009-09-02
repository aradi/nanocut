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

#geo.gen_cuboid0(numpy.array([[0,0,0],[4,6,11]]))

atoms = geo.gen_cuboid_from_body(sph)

in_out_array = sph.sorting(atoms)

output.write_structure_to_file(geo, atoms, in_out_array, 'out.xyz')
