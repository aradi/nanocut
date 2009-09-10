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
    "radius_1":[None, "float", None, False],
    "radius_2":[None, "float",None, False],
    "shift_vector":["0 0 0", "array", (1,3), True],
    "order":[1,"integer", None, False]
    }
  
  
  def __init__(self,geometry,point_1, point_2,radius_1,radius_2,shift_vector=\
               numpy.array([0,0,0]),order=1,point_1_coordsys="lattice",\
               point_2_coordsys="lattice",shift_vector_coordsys="lattice"):

    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)
    
    self._radius_1 = float(radius_1)
    self._radius_2 = float(radius_2)

    point_1=numpy.array(point_1,dtype='float64')
    point_1.shape=(1,3)
    self._point_1 = geometry.coord_transform(point_1,point_1_coordsys)

    point_2=numpy.array(point_2,dtype='float64')
    point_2.shape=(1,3)
    self._point_2 = geometry.coord_transform(point_2,point_2_coordsys)
    self._dir_vector = self._point_2 - self._point_1
    self._norm = numpy.linalg.norm(self._dir_vector)
  

  @classmethod
  def _from_dict_helper(cls,geometry,args):
    return cls(geometry,args["point_1"],args["point_2"],args["radius_1"],\
               args["radius_2"],args["shift_vector"],args["order"],\
               args["point_1_coordsys"],args["point_2_coordsys"],\
               args["shift_vector_coordsys"])
  
  
  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the cylinder'''
    cuboid = numpy.zeros((2,3))
    bounds = numpy.vstack((\
            self._point_1 + self._radius_1 , self._point_1 - self._radius_1,\
            self._point_2 + self._radius_2 , self._point_2 - self._radius_2))\
            + self._shift_vector
    cuboid[0] = bounds.min(axis=0)
    cuboid[1] = bounds.max(axis=0)
    
    return cuboid
  
  def atoms_inside(self,atoms):
    '''Assigns True and False values towards points in and out of sphere\
     boundaries respectively'''

    atoms_inside_body=numpy.zeros(atoms[:,3].shape,bool)
    
    for index in range(len(atoms)):

      ap = -(self._point_1+self._shift_vector[0])+atoms[index,:3]
      dist = numpy.linalg.norm(numpy.cross(ap,self._dir_vector))/self._norm
      ln = numpy.dot(ap,self._dir_vector.T)/self._norm**2
      rad_at_l = self._radius_1+ln*(self._radius_2-self._radius_1)
      atoms_inside_body[index] = rad_at_l>=dist and ln>=0 and ln<=1


    return atoms_inside_body
