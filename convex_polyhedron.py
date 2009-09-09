# -*- coding: utf-8 -*-
'''
Created on Sep 2, 2009

@author: sebastian
'''
import numpy
import body

class convex_polyhedron(body.body):
  '''Class for bodies determined by a group of planes describing it's surface'''

  #arguments of class defined in the following format:
  #[default, type, shape, is_coord_sys_definable]
  _arguments={
    "planes_normal":["0 0 0 0", "array", (-1,4), True],
    "planes_miller":["0 0 0 0", "array", (-1,4), False],
    "point_inside_body":[None, "array", (1,3), True],
    "shift_vector":["0 0 0", "array", (1,3), True],
    "order":[1,"integer", None, False]
    }

  def __init__(self,geometry,planes_normal,planes_miller,shift_vector,\
               point_inside_body,order=1,shift_vector_coordsys="lattice",
               planes_normal_coordsys="lattice",\
               point_inside_body_coordsys="lattice"):
    '''Initiating body using the lattice determined by geometry-object,\
    planes given by miller indices or normal shape, a point inside the polyhedron\
    and a possible shift_vector to determine it's distance from [0,0,0], as well\
    as each attribute's coordinate system'''
    
    '''Type checking/conversion and initialisation of parent class'''
    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)

    point_inside_body=numpy.array(point_inside_body,dtype='float64')
    point_inside_body.shape=(1,3)

    planes_normal=numpy.array(planes_normal,dtype='float64')
    planes_normal.shape=(-1,4)

    planes_miller=numpy.array(planes_miller,dtype='float64')
    planes_miller.shape=(-1,4)



    '''Transforms planes determined by miller indices into normal shape'''
    self._planes_miller = numpy.array([numpy.hstack((self.miller_to_normal(geometry,\
          plane[:3]),plane[3])) for plane in planes_miller])


    '''Appends planes calculated from miller indices to planes in normal form'''
    planes_normal[:,:3] = geometry.coord_transform(planes_normal[:,:3],\
                                                 planes_normal_coordsys)
    self._planes_normal = numpy.vstack((planes_normal,self._planes_miller))


    
    '''Changes point_inside_body's coordinate system if necessary'''
    self._point_inside_body = geometry.coord_transform(point_inside_body,\
                                                  point_inside_body_coordsys)

    '''Distributes True and False values towards point_inside_body's\
    respective position towards each plane'''
    self._parameter = numpy.array([(self._planes_normal[plane_idx,3]-\
          sum(self._point_inside_body[0]*self._planes_normal[plane_idx,:3]))/\
          sum(self._planes_normal[plane_idx,:3]**2) <= 0\
           for plane_idx in range(len(self._planes_normal))])
    
 
  @classmethod  
  def _from_dict_helper(cls,geometry,args):
    return cls(geometry,args["planes_normal"],args["planes_miller"],\
               args["shift_vector"],args["point_inside_body"],args["order"],\
               args["shift_vector_coordsys"],args["planes_normal_coordsys"],\
               args["point_inside_body_coordsys"])

  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the polyhedron'''
    
    corners = numpy.array([0,0,0])
    
    '''Solves a linear equation for each triplet of planes returning their vertex,\
    warns at parallel planes'''
    for plane_idx1 in range(0,len(self._planes_normal)):
      for plane_idx2 in range(plane_idx1+1,len(self._planes_normal)):
        for plane_idx3 in range(plane_idx2+1,len(self._planes_normal)):
          try:
            corner = numpy.linalg.solve(\
          numpy.vstack((self._planes_normal[plane_idx1,:3],\
          self._planes_normal[plane_idx2,:3],self._planes_normal[plane_idx3,:3])),\
          numpy.vstack((self._planes_normal[plane_idx1,3],\
          self._planes_normal[plane_idx2,3],self._planes_normal[plane_idx3,3]))).T
            corners = numpy.vstack((corners,corner))
          except numpy.linalg.linalg.LinAlgError:
            print 'Pair of parallel planes found!'
    
    '''Places extreme points in cuboid and returns cuboid'''
    corners = corners[1:]+self._shift_vector
    cuboid = numpy.zeros((2,3))
    cuboid[0]=corners.min(axis=0)
    cuboid[1]=corners.max(axis=0)
    return cuboid
          
  
  def atoms_inside(self,atoms):
    '''Creates array assigning True and False values to points in and out of\
    plane/s boundaries respectively'''
    
    atoms_inside_body=numpy.zeros(atoms[:,3].shape,bool)
    '''Determines for each point given if it shares the same position related\
    to each plane as the point_in_body'''
    for index in range(len(atoms)):
      TF_value = numpy.array([(self._planes_normal[plane_idx,3]-\
          sum((atoms[index,:3]-self._shift_vector)[0]*self._planes_normal[plane_idx,:3]))/\
          sum(self._planes_normal[plane_idx,:3]**2) <= 0\
          for plane_idx in range(len(self._planes_normal))])
      atoms_inside_body[index]=(TF_value==self._parameter).all()
    
    return atoms_inside_body
                        
  def miller_to_normal(self,geometry,plane_miller):
    '''Calculates the normal form of a plane defined by Miller indices'''
    
    return plane_miller[0]*numpy.cross(geometry._lattice_vectors[1],geometry._lattice_vectors[2])\
    + plane_miller[1]*numpy.cross(geometry._lattice_vectors[2],geometry._lattice_vectors[0])\
    + plane_miller[2]*numpy.cross(geometry._lattice_vectors[0],geometry._lattice_vectors[1])
