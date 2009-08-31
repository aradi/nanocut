'''
Created on Aug 31, 2009

@author: sebastian
'''
import numpy
# import geometry
class sphere:
  
  def __init__(self,geometry,radius_vector,shift_vector,
               radius_vector_coordsys="lattice",shift_vector_coordsys="lattice"):
    
    try:
      radius_vector.shape=(1,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for radius_vector, check configuration.'
           +'\nExiting...')
      
    try:
      shift_vector.shape=(1,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for shift_vector, check configuration.'
           +'\nExiting...')

    self._radius = numpy.linalg.norm(geometry.coord_transform(radius_vector, radius_vector_coordsys))
    
    self._shift_vector = geometry.coord_transform(shift_vector, shift_vector_coordsys)
    
    
  @classmethod  
  def from_dict(cls,geometry,d):

    if "sphere" not in d.keys():
      exit('Error:\n'+
      'sphere not defined, check configuration.'
      +'\nExiting...')
      
    try:
      radius_vector = numpy.array([float(el) for el in d["sphere"]["radius_vector"].split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for radius_vector not convertable to number, check configuration.'
           +'\nExiting...')
    
  
    try:
      shift_vector = numpy.array([float(el) for el in d["sphere"].get("shift_vector","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for shift_vector not convertable to number, check configuration.'
         +'\nExiting...')

    radius_vector_coordsys = d["sphere"].get("radius_vector_coordsys","lattice")
    shift_vector_coordsys = d["sphere"].get("shift_vector_coordsys","lattice")

    return cls(geometry,radius_vector,shift_vector,radius_vector_coordsys,shift_vector_coordsys)