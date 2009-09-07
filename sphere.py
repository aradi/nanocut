# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2009

@author: sebastian
'''
import numpy
import body

class sphere(body.body):
  '''Class for bodies of infinite points with a common distance from a center\
  not bigger than a specified radius'''
  def __init__(self,geometry,radius_vector,shift_vector=numpy.array([0,0,0]),order=1,
               radius_vector_coordsys="lattice",shift_vector_coordsys="lattice"):

    '''Initiating body with specific radius_vector, shift_vector (centre)\
     and respective coordinate systems'''
    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)
    
    '''Reshapes radius_vector to proper array if given 3 arguments'''
    try:
      radius_vector.shape=(1,3)
    except ValueError:
      exit('Error:\n'+
      'Wrong number of elements supplied for radius_vector, check configuration.'
      +'\nExiting...')
      
    '''Calculates radius length after transforming into cartesian system if necessary'''
    self._radius = numpy.linalg.norm(geometry.coord_transform(radius_vector,\
                                                    radius_vector_coordsys))
    
    
  @classmethod  
  def from_dict(cls,geometry,d):
      
    '''Searches for radius_vector'''
    try:
      radius_vector = numpy.array([float(el) for el in d["radius_vector"].split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for radius_vector not convertible to number, check configuration.'
           +'\nExiting...')
    
    '''Searches for shift_vector(centre)'''
    try:
      shift_vector = numpy.array([float(el) for el in\
                                  d.get("shift_vector","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for shift_vector not convertible to number, check configuration.'
         +'\nExiting...')

    '''Searches for radius_vector's and shift_vector's default coordinate system'''
    radius_vector_coordsys = d.get("radius_vector_coordsys","lattice")
    shift_vector_coordsys = d.get("shift_vector_coordsys","lattice")

    '''Searches for order of determined sphere'''
    try:
      order = int(d.get("order","1"))
    except ValueError:
      exit('Error:\n'+
         'Supplied string for order not convertible to integer'
         +'\nExiting...')
    
    return cls(geometry,radius_vector,shift_vector,order,\
               radius_vector_coordsys,shift_vector_coordsys)
  
  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the sphere'''
    return self._radius*numpy.array([[-1,-1,-1],[1,1,1]]) + self._shift_vector
  
  def atoms_inside(self,atoms):
    '''Assigns True and False values towards points in and out of sphere boundaries respectively'''

    return numpy.array([numpy.linalg.norm(self._shift_vector-atom[:3])\
                          for atom in atoms]) <= self._radius