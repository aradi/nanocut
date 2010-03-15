# -*- coding: utf-8 -*-
'''
Created on Sep 2, 2009

@author: sebastian
'''
import numpy
import body

class convex_polyhedron(body.body):
  '''Class for bodies determined by a planes describing its boundaries'''

  #arguments of class defined in the following format:
  #[default, type, shape, is_coord_sys_definable]
  _arguments={
    "planes_normal":["0 0 0 0", "array", (-1,4), True],
    "planes_miller":["0 0 0 0", "array", (-1,4), False],
    "shift_vector":["0 0 0", "array", (1,3), True],
    "order":[1,"integer", None, False]
    }

  def __init__(self, geometry, planes_normal, planes_miller, shift_vector,
      order=1, shift_vector_coordsys="lattice", planes_normal_coordsys="lattice"
      ):
    '''Initiating body using the lattice determined by geometry-object,
        planes given by miller indices or normal shape, a point inside the
        polyhedron and a possible shift_vector to determine it's distance from
        [0,0,0], as well as each attribute's coordinate system'''
    
    #Type checking/conversion and initialisation of parent class
    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)

    planes_normal = numpy.array(planes_normal, dtype='float64')
    planes_normal.shape = (-1,4)
    planes_normal[:,:3] = geometry.coord_transform(planes_normal[:,:3],
        planes_normal_coordsys)

    planes_miller = numpy.array(planes_miller, dtype='float64')
    planes_miller.shape = (-1,4)


    #Transforms planes determined by miller indices into normal shape
    self._planes_miller = numpy.array([ numpy.hstack((
        self.miller_to_normal(geometry, plane[:3]), plane[3] ))
        for plane in planes_miller ])

    #Appends planes calculated from miller indices to planes in normal form
    self._planes_normal = numpy.vstack(( planes_normal, self._planes_miller ))

    #Calculates and initalizes body's corners
    self._corners = numpy.array([0,0,0])
    
    #Solves a linear equation for each triplet of planes returning their
    #vertex, warns at parallel planes'''
    for plane_idx1 in range( 0, len( self._planes_normal )):
      for plane_idx2 in range( plane_idx1 + 1, len( self._planes_normal )):
        for plane_idx3 in range( plane_idx2 + 1, len( self._planes_normal )):
          try:
            corner = numpy.linalg.solve(
                numpy.vstack((
                    self._planes_normal[plane_idx1,:3],
                    self._planes_normal[plane_idx2,:3],
                    self._planes_normal[plane_idx3,:3]
                    )),
                numpy.vstack((
                    self._planes_normal[plane_idx1,3],
                    self._planes_normal[plane_idx2,3],
                    self._planes_normal[plane_idx3,3]
                    ))
                ).T
            self._corners = numpy.vstack(( self._corners, corner ))
          except numpy.linalg.linalg.LinAlgError:
            print 'Pair of parallel planes found!'
    
    #Places extreme points in cuboid and returns cuboid
    self._corners = self._corners[1:] + self._shift_vector
    
  
  @classmethod  
  def _from_dict_helper(cls, geometry, args, periodicity=None):
    return cls(geometry, args["planes_normal"], args["planes_miller"],
        args["shift_vector"], args["order"],
        args["shift_vector_coordsys"], args["planes_normal_coordsys"])

  def containing_cuboid(self, periodicity=None):
    '''Calculates the boundaries of the cuboid containing the polyhedron'''
    
    return numpy.vstack(( self._corners.min(axis=0), self._corners.max(axis=0) ))
          
  
  def atoms_inside(self, atoms, periodicity=None):
    '''Creates array assigning True and False values to points in and out of
        each plane's boundaries respectively'''
    
    #Calculates point_inside_body
    point_inside_body = numpy.array([0,0,0])
    
    for corner in self._corners:
      point_inside_body = (point_inside_body + corner)
    point_inside_body = (point_inside_body /
         self._corners.shape[0])
    
    #Distributes True and False values towards point_inside_body's respective
    #position towards each plane
    parameter = numpy.array([
        (self._planes_normal[plane_idx,3] - numpy.dot( (point_inside_body
        - self._shift_vector)[0], self._planes_normal[plane_idx,:3] ) ) <= 0
            for plane_idx in range( len( self._planes_normal ))
        ])
    
    atoms_inside_body = numpy.zeros(atoms.shape[0], bool)
    #Determines for each point given if it shares the same position related
    #to each plane as the point_in_body
    for index in range(len(atoms)):
      TF_value = numpy.array([
          (self._planes_normal[plane_idx,3] - numpy.dot( ( atoms[index,:3] -
              self._shift_vector )[0], self._planes_normal[plane_idx,:3] ) )
              <= 0
          for plane_idx in range( len( self._planes_normal ))
          ])
      atoms_inside_body[index] = ( TF_value == parameter.T ).all()
    
    return atoms_inside_body
                        
  def miller_to_normal(self, geometry, plane_miller):
    '''Calculates the normal form of a plane defined by Miller indices'''
    
    return (plane_miller[0] * numpy.cross( geometry._lattice_vectors[1],
        geometry._lattice_vectors[2] ) + plane_miller[1] * numpy.cross(
        geometry._lattice_vectors[2], geometry._lattice_vectors[0] ) +
        plane_miller[2] * numpy.cross( geometry._lattice_vectors[0], 
        geometry._lattice_vectors[1] ) )