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

<<<<<<< TREE
numpy.seterr(divide='ignore',invalid='ignore')


c=input.read_ini('planes_input.ini')
d=input.ini2dict(c)
geo = geometry.geometry.from_dict(d)
#print geo._lattice_vectors[0]
#sph = sphere.sphere.from_dict(geo, d['sphere'])

poly = convex_polyeder.convex_polyeder.from_dict(geo, d)

#print poly._planes_normal

atoms = geo.gen_cuboid_from_body(poly)
=======
'''Parse configuration from ini-file and store it in a config_ini-object.'''
config_ini=input.read_ini('sphere_input.ini')

'''Read configuration from config_ini and write it into a (dict) config_dict.'''
config_dict=input.ini2dict(config_ini)

'''Initialise geometry-object from config_dict'''
geo = geometry.geometry.from_dict(config_dict)


'''Initialise body objects and store references in bodies list'''
bodies=[]

for body in config_dict.keys():
  if body[0:7]=="sphere:":
    body = sphere.sphere.from_dict(geo, config_dict[body])
    bodies.append(body)
  else:
    print ('Warning:\n'+
      '"'+body+'"'+' is not a valid name for a body and will be ignored.'
      +'\nContinuing...')

'''Get boundaries of the cuboid containing all bodies'''

cuboid_boundaries = numpy.vstack([body.containing_cuboid() for body in bodies if body.is_additive()])
cuboid_boundaries = numpy.vstack([cuboid_boundaries.max(axis=0),cuboid_boundaries.min(axis=0)])

'''Generate lattice-cuboid'''
lattice_cuboid = geo.gen_cuboid(cuboid_boundaries)

'''Generate cuboid containig all atoms'''
atoms_cuboid = geo.gen_atoms(lattice_cuboid)

'''Decide which atoms really are inside the specified set of body.'''
#Find the highest order
max_order = max([body.get_order() for body in bodies])

atoms_inside_bodies=numpy.zeros(atoms_cuboid[:,3].shape,bool)

#Test for atoms inside bodies in the right order.


for order in range(1,max_order+1):
  
  for body in bodies:
    
    if body.order_is(order):
      tmp_atoms_inside_bodies = body.atoms_inside(atoms_cuboid)
      #Add and substract them respectively
      if order%2!=0:
	atoms_inside_bodies = atoms_inside_bodies + tmp_atoms_inside_bodies
      else:
	
	atoms_inside_bodies = (atoms_inside_bodies + tmp_atoms_inside_bodies) - tmp_atoms_inside_bodies
	






'''Write final crystal to xyz-file'''
output.write_structure_to_file(geo, atoms_cuboid, atoms_inside_bodies, 'out.xyz')


#sph = sphere.sphere.from_dict(geo, d['sphere'])

#atoms = geo.gen_cuboid_from_body(sph)
>>>>>>> MERGE-SOURCE

#in_out_array = numpy.array([1 for x in atoms == 1])

<<<<<<< TREE
in_out_array = poly.atoms_inside(atoms)
=======
#in_out_array = sph.sorting(atoms)
>>>>>>> MERGE-SOURCE

#output.write_structure_to_file(geo, atoms, in_out_array, 'out.xyz')
