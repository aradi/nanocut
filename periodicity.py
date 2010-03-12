# -*- coding: utf-8 -*-
import numpy

def gcd(a,b,c):
  '''Return greatest common divisor.'''
  while b:
    a, b = b, a % b
  while c:
    a, c = c, a % c
  return a


class periodicity:
  '''Class holding information about type of periodicity, and axes.'''  
  def __init__(self,geometry,period_type,axis=None):

    if period_type=="0D":
      self._period_type="0D"

    else:
      axis=numpy.array(axis,dtype='int')
      axis.shape=(-1,3)

      if period_type=="1D":
        self._period_type="1D"

        if (axis==0).all():
          raise ValueError, "Value of axis is invalid."

        #shorten axis if possible by division with gcd
        self._axis = axis/gcd(axis[0,0],axis[0,1],axis[0,2])

      elif period_type=="2D":
        self._period_type="2D"

        if ((axis[0]==0).all() or axis[1]==0).all():
          raise ValueError, "Value of axis is invalid."

        #shorten axes if possiple by division with gcd
        self._axis = numpy.vstack((axis[1]/gcd(axis[1,0],axis[1,1],axis[1,2]),
                                   axis[0]/gcd(axis[0,0],axis[0,1],axis[0,2])))

      else:
        raise ValueError, "Value of period_type is invalid."

      self._axis_cart=geometry.coord_transform(self._axis, "lattice")

  def get_axis(self,coordsys="lattice"):
    '''Returns axis'''
    if (self._period_type=="1D" or self._period_type=="2D"):
      if coordsys=="lattice":
        return self._axis
      elif coordsys=="cartesian":
        return self._axis_cart
      else:
        raise ValueError, "Value of coordsys is invalid."
    else:
      raise ValueError, "get_axis() called, but period_type is not 1D or 2D."
      
  def period_type_is(self,testtype):
    '''Returns True if argument matches period_type.'''
    return self._period_type==testtype

  def arrange_positions(self, atoms_coords, atoms_idx):
    '''Put atoms in periodic structures in proper position'''
    
    if self.period_type_is("1D"):
      axis_norm=numpy.linalg.norm(self._axis)
      for idx in range(atoms_idx.shape[0]):
        ndist=numpy.floor(numpy.dot(atoms_coords[idx], self._axis.T/axis_norm)/axis_norm)-1
        atoms_coords[idx]=atoms_coords[idx]-ndist*self._axis

  @classmethod
  def from_dict(cls,geometry,d):
    '''Reads periodicity from dict and checks data types'''
    if "periodicity" not in d.keys():
      return cls(geometry,"0D")

    else:
      period_type = d["periodicity"].get("period_type","0D")
      
      if period_type=="0D":
        return cls(geometry,"0D")
        
        
      elif period_type=="1D":
        
        axis = d["periodicity"].get("axis",None)
        
        if axis==None:
          exit('Error:\n'+
           'Item axis not specified but needed.'
           +'\nExiting...\n')
        try:
          axis=numpy.array([int(el) for el in axis.split()])
        except ValueError:
          exit('Error:\n'+
           'Supplied string for axis not convertible to integer-array.'
           +'\nExiting...\n')
        
        try:
          axis.shape=(1,3)
        except ValueError:
          exit('Error:\n'+
          'Wrong number of elements supplied for axis.'
           +'\nExiting...\n')
        
        if (axis==0).all():
          exit('Error:\n'+
          'Value of axis is invalid.'
          +'\nExiting...\n')

        return cls(geometry,"1D",axis)


      elif period_type=="2D":
        
        axis = d["periodicity"].get("axis",None)
        
        if axis==None:
          exit('Error:\n'+
           'Item axis not specified but needed.'
           +'\nExiting...\n')
        try:
          axis=numpy.array([int(el) for el in axis.split()])
        except ValueError:
          exit('Error:\n'+
           'Supplied string for axis not convertible to integer-array.'
           +'\nExiting...\n')
        
        try:
          axis.shape=(2,3)
        except ValueError:
          exit('Error:\n'+
          'Wrong number of elements supplied for axis.'
           +'\nExiting...\n')
        
        if ((axis[0]==0).all() or axis[1]==0).all():
          exit('Error:\n'+
          'Value of axis is invalid.'
          +'\nExiting...\n')

        return cls(geometry,"2D",axis)