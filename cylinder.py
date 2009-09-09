'''
Created on Sep 8, 2009

@author: sebastian
'''
import numpy
import body

class cylinder(body.body):

  #arguments of class defined in the following format:
  #[default, type, shape, is_coord_sys_definable]
  _arguments={
    "point_1":[None, "array", (1,3), True],
    "point_2":[None, "array", (1,3), True],
    "radius":[None, "integer", None, False],
    "radius_2":[None, "integer",None, False],
    "shift_vector":["0 0 0", "array", (1,3), True],
    "order":[1,"integer", None, False]
    }
  
  
  def __init__(self,geometry,point_1, point_2,radius,radius_2,shift_vector=\
               numpy.array([0,0,0]),order=1,point_1_coordsys="lattice",\
               point_2_coordsys="lattice",shift_vector_coordsys="lattice"):

    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)
    
    self._radius = radius
    self._radius_2 = radius_2
    self._point_1 = geometry.coord_transform(point_1,point_1_coordsys)
    self._point_2 = geometry.coord_transform(point_2,point_2_coordsys)
    self._vector = self._point_1 - self._point_2
    self._plane_1 = numpy.hstack((self._vector,sum(self._vector*self._point_1)))
    self._plane_2 = numpy.hstack((self._vector,sum(self._vector*self._point_2)))
    self._norm = numpy.linalg.norm(self._vector)
    self._norm_1 = numpy.linalg.norm(self._plane_1[:3])
    self._norm_2 = numpy.linalg.norm(self._plane_2[:3])
  

  @classmethod
  def _from_dict_helper(cls,geometry,args):
    return cls(geometry,args["point_1"],args["point_2"],args["radius"],\
               args["radius_2"],args["shift_vector"],args["order"],\
               args["point_1_coordsys"],args["point_2_coordsys"],\
               args["shift_vector_coordsys"])
  
  
  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the cylinder'''
    cuboid = numpy.zeros((2,3))
    bounds = numpy.vstack((\
            self._point_1 + self._radius , self._point_1 - self._radius,\
            self._point_2 + self._radius_2 , self._point_2 - self._radius_2))\
            + self._shift_vector
    cuboid[0] = bounds.min(axis=0)
    cuboid[1] = bounds.max(axis=0)
    
    return cuboid
  
  def atoms_inside(self,atoms):
    '''Assigns True and False values towards points in and out of sphere\
     boundaries respectively'''
    in_out_array = []

    for atom in atoms:
      if numpy.linalg.norm(numpy.cross((atom[:3]-self._point_1+self._shift_vector[0]),\
         self._vector))/self._norm\
         <= self._radius -(self._radius-self._radius_2)*\
         abs(sum((atom[:3]-self._point_1+self._shift_vector[0])*self._vector))\
         /self._norm**2\
      and (self._plane_1[3]-sum(self._plane_1[:3]*(atom[:3]+self._shift_vector)[0]))\
      /self._norm_1 >= 0\
      and (self._plane_2[3]-sum(self._plane_2[:3]*(atom[:3]+self._shift_vector)[0]))\
      /self._norm_2 <= 0:
        in_out_array.append(True)
      else:
        in_out_array.append(False)
    return in_out_array