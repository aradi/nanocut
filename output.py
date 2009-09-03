# -*- coding: utf-8 -*-
'''
Created on Sep 2, 2009

@author: sebastian
'''
import numpy

def write_structure_to_file(geometry, atoms, atoms_inside_bodies, file):
  fi = open(file, 'w')

  fi.write(repr(sum(atoms_inside_bodies)) + '\n\n')
  
  '''print atoms to file'''
  [fi.write(\
    geometry._basis_names[geometry._basis_names_idx[int(atom[3])]]+' '\
    +repr(atom[0])+' '+ repr(atom[1])+' '+ repr(atom[2])+'\n')\
  for atom in atoms[atoms_inside_bodies]]

  fi.close()