# -*- coding: utf-8 -*-


import ConfigParser
import numpy

def read_ini(configfile):
  '''Reads ini-file. Returns content as ConfigParser-object'''
  ini=ConfigParser.ConfigParser()
  try:
    ini.read(configfile)
  except ConfigParser.MissingSectionHeaderError, exc:
    exit('Error:\n'+
    'Malformed ini-file, '+configfile+'. Section Header missing.'
    +'\nExiting...')
  except ConfigParser.ParsingError, exc:
    exit('Error:\n'+
    'Malformed ini-file, '+configfile+'. Parsing error at:\n'+
    repr(exc.append).split("\n")[1][:-1]+
    '\nExiting...')
  return ini



def ini2dict(ini):
  '''Converts ConfigParser-object (generated from ini) to 2D dict (d[section][item]->value).'''
  return dict([(section,dict(ini.items(section))) for section in ini.sections()])



def geometry_from_dict(d):
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
    'Supplied string for lattice_vectors not convertible to number, check configuration.'
    +'\nExiting...')
    
  if lattice_vectors.size != 9:
    exit('Error:\n'+
    'Wrong number of elements supplied for lattice_vectors, check configuration.'
    +'\nExiting...')
    
  lattice_vectors.shape=(3,3)
  
  
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
  
  basis.shape=(basis.size/3,3)
  
  basis_name_idx=range(basis.size/3) #TODO: generate real idx, related to #TODO in l.71
  
  return (lattice_vectors, basis, basis_names, basis_name_idx)

def write_structure_to_file(geometry, atoms, atoms_inside_bodies, file):
  fi = open(file, 'w')

  fi.write(repr(sum(atoms_inside_bodies)) + '\n\n')
  
  '''print atoms to file'''
  [fi.write(\
    geometry._basis_names[geometry._basis_names_idx[int(atom[3])]]+' '\
    +repr(atom[0])+' '+ repr(atom[1])+' '+ repr(atom[2])+'\n')\
  for atom in atoms[atoms_inside_bodies]]

  fi.close()