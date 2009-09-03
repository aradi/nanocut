# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2009

@author: sebastian
'''
import numpy
import body

class sphere(body.body):
  
  def __init__(self,geometry,radius_vector,shift_vector=numpy.array([0,0,0]),order=1,
               radius_vector_coordsys="lattice",shift_vector_coordsys="lattice"):


    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)
    
    
    try:
      radius_vector.shape=(1,3)
    except ValueError:
      exit('Error:\n'+
      'Wrong number of elements supplied for radius_vector, check configuration.'
      +'\nExiting...')
      


    self._radius = numpy.linalg.norm(geometry.coord_transform(radius_vector, radius_vector_coordsys))
    
    
    
  @classmethod  
  def from_dict(cls,geometry,d):
      
    try:
      radius_vector = numpy.array([float(el) for el in d["radius_vector"].split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for radius_vector not convertible to number, check configuration.'
           +'\nExiting...')
    
  
    try:
      shift_vector = numpy.array([float(el) for el in d.get("shift_vector","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for shift_vector not convertible to number, check configuration.'
         +'\nExiting...')

    radius_vector_coordsys = d.get("radius_vector_coordsys","lattice")
    shift_vector_coordsys = d.get("shift_vector_coordsys","lattice")

    try:
      order = int(d.get("order","1"))
    except ValueError:
      exit('Error:\n'+
         'Supplied string for order not convertible to integer'
         +'\nExiting...')
    
    return cls(geometry,radius_vector,shift_vector,order,radius_vector_coordsys,shift_vector_coordsys)
  
  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the sphere'''
    return self._radius*numpy.array([[-1,-1,-1],[1,1,1]]) + self._shift_vector
  
  def atoms_inside(self,atoms):
    '''Assigns True and False values towards points in and out of sphere boundaries respectively'''

    return numpy.array([numpy.linalg.norm(self._shift_vector-x[0:3])\
                          for x in atoms]) <= self._radius