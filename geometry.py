from numpy import array, dot, matrix, asarray

class geometry:
  '''Self-defined class for handling crystal structure,
  containing unit-cell-vectors, atoms and kinds of atoms '''

  def __init__(self,lattice_vectors,basis,basis_names_idx,basis_names,
               basis_coordsys="lattice"):

#TODO check data types

    try:
      lattice_vectors.shape=(3,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for lattice_vectors, check configuration.'
           +'\nExiting...')

    self._lattice_vectors = lattice_vectors

    try:
      basis.shape=(basis.size/3,3)
    except ValueError:
      exit('Error:\n'+
           'Wrong number of elements supplied for basis_vectors, check configuration.'
           +'\nExiting...')

    self._basis_names_idx = basis_names_idx
    self._basis_names = basis_names
    self._basis_coordsys = basis_coordsys
    self._basis = self.coord_transform(basis, basis_coordsys)
    self._basis = self.mv_basis_to_prim(self._basis)

  
  @classmethod
  def from_dict(cls,d):
    '''Reads geometry from dict. Returns (lattice, basis, basis_names, basis_ids)
    (3x3-array, ?x3-array, list, list)'''
  
    if "geometry" not in d.keys():
      exit('Error:\n'+
      'geometry not defined, check configuration.'
      +'\nExiting...')
    
    if "lattice_vectors" not in d["geometry"].keys():
      exit('Error:\n'+
           'lattice_vectors not defined, check configuration.'
           +'\nExiting...')
    
    if "basis" not in d["geometry"].keys():
      exit('Error:\n'+
           'basis not defined, check configuration.'
           +'\nExiting...')
  
  
  
    try:
      lattice_vectors = array([float(el) for el in d["geometry"]["lattice_vectors"].split()])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for lattice_vectors not convertable to number, check configuration.'
           +'\nExiting...')
    
  
    basis=d["geometry"]["basis"].split()
  
    if len(basis) % 4 != 0:
      exit('Error:\n'+
           'Wrong number of elements supplied for basis, check configuration.'
           +'\nExiting...')
    
    basis_names=[basis.pop(ind) for ind in range(0,len(basis)*3/4,3)]
    '''#TODO: do not create dublicate entries, related to #TODO in l.88'''
  
    try:
      basis = array([float(el) for el in basis])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for basis not convertable to number, check configuration.'
           +'\nExiting...')

    basis_names_idx=range(basis.size/3) #TODO: generate real idx, related to #TODO in l.71

    basis_coordsys = d["geometry"].get("basis_coordsys","lattice")
    return cls(lattice_vectors,basis,basis_names_idx,basis_names,basis_coordsys)
    
    
  def coord_transform(self, array, array_coordsys):
    if array_coordsys == "lattice":
      return  dot(self._lattice_vectors.T,array.T).T
    elif array_coordsys == "cartesian":
      return array
    else:
      exit('Error:\n'+
           'Supplied string "' + array_coordsys + '" for coordsys not valid, check configuration.'
           +'\nExiting...')
      
  def mv_basis_to_prim(self, basis):
    '''moves basis vectors into primitive cell'''
    basis = dot(asarray(matrix(self._lattice_vectors.T).I),basis.T).T
    basis %= 1
    return self.coord_transform(basis, "lattice")