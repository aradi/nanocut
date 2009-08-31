from numpy import array, dot

class convex_polyeder:
  '''Self-defined class for handling crystal structure,
  containing unit-cell-vectors, atoms and kinds of atoms '''

  def __init__(self,geometry,planes_miller,planes_normal,shift_vector,
               planes_miller_coordsys="lattice",planes_normal_coordsys="lattice",
               shift_vector_coordsys="lattice"):
    
#TODO transform miller to normal
#TODO separate distance value from normal vectors
#    self.planes_normal = geometry.coord_transform(planes_normal, planes_normal_coordsys)
#    self.shift_vector = geometry.coord_transform(shift_vectors, planes_normal_coordsys)
#TODO transform all to cartesian
    pass
  
  
  @classmethod
  def from_dict(cls,geometry,d):
    '''Reads planes from dict. Returns (object)'''
  
    if "convex_polyeder" not in d.keys():
      exit('Error:\n'+
      'convex_polyeder not defined, check configuration.'
      +'\nExiting...')
    
    try:
      planes_miller = array([float(el) for el in d["convex_polyeder"].get("planes_miller","").split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_miller not convertible to numbers, check configuration.'
           +'\nExiting...')
    
    try:
      planes_normal = array([float(el) for el in d["convex_polyeder"].get("planes_normal","").split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for planes_normal not convertible to numbers, check configuration.'
           +'\nExiting...')
  
    try:
      shift_vector = array([float(el) for el in d["convex_polyeder"].get("shift_vector","0 0 0").split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for shift_vector not convertible to numbers, check configuration.'
           +'\nExiting...')

    planes_miller_coordsys = d["convex_polyeder"].get("planes_miller_coordsys", "lattice")
    planes_normal_coordsys = d["convex_polyeder"].get("planes_normal_coordsys", "lattice")
    shift_vector_coordsys = d["convex_polyeder"].get("shift_vector_coordsys", "lattice")
    
    return cls(geometry,planes_miller,planes_normal,shift_vector,planes_miller_coordsys,
               planes_normal_coordsys,shift_vector_coordsys)