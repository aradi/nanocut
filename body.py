# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2009

@author: sebastian
'''

class body:
  '''Metaclass; all body-classes regardless of shape should be derived from this one.'''
  def __init__(self,geometry,shift_vector,order,shift_vector_coordsys):

    self._order=order
        
    try:
      shift_vector.shape=(1,3)
    except ValueError:
      exit('Error:\n'+
      'Wrong number of elements supplied for shift_vector, check configuration.'
      +'\nExiting...')



    self._shift_vector = geometry.coord_transform(shift_vector, shift_vector_coordsys)

  def get_order(self):
    return self._order
  
  def order_is(self,test_order):
    if self._order==test_order:
      return True
    else:
      return False

  def is_additive(self):
    if self._order>0 and self._order%2!=0:
      return True
    else:
      return False
    
  def is_substractive(self):
    if self._order>0 and self._order%2==0:
        return True
    else:
      return False
    
  def is_ignored(self):
    if self._order<=0:
        return True
    else:
      return False

  def containing_cuboid(self):
    pass
  
  