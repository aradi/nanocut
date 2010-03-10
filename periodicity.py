# -*- coding: utf-8 -*-
import numpy


def gcd(a,b,c):
  while b:
    a, b = b, a % b
  while c:
    a, c = c, a % c
  return a


class periodicity:
  

  def __init__(self,geometry,period_type,axis=None,plane=None,plane_thickness=None):

    if period_type=="0D":
      self._period_type="0D"

    elif period_type=="1D":
      self._period_type="1D"
      
      axis=numpy.array(axis,dtype='int')
      axis.shape=(1,3)

      if (axis==numpy.array([[0,0,0]])).all():
        axis=None
      self._axis = axis/gcd(axis[0,0],axis[0,1],axis[0,2])
      self._axis_cart=geometry.coord_transform(axis, "lattice")

    elif period_type=="2D":
      self._period_type="2D"
      
      axis=numpy.array(axis,dtype='int')
      axis.shape=(2,3)

      if (axis==numpy.array([[0,0,0]])).all():
        axis=None
      self._axis = numpy.vstack((axis[1]/gcd(axis[1,0],axis[1,1],axis[1,2]),
                                 axis[0]/gcd(axis[0,0],axis[0,1],axis[0,2])))
      self._axis_cart=geometry.coord_transform(axis, "lattice")

    else:
      #TODO: Raise Exeption
      exit('InternalError:\n'+
           'No valid period_type given.'
           +'\nExiting...\n')

  def get_axis(self,coordsys="lattice"):
    if (self._period_type=="1D" or self._period_type=="2D"):
      if coordsys=="lattice":
        return self._axis
      elif coordsys=="cartesian":
        return self._axis_cart
      else:
        #TODO: Raise Exeption
        exit('InternalError:\n'+
           'No valid coordinate system given.'
           +'\nExiting...\n')
    else:
      #TODO: Raise Exeption
      exit('InternalError:\n'+
           'get_axis() called, but period_type is not 1D or 2D.'
           +'\nExiting...\n')

  def period_type_is(self,testtype):
    return self._period_type==testtype



  @classmethod
  def from_dict(cls,geometry,d):
    #Reads periodicity from dict
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
          axis.shape=(1,6)
        except ValueError:
          exit('Error:\n'+
          'Wrong number of elements supplied for axis.'
           +'\nExiting...\n')
        
        return cls(geometry,"2D",axis)