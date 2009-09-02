'''
Created on Sep 2, 2009

@author: sebastian
'''
import numpy

class planes:
  
  def __init__(self,geometry,planes_normal,planes_miller,shift_vector,
               shift_vector_coordsys="lattice"):
    
    try:
      planes_normal.shape=(1,4)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for planes_normal, check configuration.'
           +'\nExiting...')
      
    try:
      planes_miller.shape=(1,4)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for planes_miller, check configuration.'
           +'\nExiting...')
            
    self._planes_miller = numpy.hstack((miller_to_normal(geometry,planes_miller)\
                                        ,planes_miller[3]))
    
    self._planes_normal = numpy.vstack((planes_normal,self._planes_miller))

    try:
      shift_vector.shape=(1,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for shift_vector, check configuration.'
           +'\nExiting...')

    self._shift_vector = geometry.coord_transform(shift_vector, shift_vector_coordsys)
    
    self._parameter = (self._planes_normal[4]-sum(self._shift_vector*\
                self._planes_normal[:3]))/sum(self._planes_normal[:3]**2) <= 0

  @classmethod  
  def from_dict(cls,geometry,d):

    if "planes" not in d.keys():
      exit('Error:\n'+
      'planes not defined, check configuration.'
      +'\nExiting...')
      
    try:
      planes_normal = numpy.array\
      ([float(el) for el in d["planes"]["planes_normal"].split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_normal not convertible to number, check configuration.'
           +'\nExiting...')
    
    try:
      planes_miller = numpy.array\
      ([float(el) for el in d["planes"]["planes_miller"].split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_miller not convertible to number, check configuration.'
           +'\nExiting...')
  
    try:
      shift_vector = numpy.array\
      ([float(el) for el in d["planes"].get("shift_vector","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for shift_vector not convertible to number, check configuration.'
         +'\nExiting...')

    shift_vector_coordsys = d["sphere"].get("shift_vector_coordsys","lattice")

    return cls(geometry,planes_normal,planes_miller,shift_vector,\
               shift_vector_coordsys)
  
  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the sphere'''
    return self._radius*numpy.array([[-1,-1,-1],[1,1,1]]) + self._shift_vector
  
  def sorting(self,atoms):
    '''Assigns True and False values towards points in and out of plane/s boundaries respectively'''
    
    in_out_array = []
    for atom in atoms:
      TF_value = (self._planes_normal[4]-sum(atom[:3]*\
                self._planes_normal[:3]))/sum(self._planes_normal[:3]**2) <= 0
      in_out_array.append(TF_value == self._parameter)
      
    return in_out_array
                        
  def miller_to_normal(self,geometry,planes_miller):
    '''Calculates the normalform of a plane defined by Miller indices'''
    return planes_miller[0]*numpy.cross(geometry._lattice_vectors[1],geometry._lattice_vectors[2])\
    + planes_miller[1]*numpy.cross(geometry._lattice_vectors[2],geometry._lattice_vectors[0])\
    + planes_miller[2]*numpy.cross(geometry._lattice_vectors[0],geometry._lattice_vectors[1])
    