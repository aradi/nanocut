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
import convex_polyeder

numpy.seterr(divide='ignore',invalid='ignore')


c=input.read_ini('planes_input.ini')
d=input.ini2dict(c)
geo = geometry.geometry.from_dict(d)
#print geo._lattice_vectors[0]
#sph = sphere.sphere.from_dict(geo, d['sphere'])

poly = convex_polyeder.convex_polyeder.from_dict(geo, d)

#print poly._planes_normal

atoms = geo.gen_cuboid_from_body(poly)

#in_out_array = numpy.array([1 for x in atoms == 1])

in_out_array = poly.atoms_inside(atoms)

output.write_structure_to_file(geo, atoms, in_out_array, 'out.xyz')
