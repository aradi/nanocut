'''
Created on Sep 2, 2009

@author: sebastian
'''
import numpy
import body

class convex_polyhedron(body.body):
  '''Class for bodies determined by a group of planes describing it's surface'''

  def __init__(self,geometry,planes_normal,planes_miller,shift_vector,\
               point_inside_body,order=1,shift_vector_coordsys="lattice",
               planes_normal_coordsys="lattice",planes_miller_coordsys="lattice",\
               point_inside_body_coordsys="lattice"):
    '''Initiating body using the lattice determined by geometry-object,\
    planes given by miller indices or normal shape, a point inside the polyhedron\
    and a possible shift_vector to determine it's distance from [0,0,0], as well\
    as each attribute's coordinate system'''
    
    '''Hands body-attributes over to body class'''
    body.body.__init__(self,geometry,shift_vector,order,shift_vector_coordsys)

    '''Reshapes planes in normal form if given proper amount of elements''' 
    try:
      planes_normal.shape=(-1,4)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for planes_normal, check configuration.'
           +'\nExiting...')

    '''Reshapes planes in miller form if given proper amount of elements''' 
    try:
      planes_miller.shape=(-1,4)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for planes_miller, check configuration.'
           +'\nExiting...')
            
    '''Transforms planes determined by miller indices into normal shape'''
    self._planes_miller = numpy.array([numpy.hstack((self.miller_to_normal(geometry,\
          plane[:3]),plane[3])) for plane in planes_miller])
    self._planes_miller.shape=(-1,4)

    '''Appends planes calculated from miller indices to planes in normal form'''
    planes_normal[:,:3] = geometry.coord_transform(planes_normal[:,:3],\
                                                 planes_normal_coordsys)
    self._planes_normal = numpy.vstack((planes_normal,self._planes_miller))

    '''Transforms point given to be inside the shape into proper array'''
    try:
      point_inside_body.shape=(1,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for point_inside_body, check configuration.'
           +'\nExiting...')

    '''Changes point_inside_body's coordinate system if necessary'''
    self._point_inside_body = geometry.coord_transform(point_inside_body,\
                                                  point_inside_body_coordsys)

    '''Distributes True and False values towards point_inside_body's\
    respective position towards each plane'''
    self._parameter = numpy.array([(self._planes_normal[plane_idx,3]-\
          sum(self._point_inside_body[0]*self._planes_normal[plane_idx,:3]))/\
          sum(self._planes_normal[plane_idx,:3]**2) <= 0\
           for plane_idx in range(len(self._planes_normal))])
    
 
  @classmethod  
  def from_dict(cls,geometry,d):
    '''Reads necessary data from dictionary to create proper polyhedron'''
    
    '''Searches for planes determined by miller indices'''
    try:
      planes_miller = numpy.array\
      ([float(el) for el in d.get("planes_miller","").split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_miller not convertible to number, check configuration.'
           +'\nExiting...')
      
    '''Searches for planes given in normal form'''
    try:
      planes_normal = numpy.array\
      ([float(el) for el in d.get("planes_normal","").split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_normal not convertible to number, check configuration.'
           +'\nExiting...')

    '''Searches for shift_vector'''
    try:
      shift_vector = numpy.array\
      ([float(el) for el in d.get("shift_vector","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for shift_vector not convertible to number, check configuration.'
         +'\nExiting...')

    '''Searches for point_inside_body'''
    try:
      point_inside_body = numpy.array\
      ([float(el) for el in d.get("point_inside_body","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
         'Supplied string for point_inside_body not convertible to number, check configuration.'
         +'\nExiting...')

    '''Gathers each attribute's coordinate system'''
    shift_vector_coordsys = d.get("shift_vector_coordsys","lattice")
    point_inside_body_coordsys = d.get("point_inside_body_coordsys", "lattice")
    planes_miller_coordsys = d.get("planes_miller_coordsys", "lattice")
    planes_normal_coordsys = d.get("planes_normal_coordsys", "lattice")
    
    '''Searches for shape's order attribute'''
    try:
      order = int(d.get("order","1"))
    except ValueError:
      exit('Error:\n'+
         'Supplied string for order not convertible to integer'
         +'\nExiting...')
    
    return cls(geometry,planes_normal,planes_miller,shift_vector,point_inside_body,\
               order,shift_vector_coordsys, planes_normal_coordsys,\
               planes_miller_coordsys,point_inside_body_coordsys)
  
  def containing_cuboid(self):
    '''Calculates the boundaries of the cuboid containing the polyhedron'''
    
    corners = numpy.array([0,0,0])
    
    '''Solves a linear equation for each triplet of planes returning their vertex,\
    warns at parallel planes'''
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
            print 'Pair of parallel planes found!'
    
    '''Places extreme points in cuboid and returns cuboid'''
    corners = corners[1:]+self._shift_vector
    cuboid = numpy.zeros((2,3))
    cuboid[0]=corners.min(axis=0)
    cuboid[1]=corners.max(axis=0)
    return cuboid
          
  
  def atoms_inside(self,atoms):
    '''Creates array assigning True and False values to points in and out of\
    plane/s boundaries respectively'''
    
    in_out_array = []
    '''Determines for each point given if it shares the same position related\
    to each plane as the point_in_body'''
    for atom in atoms:
      TF_value = numpy.array([(self._planes_normal[plane_idx,3]-\
          sum((atom[:3]-self._shift_vector)[0]*self._planes_normal[plane_idx,:3]))/\
          sum(self._planes_normal[plane_idx,:3]**2) <= 0\
          for plane_idx in range(len(self._planes_normal))])
      in_out_array.append((TF_value==self._parameter).all())
    
    return in_out_array
                        
  def miller_to_normal(self,geometry,plane_miller):
    '''Calculates the normal form of a plane defined by Miller indices'''
    
    return plane_miller[0]*numpy.cross(geometry._lattice_vectors[1],geometry._lattice_vectors[2])\
    + plane_miller[1]*numpy.cross(geometry._lattice_vectors[2],geometry._lattice_vectors[0])\
    + plane_miller[2]*numpy.cross(geometry._lattice_vectors[0],geometry._lattice_vectors[1])
