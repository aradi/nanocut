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


c=input.read_ini('planes_input.ini')
d=input.ini2dict(c)
geo = geometry.geometry.from_dict(d)

#sph = sphere.sphere.from_dict(geo, d['sphere'])

poly = convex_poly.convex_poly.from_dict(geo, d)

#print poly._planes_normal

atoms = geo.gen_cuboid_from_body(poly)

#in_out_array = numpy.array([1 for x in atoms == 1])

in_out_array = convex_poly.sorting(atoms)

output.write_structure_to_file(geo, atoms, in_out_array, 'out.xyz')
