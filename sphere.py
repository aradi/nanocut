# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2009

@author: sebastian
'''
import numpy
import body

class sphere(body.body):

  #arguments of class defined in the following format:
  #[default, type, shape, is_coord_sys_definable]
  _arguments={
    "radius_vector":[None, "array", (1,3), True],
    "shift_vector":["0 0 0", "array", (1,3), True],
    "order":[1,"integer", None, False]
    }
  #_init_arguments=['radius_vector','shift_vector','order','radius_vector_coordsys','shift_vector_coordsys']
  
  
  def __init__(self,geometry,radius_vector,shift_vector=numpy.array([0,0,0]),order=1,
               radius_vector_coordsys="lattice",shift_vector_coordsys="lattice"):

    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)
    
    radius_vector=numpy.array(radius_vector,dtype='float64')
    radius_vector.shape=(1,3)
    radius_vector=geometry.coord_transform(radius_vector, radius_vector_coordsys)

    self._radius = numpy.linalg.norm(radius_vector)
  
  @classmethod
  def _from_dict_helper(cls,geometry,args,periodicity=None):
    return cls(geometry,args["radius_vector"],args["shift_vector"],args["order"],
               args["radius_vector_coordsys"],args["shift_vector_coordsys"])
    
  
  
  
  def containing_cuboid(self,periodicity=None):
    #Calculates the boundaries of the cuboid containing the sphere
    return self._radius*numpy.array([[-1,-1,-1],[1,1,1]]) + self._shift_vector
  
  def atoms_inside(self,atoms,periodicity=None):
    #Assigns True and False values towards points in and out of sphere boundaries respectively

    return numpy.array([numpy.linalg.norm(self._shift_vector-x[0:3])\
                          for x in atoms]) <= self._radius
