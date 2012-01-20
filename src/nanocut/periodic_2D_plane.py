# -*- coding: utf-8 -*-
'''
Created on Aug 31, 2009

@author: sebastian
'''
import numpy
import nanocut.body as body

class periodic_2D_plane(body.body):
    '''Class for plane elements with 2D periodicity'''
    #arguments of class defined in the following format:
    #[default, type, shape, is_coord_sys_definable]
    _arguments={
        "thickness":[None, "float", None, False],
        "shift_vector":["0 0 0", "array", (1,3), True],
        "order":[1,"integer", None, False]
    }

    def __init__(self, geometry, periodicity, thickness, shift_vector=
        numpy.array([0,0,0]), order=1, shift_vector_coordsys="lattice"):
        body.body.__init__(self, geometry, shift_vector, order,
            shift_vector_coordsys)
        self._thickness = float(thickness)
    @classmethod
    def _from_dict_helper(cls, geometry, args, periodicity):
        return cls(geometry, periodicity, args["thickness"], args["shift_vector"],
            args["order"], args["shift_vector_coordsys"])

    def containing_cuboid(self,periodicity):
        '''Calculates the boundaries of the cuboid containing a plane element'''
        #Retrieve periodic axis from periodicity
        axis = periodicity.get_axis("cartesian")
        bounds = numpy.vstack((
            self._shift_vector + self._thickness,
            self._shift_vector - self._thickness,
            axis[0] + self._shift_vector + self._thickness,
            axis[0] + self._shift_vector - self._thickness,
            axis[1] + self._shift_vector + self._thickness,
            axis[1] + self._shift_vector - self._thickness,
            ))
        return numpy.vstack((bounds.min(axis=0), bounds.max(axis=0)))

    def atoms_inside(self,atoms,periodicity):
        '''Assigns True and False values towards points in and out of a single
        plane element's boundaries respectively'''
        atoms_inside_body = numpy.zeros(atoms.shape[0], bool)
        #Retrieve periodic axis from periodicity
        axis = periodicity.get_axis("cartesian")
        non_periodic_dir = numpy.cross(axis[0], axis[1]).astype('float64')
        non_periodic_dir = non_periodic_dir/numpy.linalg.norm(non_periodic_dir)
        for idx in range(atoms.shape[0]):
           dist = abs(numpy.dot( (atoms[idx]-self._shift_vector), non_periodic_dir))
           atoms_inside_body[idx] = self._thickness/2 >= dist
        return atoms_inside_body
