# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2009

@author: sebastian
'''
import numpy
import body

class periodic_1D_cylinder(body.body):

  #arguments of class defined in the following format:
  #[default, type, shape, is_coord_sys_definable]
  _arguments={
    "radius":[None, "float", None, False],
    "shift_vector":["0 0 0", "array", (1,3), True],
    "order":[1,"integer", None, False]
    }

  def __init__(self,geometry,periodicity,radius,shift_vector=numpy.array([0,0,0]),order=1,shift_vector_coordsys="lattice"):

    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)
    
    self._radius=float(radius)
    
  @classmethod
  def _from_dict_helper(cls,geometry,args,periodicity):
    return cls(geometry,periodicity,args["radius"],args["shift_vector"],args["order"],
               args["shift_vector_coordsys"])


  
  def containing_cuboid(self,periodicity):
    #Calculates the boundaries of the cuboid containing the sphere
    axis=periodicity.get_axis("cartesian")

    
    bounds = numpy.vstack((
            self._shift_vector + self._radius,
            self._shift_vector - self._radius,
            axis + self._shift_vector + self._radius,
            axis + self._shift_vector - self._radius,
            ))
    return numpy.vstack((bounds.min(axis=0),bounds.max(axis=0)))


  
  def atoms_inside(self,atoms,periodicity):
    #Assigns True and False values towards points inside and out of cylinder
       boundaries respectively

    atoms_inside_body=numpy.zeros(atoms.shape[0],bool)
    
    axis=periodicity.get_axis("cartesian")
    
    for index in range(len(atoms)):

      ap = -(self._shift_vector[0])+atoms[index,:3]
      dist = numpy.linalg.norm(numpy.cross(ap,axis))/numpy.linalg.norm(axis)
      atoms_inside_body[index] = self._radius>=dist

    return atoms_inside_body
