# -*- coding: utf-8 -*-
from numpy import array, dot, matrix, asarray
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
  
  def gen_cuboid_from_body(self, body):
    return self.gen_cuboid0(body.containing_cuboid())
    
  def gen_cuboid0(self, cuboid):
    print "cuboid:"
    print cuboid
    '''Calculate center of cuboid'''
    print "center:"
    center = 0.5*numpy.array([cuboid[0]+cuboid[1]])
    print center
    '''Calculate boundaries for a,b,c. Equation for cuboid is: x=(a,b,c).T+center using
    cartesian coordinates. Bounderies are: -a_min=a_max -b_min=b_max -c_min=c_max .'''
    abc_boundaries=abs(0.5*numpy.array([cuboid[0]-cuboid[1]])).T
    print "abc_boundaries:\n", abc_boundaries
    '''Calculate inverse of lattice_vectors matrix. Result transforms any vector (d,e,f)
    to lattice coordinates: dot((d,e,f).T , trafo)'''
    trafo=numpy.asarray(numpy.matrix(self._lattice_vectors).I)
    #print "trafo:\n", trafo
    '''Calculate "worst case"-boundaries for n, m, o. Equation for cuboid is:
    x=dot((a,b,c).T,trafo)+center = (n,m,o).T+center using lattice coordinates.'''
    coeff=array([[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1]])
    #print "abc_boundaries:\n", abc_boundaries
    coeff_abc_boundaries = (coeff.T*abc_boundaries).T
    nmo_boundaries=abs(numpy.dot(trafo.T,coeff_abc_boundaries.T))
    nmo_boundaries=nmo_boundaries.max(axis=1)
    print "nmo_boundaries:\n",nmo_boundaries
    
    for n in range(int(-nmo_boundaries[0]),int(nmo_boundaries[0])+1):
      for m in range(int(-nmo_boundaries[1]),int(nmo_boundaries[1])+1):
	for o in range(int(-nmo_boundaries[1]),int(nmo_boundaries[1])+1):
	  print (n,m,o)
	  
    
    
    
    




  def gen_cuboid1(self, cuboid):
    m = 0.5*array([cuboid[0]+cuboid[1]])
    n = numpy.linalg.solve(self._lattice_vectors.T,m.T)
    coords = numpy.array([[0,0,0]])
    
    temporary_list=[]
    
    
    n_intsec = (cuboid - dot(self._lattice_vectors[1:3,:].T,n[1:3]).T)\
     / self._lattice_vectors[0]
     
     
    n_min_idx = abs(n_intsec[0]-n[0]).argmin()
    n_max_idx = abs(n_intsec[1]-n[0]).argmin()
    
    if int(n_intsec[0,n_min_idx]) > int(n_intsec[1,n_max_idx]):
      n_min_idx,n_max_idx=n_max_idx,n_min_idx
      a,b=1,0
    else:
      a,b=0,1
    n_range=range(int(n_intsec[a,n_min_idx]),int(n_intsec[b,n_max_idx])+1)
    
    for n0 in n_range:
      n_intsec = (cuboid - dot(self._lattice_vectors[0:3:2,:].T,n[0:3:2]).T)\
      / self._lattice_vectors[1]
      
      n_min_idx = abs(n_intsec[0]-n0).argmin()
      n_max_idx = abs(n_intsec[1]-n0).argmin()
    
      if int(n_intsec[0,n_min_idx]) > int(n_intsec[1,n_max_idx]):
        n_min_idx,n_max_idx=n_max_idx,n_min_idx
        a,b=1,0
      else:
        a,b=0,1
      n_range=range(int(n_intsec[a,n_min_idx]),int(n_intsec[b,n_max_idx])+1)
      
      for n1 in n_range:
        n_intsec = (cuboid - dot(self._lattice_vectors[0:2,:].T,n[0:2]).T)\
        / self._lattice_vectors[2]
        n_min_idx = abs(n_intsec[0]-n1).argmin()
        n_max_idx = abs(n_intsec[1]-n1).argmin()
    
        if int(n_intsec[0,n_min_idx]) > int(n_intsec[1,n_max_idx]):
          n_min_idx,n_max_idx=n_max_idx,n_min_idx
          a,b=1,0
        else:
          a,b=0,1
        n_range=range(int(n_intsec[a,n_min_idx]),int(n_intsec[b,n_max_idx])+1)
        
        for n2 in n_range:
          coords = numpy.vstack((coords, n0*self._lattice_vectors[0]+n1*\
                                         self._lattice_vectors[1]+n2*self._lattice_vectors[2]))
          temporary_list.append(n0*self._lattice_vectors[0]+n1*self._lattice_vectors[1]+n2*self._lattice_vectors[2])
    return temporary_list