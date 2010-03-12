#!usr/bin/python
# -*- coding: utf-8 -*-

#Import public modules

import sys, numpy, getopt


#Import own modules
import inout, geometry, sphere, convex_polyhedron, cylinder,\
    periodic_1D_cylinder, periodic_1D_convex_prism, periodicity

#Hands user's files to inout module
inputfilename, writefilenames, appendfilenames = inout.parse_args(sys.argv)

#Parse configuration from ini-file and store it in a config_ini-object.
config_ini = inout.read_ini(inputfilename)

#Read configuration from config_ini and write it into a (dict) config_dict.
config_dict = inout.ini2dict(config_ini)


#Initialise geometry-object from config_dict
geo = geometry.geometry.from_dict(config_dict)

#Initialise periodicity-object form config_dict
period = periodicity.periodicity.from_dict(geo,config_dict)

#Initialise body objects and store references in bodies list
bodies = []
if period.period_type_is("0D"):
  for body in config_dict.keys():
    if body.startswith('sphere'):
      body = sphere.sphere.from_dict(geo, config_dict[body])
      bodies.append(body)
    elif body.startswith('convex_polyhedron'):
      body = convex_polyhedron.convex_polyhedron.from_dict(geo,
          config_dict[body])
      bodies.append(body)
    elif body.startswith('cylinder'):
      body = cylinder.cylinder.from_dict(geo, config_dict[body])
      bodies.append(body)
      
elif period.period_type_is("1D"):
  for body in config_dict:
    if body.startswith('periodic_1D_cylinder'):
      body = periodic_1D_cylinder.periodic_1D_cylinder.from_dict(geo,
          config_dict[body], period)
      bodies.append(body)
    elif body.startswith('periodic_1D_convex_prism'):
      body = periodic_1D_convex_prism.periodic_1D_convex_prism.from_dict(geo,
          config_dict[body], period)
      bodies.append(body)


elif period.period_type_is("2D"):
  for body in config_dict:
    if body.startswith('periodic_2D_plane'):
      body = periodic_2D_plane.periodic_2D_plane.from_dict(geo,
          config_dict[body], period)
      bodies.append(body)

else:
  exit("Could not determine type of periodicity. This should never happen.")

if len(bodies) == 0:
    print ('Warning:\n'+
      'No bodies specified.'
      +'\nExiting...')
    exit()


#Get boundaries of the cuboid containing all bodies
cuboid_boundaries = numpy.vstack(( [ body.containing_cuboid(period)
    for body in bodies if body.is_additive() ] ))

cuboid_boundaries = numpy.vstack(( [ cuboid_boundaries.max(axis=0),
    cuboid_boundaries.min(axis=0) ] ))

print cuboid_boundaries
#Generate lattice-cuboid
lattice_cuboid = geo.gen_cuboid(cuboid_boundaries,period)


#Generate cuboid containing all atoms/ Distribute atoms to lattice points
atoms_coords, atoms_idx = geo.gen_atoms(lattice_cuboid)


#Decide which atoms are inside the specified set of bodies.

#Find the highest order

max_order = max([ body.get_order() for body in bodies ])

#Test for atoms inside bodies in the right order.
atoms_inside_bodies = numpy.zeros(atoms_coords.shape[0], bool)

for order in range( 1, max_order + 1):
  
  for body in bodies:
    
    if body.order_is(order):
      tmp_atoms_inside_bodies = body.atoms_inside(atoms_coords,period)
      #Add and substract each body depending on order
      if order%2!=0:
	atoms_inside_bodies = atoms_inside_bodies + tmp_atoms_inside_bodies
      else:
	atoms_inside_bodies = ((atoms_inside_bodies + tmp_atoms_inside_bodies)
	      - tmp_atoms_inside_bodies)

#Forget atoms outside bodies
atoms_coords = atoms_coords[atoms_inside_bodies]
atoms_idx = atoms_idx[atoms_inside_bodies]

#Put atoms in periodic structures in proper position
period.arrange_positions(geo, atoms_coords, atoms_idx)

#Write final crystal to file
inout.write_crystal(geo,atoms_coords, atoms_idx,
writefilenames, appendfilenames)
