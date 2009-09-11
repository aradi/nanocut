# -*- coding: utf-8 -*-

import numpy

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
      lattice_vectors = numpy.array([float(el) for el in d["geometry"]["lattice_vectors"].split()])
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
    '''#TODO: do not create double entries, related to #TODO in l.88'''
  
    try:
      basis = numpy.array([float(el) for el in basis])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for basis not convertible to number, check configuration.'
           +'\nExiting...')

    basis_names_idx=range(basis.size/3) #TODO: generate real idx, related to #TODO in l.71

    basis_coordsys = d["geometry"].get("basis_coordsys","lattice")
    return cls(lattice_vectors,basis,basis_names_idx,basis_names,basis_coordsys)
    
    
  def coord_transform(self, array, array_coordsys):
    if array_coordsys == "lattice":
      return  numpy.dot(self._lattice_vectors.T,array.T).T
    elif array_coordsys == "cartesian":
      return array
    else:
      exit('Error:\n'+
           'Supplied string "' + array_coordsys + '" for coordsys not valid, check configuration.'
           +'\nExiting...')
      
  def mv_basis_to_prim(self, basis):
    '''moves basis vectors into primitive cell'''
    basis = numpy.dot(numpy.asarray(numpy.matrix(self._lattice_vectors.T).I),basis.T).T
    basis %= 1
    return self.coord_transform(basis, "lattice")
  

    return self.gen_cuboid0(body.containing_cuboid())
    
  def gen_cuboid(self, cuboid, axis=None):
    
    '''Calculate center of cuboid'''
    
    abc_center = 0.5*numpy.array([cuboid[0]+cuboid[1]])

    '''Calculate boundaries for a,b,c. Equation for cuboid is: x=(a,b,c).T+center using
    cartesian coordinates. Bounderies are: -a_min=a_max -b_min=b_max -c_min=c_max .'''
    abc_boundaries=abs(0.5*numpy.array([cuboid[0]-cuboid[1]])).T

    '''Add buffer to abc_boudaries'''
    abc_boundaries+=abs(self._lattice_vectors).max(axis=0).reshape((3,1))
    
    '''Calculate inverse of lattice_vectors matrix. Result transforms any vector (d,e,f)
    to lattice coordinates: dot((d,e,f).T , trafo)'''
    trafo=numpy.asarray(numpy.matrix(self._lattice_vectors).I)
    
    
    '''Calculate "worst case"-boundaries for n, m, o. Equation for cuboid is:
    x=dot((a,b,c).T,trafo)+center = (n,m,o).T+center using lattice coordinates.'''
    coeff=numpy.array([[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1]])
    
    
    coeff_abc_boundaries = (coeff.T*abc_boundaries).T
    nmo_boundaries=abs(numpy.dot(trafo.T,coeff_abc_boundaries.T))
    
    nmo_boundaries=nmo_boundaries.max(axis=1)
    

    
    '''Calculate n,m,o of center'''
    nmo_center=numpy.dot(trafo.T,abc_center.T)

    
    
    '''Generating list of n,m,o which are dedicated to the points inside the cuboid
    (or parallelepiped)'''

    nmo = numpy.array([[n,m,o]\
	      for n in range(int(-nmo_boundaries[0]+nmo_center[0]),
	                      int(nmo_boundaries[0]+nmo_center[0])+1)\
	      for m in range(int(-nmo_boundaries[1]+nmo_center[1]),
	                      int(nmo_boundaries[1]+nmo_center[1])+1)\
	      for o in range(int(-nmo_boundaries[2]+nmo_center[2]),
	                      int(nmo_boundaries[2]+nmo_center[2])+1)\
	      if 1==1])

    def is_int_multiple():
      diff=numpy.array((nmo[idx_1]-nmo[idx_2]))
      factor=diff[axis_max_idx]/axis[axis_max_idx]
      if (axis*factor==diff).all():
        is_dub[idx_2]=True

    if axis!=None:
      axis_max_idx=axis.argmax()
      is_dub=numpy.zeros(len(nmo),bool)
      [is_int_multiple()\
           for idx_1 in range(len(nmo)) if is_dub[idx_1]==False\
           for idx_2 in range(idx_1+1,len(nmo)) if is_dub[idx_2]==False\
      ]
      return numpy.dot(nmo[numpy.invert(is_dub)],self._lattice_vectors)
    return numpy.dot(nmo,self._lattice_vectors)
      
  
  def gen_atoms(self, lattice_points):
    '''Returns the atoms distributed to a given lattice point as array([x-coord, y-coord, z-coord, ID])'''
    atoms = numpy.array([numpy.hstack((point+self._basis[atom_idx], atom_idx)) for point in lattice_points for atom_idx in range(len(self._basis))])
    return atoms
