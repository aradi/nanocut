# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2009

@author: sebastian
'''

import numpy

class body:
    '''Metaclass; all body-classes regardless of shape should be derived from this one'''
    def __init__(self, geometry, shift_vector, order, shift_vector_coordsys):
        shift_vector = numpy.array(shift_vector, dtype='float64')
        shift_vector.shape = (1, 3)
        order = int(order)
        self._order = order
        self._shift_vector = geometry.coord_transform(shift_vector,
            shift_vector_coordsys)

    def get_order(self):
        return self._order
  
    def order_is(self,test_order):
        return self._order == test_order

    def is_additive(self):
        return self._order > 0 and self._order%2 == 1
    
    def is_substractive(self):
        return self._order > 0 and self._order%2 == 0
    
    def is_ignored(self):
        return self._order <= 0
    @classmethod  
    def from_dict(cls, geometry, configdict, periodicity=None):
        '''Reads body properties from doctionary and assigns them to relevant attributes'''
        init_args = {}
        for arg, spec in cls._arguments.items():
            init_args[arg] = configdict.get(arg, spec[0])
            if init_args[arg] == None:
                exit('Error:\n' + arg + ' not specified, but needed.\n Exiting...\n')
            if spec[1] == 'array':
                try:
                    init_args[arg] = numpy.array([ float(el)
                        for el in init_args[arg].split()])
                except ValueError:
                    exit('Error:\n Supplied string for ' + arg + 
                        ' not convertible to float-array.\n Exiting...\n')
                try:
                    init_args[arg].shape = spec[2]
                except ValueError:
                    exit('Error:\n Wrong number of elements supplied for ' + arg +
                        '.\n Exiting...\n')
            elif spec[1] == 'intarray':
                try:
                    init_args[arg] = numpy.array([ int(el)
                        for el in init_args[arg].split()])
                except ValueError:
                    exit('Error:\n Supplied string for ' + arg + 
                        ' not convertible to integer-array.\n Exiting...\n')
                try:
                    init_args[arg].shape = spec[2]
                except ValueError:
                    exit('Error:\n Wrong number of elements supplied for ' + arg +
                        '.\n Exiting...\n')
            elif spec[1] == 'integer':
                try:
                    init_args[arg]=int(init_args[arg])
                except ValueError:
                    exit('Error:\n Supplied string for ' + arg +
                        ' not convertible to integer.\n Exiting...\n')
            elif spec[1] == 'float':
                try:
                    init_args[arg] = float(init_args[arg])
                except ValueError:
                    exit('Error:\n Supplied string for ' + arg +
                        ' not convertible to float.\n Exiting...\n')
            else:
                #TODO: Raise Exeption
                exit('InternalError:\n There is no valid argument type ' + spec[1] + 
                    ' can\'t use from_dict() with this class.\n Exiting...\n')
            if spec[3] == True:
                init_args[arg + '_coordsys'] = configdict.get(arg + '_coordsys','lattice')
                if init_args[arg + '_coordsys'] not in ['lattice', 'cartesian']:
                    exit('Error:\n Supplied string "' + init_args[arg + '_coordsys'] + 
                        '"for ' + arg + '_coordsys is invalid.\n Exiting...\n')

        return cls._from_dict_helper(geometry, init_args, periodicity)
