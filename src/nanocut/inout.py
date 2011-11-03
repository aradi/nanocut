# -*- coding: utf-8 -*-

#import modules
import ConfigParser
import numpy
import getopt
import sys

def print_usage(shouldexit=True):
  '''Short Instructions'''
  print 'Usage: nanocut [OPTIONS] INFILE [OPTIONS]\n\
         \n\
         Option    Meaning\n\
         -a FILE   appends created structure to FILE\n\
         -h        prints help\n\
         --help    prints help\n\
         -w FILE   creates or overwrites FILE'
  if shouldexit:
    exit()

def print_help(shouldexit=True):
  '''Help message'''
  print 'helptext:\n\n'
  print_usage(shouldexit)
  
def parse_args(argv):
  '''Handles user command. Raises error if bad input'''

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

  write = [a for o,a in opts if o == '-w']
  append = [a for o,a in opts if o == '-a']

  return (input[1], write, append)


def read_ini(filename):
  '''Reads ini-file. Returns content as ConfigParser-object'''
  ini = ConfigParser.ConfigParser()
  
  try:
    configfile = open(filename, 'r')
  except IOError:
    exit('Error:\n'+
    "Can't open " + filename + '.'
    +'\nExiting...')
  
  try:
    ini.readfp(configfile)
  except ConfigParser.MissingSectionHeaderError, exc:
    exit('Error:\n' +
    'Malformed ini-file, ' + configfile.name + '. Section Header missing.'
    + '\nExiting...')
  except ConfigParser.ParsingError, exc:
    exit('Error:\n' +
    'Malformed ini-file, ' + configfile.name + '. Parsing error at:\n' +
    repr(exc.append).split("\n")[1][:-1] +
    '\nExiting...')
    
  configfile.close()
  return ini



def ini2dict(ini):
  '''Converts ConfigParser-object (generated from ini) to 2D dict
      (d[section][item]->value).'''
      
  return dict([ (section, dict(ini.items(section)) )
      for section in ini.sections() ])

def write_crystal(geometry, atoms_coords, atoms_idx, axis_string,
    writefilenames, appendfilenames):

  number_atoms = atoms_idx.shape[0]
  write_to_stdout = (len(writefilenames) == 0 and len(appendfilenames) == 0) 

  files = []
  for filename in appendfilenames:
    try:
      file = open(filename, 'r')
    except IOError:
      exit("Error:\n'Can't open " + filename + ".\nExiting...")    
    try:
      old_file_number_atoms = int( file.readline() )
    except ValueError:
      exit('Error:\n' + file.name + ' not in xyz-format.\nExiting...')
    old_file = ([ "%d\n" % (old_file_number_atoms + number_atoms) ]
                + file.readlines()[:old_file_number_atoms + 1])
    file.close()
    file = open(filename, "w")
    file.writelines(old_file)
    files.append(file)
    
  for filename in writefilenames:
    try:
      file = open(filename, 'w')
    except IOError:
      exit("Error:\n Can't open " + filename + ".\nExiting...")
    file.write("%d\n%s\n" % (number_atoms, axis_string))  
    files.append(file)
    
  fcontent = [ " %-3s %18.10E %18.10E %18.10E\n" 
               % (geometry.get_name_of_atom(atoms_idx[it]), atoms_coords[it,0],
                  atoms_coords[it,1], atoms_coords[it,2]) 
               for it in range(len(atoms_coords)) ]
  for file in files:
    file.writelines(fcontent)
  if write_to_stdout:
      sys.stdout.writelines(fcontent)      
  for file in files:
    file.close()
