#!usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 28, 2009

@author: sebastian
'''
#Import public modules
import sys, numpy

#Import own modules
import inout, geometry, sphere, convex_polyhedron

try:
  config_ini=inout.read_ini(sys.argv[1])
except IndexError:
  exit('Error! Please assign an input file!')


'''Read configuration from config_ini and write it into a (dict) config_dict.'''
config_dict=inout.ini2dict(config_ini)

'''Initialise geometry-object from config_dict'''
geo = geometry.geometry.from_dict(config_dict)


'''Initialise body objects and store references in bodies list'''
bodies=[]

for body in config_dict.keys():
  if body[0:7]=="sphere:":
    body = sphere.sphere.from_dict(geo, config_dict[body])
    bodies.append(body)
  elif body[0:18]=="convex_polyhedron:":
    body = convex_polyhedron.convex_polyhedron.from_dict(geo, config_dict[body])
    bodies.append(body)
  else:
    print ('Warning:\n'+
      '"'+body+'"'+' is not a valid name for a body and will be ignored.'
      +'\nContinuing...')

'''Get boundaries of the cuboid containing all bodies'''

print config_dict.keys()
print bodies

cuboid_boundaries = numpy.vstack([body.containing_cuboid() for body in bodies if body.is_additive()])
cuboid_boundaries = numpy.vstack([cuboid_boundaries.max(axis=0),cuboid_boundaries.min(axis=0)])


'''Generate lattice-cuboid'''
lattice_cuboid = geo.gen_cuboid(cuboid_boundaries)


'''Generate cuboid containig all atoms'''
atoms_cuboid = geo.gen_atoms(lattice_cuboid)



'''Decide which atoms really are inside the specified set of body.'''
#Find the highest order
max_order = max([body.get_order() for body in bodies])


#Test for atoms inside bodies in the right order.

atoms_inside_bodies=numpy.zeros(atoms_cuboid[:,3].shape,bool)

for order in range(1,max_order+1):
  
  for body in bodies:
    
    if body.order_is(order):
      tmp_atoms_inside_bodies = body.atoms_inside(atoms_cuboid)
      #Add and substract them respectively
      if order%2!=0:
	atoms_inside_bodies = atoms_inside_bodies + tmp_atoms_inside_bodies
      else:
	
	atoms_inside_bodies = (atoms_inside_bodies + tmp_atoms_inside_bodies) - tmp_atoms_inside_bodies
	
'''Write final crystal to file'''
try:
  inout.write_structure_to_file(geo, atoms_cuboid, atoms_inside_bodies, sys.argv[2])
except IndexError:
  exit('Error! Please assign an output file name!')
  
