# -*- coding: utf-8 -*-


import ConfigParser
import numpy
import getopt

def print_usage(shouldexit=True):
  print 'Usage: nanocut [OPTIONS] INFILE [OPTIONS]\n\
         \n\
         Option\t Meaning\n\
         -a OUTFILE\t appends created structure to OUTFILE\n\
         -h \t prints help\n\
         --help\t print help\n\
         -w OUTFILE\t creates or overwrites OUTFILE'
  if shouldexit:
    exit()

def print_help(shouldexit=True):
  print 'helptext:\n\n'
  print_usage(shouldexit)
  
def parse_args(argv):

  try:
    opts, input = getopt.gnu_getopt(argv, 'a:hw:', ['help'])
  except getopt.GetoptError, exc:
    print 'Error:\n\
           Invalid argument. ',exc.opt,'\n\n'
    print_usage()
  if len(input) != 2:
    print 'Error:\n\
           No or multiple INFILEs specified.\n\n'
    print_usage()
  
  if '-h' in opts or '--help' in opts:
    print_help()

  write = [a for o,a in opts if o== '-w']
  append = [a for o,a in opts if o== '-a']

  return (input[1], write, append)


def read_ini(filename):
  '''Reads ini-file. Returns content as ConfigParser-object'''
  ini=ConfigParser.ConfigParser()
  
  try:
    configfile = open(filename, 'r')
  except IOError:
    exit('Error:\n'+
    "Can't open "+filename+'.'
    +'\nExiting...')
  
  try:
    ini.readfp(configfile)
  except ConfigParser.MissingSectionHeaderError, exc:
    exit('Error:\n'+
    'Malformed ini-file, '+configfile.name+'. Section Header missing.'
    +'\nExiting...')
  except ConfigParser.ParsingError, exc:
    exit('Error:\n'+
    'Malformed ini-file, '+configfile.name+'. Parsing error at:\n'+
    repr(exc.append).split("\n")[1][:-1]+
    '\nExiting...')
  configfile.close()
  return ini



def ini2dict(ini):
  '''Converts ConfigParser-object (generated from ini) to 2D dict\
   (d[section][item]->value).'''
  return dict([(section,dict(ini.items(section))) for section in ini.sections()])

def write_crystal(geometry,atoms_cuboid, atoms_inside_bodies, writefilenames, appendfilenames):

  number_atoms = sum(atoms_inside_bodies)
  if len(writefilenames)==0 and len(appendfilenames)==0:
    write_to_stdout=True
  else:
    write_to_stdout=False
  
  files = []
  for filename in appendfilenames:
    try:
      file = open(filename, 'r+')
    except IOError:
      exit('Error:\n'+
           "Can't open "+filename+'.'
           +'\nExiting...')
      
    try:
      old_file_number_atoms = int(file.readline())
    except ValueError:
      exit('Error:\n'+
           +file.name+' not in xyz-format.'
           +'\nExiting...')

    old_file = [repr(old_file_number_atoms + number_atoms)+'\n']\
                    + file.readlines()[:old_file_number_atoms+1]
    file.seek(0)
    file.writelines(old_file)
    files.append(file)
    
  for filename in writefilenames:
    try:
      file = open(filename, 'w')
    except IOError:
      exit('Error:\n'+
           "Can't open "+filename+'.'
           +'\nExiting...')
    file.write(repr(number_atoms)+'\n\n')
    files.append(file)
    
  for atom in atoms_cuboid[atoms_inside_bodies]:
    atomsstring = geometry._basis_names[geometry._basis_names_idx[int(atom[3])]]+' '\
            +repr(atom[0])+' '+ repr(atom[1])+' '+ repr(atom[2])+'\n'
    [file.write(atomsstring) for file in files]
    if write_to_stdout:
      print atomsstring
    
  [file.close() for file in files]
