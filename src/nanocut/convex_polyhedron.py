import numpy as np
import body
import nanocut.common as nc

class convex_polyhedron(body.body):
  '''Class for bodies determined by a planes describing its boundaries'''

  #arguments of class defined in the following format:
  #[default, type, shape, is_coord_sys_definable]
  _arguments={
    "planes_normal":["0 0 0 0", "array", (-1,4), True],
    "planes_miller":["0 0 0 0", "array", (-1,4), False],
    "shift_vector":["0 0 0", "array", (1,3), True],
    "order":[1,"integer", None, False]
    }

  def __init__(self, geometry, planes_normal, planes_miller, shift_vector,
      order=1, shift_vector_coordsys="lattice", planes_normal_coordsys="lattice"
      ):
    '''Initiating body using the lattice determined by geometry-object,
        planes given by miller indices or normal shape, a point inside the
        polyhedron and a possible shift_vector to determine it's distance from
        [0,0,0], as well as each attribute's coordinate system'''
    
    #Type checking/conversion and initialisation of parent class
    body.body.__init__(self, geometry, shift_vector, order,
                       shift_vector_coordsys)

    if np.all(planes_normal == 0):
      pass
    else:
      planes_normal = np.array(planes_normal, dtype=np.float64)
      planes_normal[:,:3] = geometry.coord_transform(planes_normal[:,:3],
          planes_normal_coordsys)
      for plane in planes_normal:
        if np.all(abs(plane[:3]) < 1e-12):
          raise ValueError, "Bad input: empty normal vector"

    if np.all(planes_miller == 0):
      pass
    else:
      planes_miller = np.array(planes_miller, dtype=np.float64)
      for plane in planes_miller:
        if np.all(abs(plane[:3]) < 1e-12):
          raise ValueError, "Bad input: empty miller plane"

      #Transforms planes determined by miller indices into normal shape
      planes_miller[:,0:3] = nc.miller_to_normal(geometry._lattice_vectors,
                                                 planes_miller[:,0:3])

    # Appends planes calculated from miller indices to planes in normal form
    self._planes_normal = np.vstack(( planes_normal, planes_miller ))
    if np.all(abs(self._planes_normal[:,:3]) < 1e-12):
      exit('Error:\nNo proper planes specified.\nExiting...\n')
    
    # Removes empty (dummy) planes and normalizes others
    idx = 0
    while idx < self._planes_normal.shape[0]:
      if np.all(abs(self._planes_normal[idx,:3]) < 1e-12):
        self._planes_normal = np.delete(self._planes_normal, idx, 0)
      else:
        idx += 1
    norms = np.sqrt(np.sum(self._planes_normal[:,0:3]**2, axis=1))
    self._planes_normal[:,0:3] /= norms[:,np.newaxis] 

    # Removes identical planes
    idx1 = 0
    idx2 = 1
    while idx1 < self._planes_normal.shape[0] - 1:
      while idx2 < self._planes_normal.shape[0]:
        ddiff = self._planes_normal[idx1,3] - self._planes_normal[idx2,3]
        cross = np.cross(self._planes_normal[idx1,:3],
                         self._planes_normal[idx2,:3])
        vsum = self._planes_normal[idx1,:3] + self._planes_normal[idx2,:3]
        if (abs(ddiff) < 1e-12 and np.all(abs(cross) < 1e-12) 
            and np.all(abs(vsum) > 1e-12)): 
          self._planes_normal = np.delete(self._planes_normal, idx2, 0)
        else:
          idx2 += 1
      idx1 += 1
      idx2 = idx1 + 1
    
    # Calculates and initalizes body's corners
    self._corners = []
    
    # Solves a linear equation for each triplet of planes returning their
    # vertex, warns at parallel planes'''
    for plane_idx1 in range(0, len( self._planes_normal)):
      for plane_idx2 in range(plane_idx1 + 1, len( self._planes_normal)):
        for plane_idx3 in range(plane_idx2 + 1, len( self._planes_normal)):
          try:
            corner = np.linalg.solve(
                np.vstack((
                    self._planes_normal[plane_idx1,:3],
                    self._planes_normal[plane_idx2,:3],
                    self._planes_normal[plane_idx3,:3]
                    )),
                np.vstack((
                    self._planes_normal[plane_idx1,3],
                    self._planes_normal[plane_idx2,3],
                    self._planes_normal[plane_idx3,3]
                    )
                ))
            self._corners.append(corner.flatten())
          except np.linalg.linalg.LinAlgError:
            pass
    self._corners = np.array(self._corners)
    
    if np.all(len(self._corners) < 6 or abs(self._corners) < 1e-12):
      exit('Error:\nNo or insufficient corners found.\nExiting...\n')

    self._corners += self._shift_vector
    
  
  @classmethod  
  def _from_dict_helper(cls, geometry, args, periodicity=None):
    return cls(geometry, args["planes_normal"], args["planes_miller"],
        args["shift_vector"], args["order"],
        args["shift_vector_coordsys"], args["planes_normal_coordsys"])

  def containing_cuboid(self, periodicity=None):
    '''Calculates the boundaries of the cuboid containing the polyhedron'''
    
    return np.vstack(( self._corners.min(axis=0), self._corners.max(axis=0) ))
          
  
  def atoms_inside(self, atoms, periodicity=None):
    '''Creates array assigning True and False values to points in and out of
        each plane's boundaries respectively'''
    
    # Calculates point_inside_body
    point_inside_body = (np.sum(self._corners, axis=0) 
                         / float(len(self._corners)))
    point_inside_body -= self._shift_vector[0]
    
    atoms_relative = np.transpose(atoms[:,:3] - self._shift_vector[0])
    sign_point = (self._planes_normal[:,3] 
                  - np.dot(self._planes_normal[:,:3], point_inside_body)) <= 0.0
    sign_atoms = (self._planes_normal[:,3,np.newaxis] 
                  - np.dot(self._planes_normal[:,:3], atoms_relative)) <= 0.0
    compared = (sign_atoms == sign_point[:,np.newaxis])
    atoms_inside_body = [ np.all(compared[:,ii]) for ii in range(len(atoms)) ]
    return np.array(atoms_inside_body, bool)
