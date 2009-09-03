'''
Created on Sep 2, 2009

@author: sebastian
'''
import numpy

class convex_polyeder:
  
  def __init__(self,geometry,planes_normal,planes_miller,shift_vector,\
               point_inside_body,shift_vector_coordsys="lattice",
               planes_normal_coordsys="lattice",planes_miller_coordsys="lattice",\
               point_inside_body_coordsys="lattice"):
    
    try:
      planes_normal.shape=(-1,4)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for planes_normal, check configuration.'
           +'\nExiting...')
      
    try:
      planes_miller.shape=(-1,4)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for planes_miller, check configuration.'
           +'\nExiting...')
            
    self._planes_miller = numpy.array([numpy.hstack((self.miller_to_normal(geometry,\
          planes_miller[plane][:3]),planes_miller[3])) for plane in planes_miller])
    self._planes_miller.shape=(-1,4)

    planes_normal[:,:3] = geometry.coord_transform(planes_normal[:,:3],\
                                                 planes_normal_coordsys)
    self._planes_normal = numpy.vstack((planes_normal,self._planes_miller))

    try:
      shift_vector.shape=(1,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for shift_vector, check configuration.'
           +'\nExiting...')

    try:
      point_inside_body.shape=(1,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for point_inside_body, check configuration.'
           +'\nExiting...')

    self._shift_vector = geometry.coord_transform(shift_vector,\
                                                  shift_vector_coordsys)
    self._point_inside_body = geometry.coord_transform(point_inside_body,\
                                                  point_inside_body_coordsys)

    self._parameter = numpy.array([(self._planes_normal[plane_idx,3]-\
          sum(self._point_inside_body[0]*self._planes_normal[plane_idx,:3]))/\
          sum(self._planes_normal[plane_idx,:3]**2) <= 0\
           for plane_idx in range(len(self._planes_normal))])
 
  @classmethod  
  def from_dict(cls,geometry,d):

    if "convex_polyeder" not in d.keys():
      exit('Error:\n'+
      'convex_polyeder not defined, check configuration.'
      +'\nExiting...')
      
    try:
      planes_normal = numpy.array\
      ([float(el) for el in d["convex_polyeder"].get("planes_normal","").split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_normal not convertible to number, check configuration.'
           +'\nExiting...')
    
    try:
      planes_miller = numpy.array\
      ([float(el) for el in d["convex_polyeder"].get("planes_miller","").split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_miller not convertible to number, check configuration.'
           +'\nExiting...')
  
    try:
      shift_vector = numpy.array\
      ([float(el) for el in d["convex_polyeder"].get("shift_vector","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for shift_vector not convertible to number, check configuration.'
         +'\nExiting...')

    try:
      point_inside_body = numpy.array\
      ([float(el) for el in d["convex_polyeder"].get("point_inside_body","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for point_inside_body not convertible to number, check configuration.'
         +'\nExiting...')

    shift_vector_coordsys = d["convex_polyeder"].get("shift_vector_coordsys","lattice")
    point_inside_body_coordsys = d["convex_polyeder"].get("point_inside_body_coordsys", "lattice")
    planes_miller_coordsys = d["convex_polyeder"].get("planes_miller_coordsys", "lattice")
    planes_normal_coordsys = d["convex_polyeder"].get("planes_normal_coordsys", "lattice")
    
    return cls(geometry,planes_normal,planes_miller,shift_vector,point_inside_body,\
               shift_vector_coordsys, planes_normal_coordsys,\
               planes_miller_coordsys,point_inside_body_coordsys)
  
  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the sphere'''
    
    corners = numpy.array([0,0,0])
#    corners = numpy.linalg.solve(\
#          numpy.vstack((self._planes_normal[0][:3],\
#          self._planes_normal[1][:3],self._planes_normal[2][:3])),\
#          numpy.vstack((self._planes_normal[0][3],\
#          self._planes_normal[1][3],self._planes_normal[2][3])))
    for plane_idx1 in range(0,len(self._planes_normal)):
      for plane_idx2 in range(plane_idx1+1,len(self._planes_normal)):
        for plane_idx3 in range(plane_idx2+1,len(self._planes_normal)):
          try:
            corner = numpy.linalg.solve(\
          numpy.vstack((self._planes_normal[plane_idx1,:3],\
          self._planes_normal[plane_idx2,:3],self._planes_normal[plane_idx3,:3])),\
          numpy.vstack((self._planes_normal[plane_idx1,3],\
          self._planes_normal[plane_idx2,3],self._planes_normal[plane_idx3,3]))).T
            corners = numpy.vstack((corners,corner))
          except numpy.linalg.linalg.LinAlgError:
            print 'Warning, parallel planes detected!'
    
    corners = corners[1:]
    cuboid = numpy.zeros((2,3))
    cuboid[0] = [corners[:,x].min() for x in range(3)]
    cuboid[1] = [corners[:,x].max() for x in range(3)]
    return cuboid
          
  
  def atoms_inside(self,atoms):
    '''Assigns True and False values to points in and out of plane/s boundaries respectively'''
    
    in_out_array = []
    for atom in atoms:
      TF_value = numpy.array([(self._planes_normal[plane_idx,3]-\
          sum(atom[:3]*self._planes_normal[plane_idx,:3]))/\
          sum(self._planes_normal[plane_idx,:3]**2) <= 0\
          for plane_idx in range(len(self._planes_normal))])
      
      in_out_array.append(TF_value.all() == self._parameter.all())
    
    return in_out_array
                        
  def miller_to_normal(self,geometry,plane_miller):
    '''Calculates the normal form of a plane defined by Miller indices'''
    
    return plane_miller[0]*numpy.cross(geometry._lattice_vectors[1],geometry._lattice_vectors[2])\
    + plane_miller[1]*numpy.cross(geometry._lattice_vectors[2],geometry._lattice_vectors[0])\
    + plane_miller[2]*numpy.cross(geometry._lattice_vectors[0],geometry._lattice_vectors[1])