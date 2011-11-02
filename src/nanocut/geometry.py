# -*- coding: utf-8 -*-

import numpy

class geometry:
  '''Class for handling crystal structure, containing unit-cell-vectors,
      atom coordinates and names of atoms.'''

  def __init__(self, lattice_vectors, basis,basis_names_idx, basis_names,
      basis_coordsys="lattice"):
    
    self._lattice_vectors = numpy.array(lattice_vectors, dtype='float64')
    self._lattice_vectors.shape = (3, 3)
    self._basis_names_idx = basis_names_idx
    self._basis_names = basis_names
    self._basis_coordsys = basis_coordsys
    self._basis = numpy.array(basis, dtype='float64')
    self._basis.shape = (-1, 3)
    self._basis = self.coord_transform(basis, basis_coordsys)
    self._basis = self.mv_basis_to_prim(self._basis)

  
  @classmethod
  def from_dict(cls,d):
    '''Reads geometry from dict and checks data types.'''
  
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
	       
    try:
      lattice_vectors.shape=(3,3)
    except ValueError:
            exit('Error:\n'+
           'Wrong number of elements supplied for lattice_vectors, check configuration.'
           +'\nExiting...')

    basis=d["geometry"]["basis"].split()
  
    if len(basis) % 4 != 0:
      exit('Error:\n'+
           'Wrong number of elements supplied for basis, check configuration.'
           +'\nExiting...')
    
    basis_names=[basis.pop(idx) for idx in range(0,len(basis)*3/4,3)]
    
    try:
      basis = numpy.array([float(el) for el in basis])
    except ValueError:
      exit('Error:\n'+
           'Supplied string for basis not convertible to number, check configuration.'
           +'\nExiting...')
           
    basis.shape=(-1,3)
    basis_names_idx=range(basis.size/3)

    basis_coordsys = d["geometry"].get("basis_coordsys","lattice")
    
    if basis_coordsys not in ["lattice","cartesian"]:
      exit('Error:\n'+
           'Supplied string "' + array_coordsys + '" for coordsys not valid, check configuration.'
           +'\nExiting...')

    if numpy.linalg.det(lattice_vectors)==0:
      exit('Error:\n'+
      'Value of lattice_vectors is invalid.'
      +'\nExiting...\n')





    return cls(lattice_vectors,basis,basis_names_idx,basis_names,basis_coordsys)
    
    
  def coord_transform(self, array, array_coordsys):
    '''Transforms given vector into lattice or cartesian coordinate system'''
    if array_coordsys == "lattice":
      return numpy.dot(self._lattice_vectors.T,array.T).T
    elif array_coordsys == "cartesian":
      return array
    else:
      raise ValueError
      
  def mv_basis_to_prim(self, basis):
    '''Moves basis vectors into primitive cell'''
    basis = numpy.dot(numpy.asarray(numpy.matrix(self._lattice_vectors.T).I),basis.T).T
    basis %= 1
    return self.coord_transform(basis, "lattice")

    
  def gen_cuboid(self, cuboid, periodicity=None):
    '''Generates grid of lattice points containing at least every lattice point
        corresponding to atoms inside the given cuboid boundaries. Eliminates
        equivalent lattice points in case periodicities are present.'''

    #Calculate center of cuboid
    abc_center = 0.5*numpy.array([cuboid[0]+cuboid[1]])

    #Calculate boundaries for a,b,c. Equation for cuboid is:
    #x=(a,b,c).T+center using cartesian coordinates.
    #Boundaries are: -a_min=a_max -b_min=b_max -c_min=c_max .'''
    abc_boundaries=abs(0.5*numpy.array([cuboid[0]-cuboid[1]])).T

    #Add buffer to abc_boudaries
    abc_boundaries+=abs(self._lattice_vectors).max(axis=0).reshape((3,1))

    #Calculate inverse of lattice_vectors matrix.
    #Result transforms any vector (d,e,f) to lattice coordinates.
    trafo=numpy.array(numpy.matrix(self._lattice_vectors).I)
    trafo_back=self._lattice_vectors

    #Calculate "worst case"-boundaries for n, m, o. Equation for cuboid is:
    #x=dot((a,b,c).T,trafo)+center=(n,m,o).T+center using lattice coordinates.
    coeff=numpy.array([[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1]])
    coeff_abc_boundaries = (coeff.T*abc_boundaries).T
    nmo_boundaries=abs(numpy.dot(trafo.T,coeff_abc_boundaries.T))
    nmo_boundaries=nmo_boundaries.max(axis=1)
    
    #Calculate n,m,o of center
    nmo_center=numpy.dot(trafo.T,abc_center.T)

    #Generate list of n,m,o corresponding to all points inside the
    #cuboid (or parallelepiped)'''
    nmo = numpy.array([[n,m,o]
        for n in range(int(-nmo_boundaries[0]+nmo_center[0]),
	                int(nmo_boundaries[0]+nmo_center[0])+1)
	for m in range(int(-nmo_boundaries[1]+nmo_center[1]),
	                int(nmo_boundaries[1]+nmo_center[1])+1)
	for o in range(int(-nmo_boundaries[2]+nmo_center[2]),
	                int(nmo_boundaries[2]+nmo_center[2])+1)
              #TODO: exclude atoms inside parallelepiped but outside cuboid
	if ((abc_center-abc_boundaries.T<=numpy.dot(trafo_back.T,[n,m,o])) *
	    (numpy.dot(trafo_back.T,[n,m,o])<=abc_center+abc_boundaries.T))
	    .all()])

    #Test for equivalent points in case periodicities are present
    if periodicity==None or periodicity.period_type_is("0D"):
      return numpy.dot(nmo,self._lattice_vectors)

    else:
      axis = periodicity.get_axis("lattice")
      is_unique=numpy.ones(len(nmo),bool)

      if periodicity.period_type_is("1D"):

        #Identify of biggest entry of axis to prevent division with 0 later (*)
        axis_max_idx=numpy.abs(axis[0]).argmax()
        axis_max=axis[0,axis_max_idx]

        #Test if point at idx1 is dublicate of point at idx2 for every
        #possible combination
        progress=0
        for idx_1 in range(len(nmo)):
	  print progress,"/",len(nmo)
          if is_unique[idx_1]:
	    progress+=1
            for idx_2 in range(idx_1+1,len(nmo)):
	      if is_unique[idx_2]:
		#Calculate difference between points at idx1 and idx2
		difference=(nmo[idx_1]-nmo[idx_2])
		#Calculate if difference vector is integer multiple of axis (*)
		#factor=difference[axis_max_idx]/axis[0,axis_max_idx]
		factor=difference[axis_max_idx]/axis_max
		#Mark dublicate points
		if (axis[0]*factor==difference).all():
                  is_unique[idx_2]=False
                  progress+=1
        return numpy.dot(nmo[is_unique],self._lattice_vectors)
        
      elif periodicity.period_type_is("2D"):

	axis_basis_3D=numpy.vstack((axis,numpy.cross(axis[0],axis[1])))
        for idx_1 in range(len(nmo)):
	  if is_unique[idx_1]:
            for idx_2 in range(idx_1+1,len(nmo)):
	      if is_unique[idx_2]:
		#Calculate difference between points at idx1 and idx2
		difference=numpy.array((nmo[idx_1]-nmo[idx_2]))
		#Calculate if difference vector is sum of integer multiples
		#of axes (*)
                factor = numpy.linalg.solve(axis_basis_3D.T,difference.T)
                factor = factor.round().astype('int')
                if (axis[0]*factor[0]+axis[1]*factor[1]==difference).all():
		  #Mark dublicate points
                  is_unique[idx_2]=False

        return numpy.dot(nmo[is_unique],self._lattice_vectors)

      

  def get_name_of_atom(self, index):
    '''Returns name corresponding to given index.'''
    return self._basis_names[self._basis_names_idx[index]]
  
  def gen_atoms(self, lattice_points):
    '''Returns the coordinates and index of each atom inside the cells
    corresponding to given lattice points'''
    
    #coordinates
    atoms_coords = numpy.array([(point+self._basis[atom_idx])
    for point in lattice_points for atom_idx in range(len(self._basis))])

    #indexes
    atoms_idx = numpy.array([ atom_idx
    for point in lattice_points for atom_idx in range(len(self._basis))])
    
    return atoms_coords, atoms_idx
