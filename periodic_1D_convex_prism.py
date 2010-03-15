# -*- coding: utf-8 -*-
'''
Created on Sep 2, 2009

@author: sebastian
'''
import numpy
import body

class periodic_1D_convex_prism(body.body):
  '''Class for periodic bodies determined by a group of planes describing it's
      boundaries'''

  #arguments of class defined in the following format:
  #[default, type, shape, is_coord_sys_definable]
  _arguments={
     "planes_normal":["0 0 0 0", "array", (-1,4), True],
     "planes_miller":["0 0 0 0", "array", (-1,4), False],
     "point_inside_body":[None, "array", (1,3), True],
     "shift_vector":["0 0 0", "array", (1,3), True],
     "order":[1,"integer", None, False]
    }

  def __init__(self,geometry,periodicity,planes_normal,planes_miller,
               shift_vector, point_inside_body,order=1,shift_vector_coordsys=
               "lattice", planes_normal_coordsys="lattice",
               point_inside_body_coordsys="lattice"):
    #Initiating body using the lattice determined by geometry-object, planes
    #given by miller indices or normal shape, a point inside the polyhedron and
    #a possible shift_vector to determine it's distance from [0,0,0], as well
    #as each attribute's coordinate system
    
    #Type checking/conversion and initialisation of parent class
    body.body.__init__(self, geometry, shift_vector, order, 
        shift_vector_coordsys)

    
    point_inside_body = numpy.array(point_inside_body, dtype='float64')
    point_inside_body.shape = (1,3)
    
    
    planes_normal = numpy.array(planes_normal, dtype='float64')
    planes_normal.shape = (-1,4)
    planes_normal[:,:3] = geometry.coord_transform(planes_normal[:,:3],
        planes_normal_coordsys)

    planes_miller = numpy.array(planes_miller, dtype='float64')
    planes_miller.shape = (-1,4)

    #Transforms planes determined by miller indices into normal shape
    self._planes_miller = numpy.array([ numpy.hstack(( self.miller_to_normal(
	geometry,plane[:3]), plane[3] )) for plane in planes_miller ])

    #Appends planes calculated from miller indices to planes in normal form
    self._planes_normal = numpy.vstack(( planes_normal, self._planes_miller ))

    #Retrieve periodic axis from module periodicity
    axis = periodicity.get_axis("cartesian")
    
    #Check for 
    for plane in self._planes_normal:
      if (plane[:3]!=0).any():
        if ( numpy.cross( plane[:3], axis ) == 0 ).all():
            raise ValueError, "Plane orthogonal to axis.\n\
            Projection impossible."
    
    #Check if planes create closed space and warn if necessary
    for plane_idx1 in range( 0,len( self._planes_normal )):
      for plane_idx2 in range( plane_idx1+1,len( self._planes_normal )):
        for plane_idx3 in range( plane_idx2+1,len( self._planes_normal )):
          try:
            corner = numpy.linalg.solve(
                numpy.vstack((
                    self._planes_normal[plane_idx1,:3],
                    self._planes_normal[plane_idx2,:3],
                    self._planes_normal[plane_idx3,:3]
                    )),
                numpy.vstack((
                    self._planes_normal[plane_idx1,3],
                    self._planes_normal[plane_idx2,3],
                    self._planes_normal[plane_idx3,3]
                    ))
                ).T
            print 'Warning! Planes might intersect and possibly create closed\
            space.\n Are you sure your input is correct?'
          except:
            pass
    
    NumError = 10**(-10) #TODO Define NumError
    
    #Check if planes are parallel to axis, rotate plane if not so
    for plane in self._planes_normal:
      try:
        if numpy.abs( numpy.dot(plane[:3],axis.T) )-NumError>0: 
            print "Given plane appears not parallel to axis.\n\
            possibly numerical error.\n\
            Plane will be projected to fit axis!"
            plane[:3] = numpy.cross( numpy.cross( plane[:3],axis ),axis )
        else:
          pass
      except ZeroDivisionError:
          pass
    
    #Calculates normal vectors if necessary
    for plane in self._planes_normal:
      try:
         plane[:3] = plane[:3] / numpy.linalg.norm(plane[:3])
      except ZeroDivisionError:
        pass

    
    #Computes intersection lines of planes if possible
    self._lines = numpy.array([0,0,0,0,0,0])
    for plane in self._planes_normal:
      try:
        self._lines = numpy.vstack((
            self._lines, numpy.hstack((
                numpy.cross( plane[:3], axis)[0], (numpy.dot(plane[:3],
                    self._shift_vector.T) + plane[3]) * plane[:3] /
                    numpy.linalg.norm(plane[:3]) - self._shift_vector[0]
                ))
             ))
      except ZeroDivisionError:
        pass 
      
    #Properly shaping and norming self._lines
    self._lines = self._lines[1:]
    
    for line in self._lines:
      try:
        line[:3] = line[:3] / numpy.linalg.norm(line[:3])
      except ZeroDivisionError:
        pass 


    
    #Changes point_inside_body's coordinate system if necessary
    self._point_inside_body = geometry.coord_transform(point_inside_body,
        point_inside_body_coordsys)

    #Distributes True and False values towards point_inside_body's respective
    #position towards each plane
    try:
      self._parameter = numpy.array([ (self._planes_normal[plane_idx,3] -
          sum( self._point_inside_body[0] * self._planes_normal[plane_idx,:3] )
          ) / sum(self._planes_normal[plane_idx,:3]**2) <= 0
          for plane_idx in range( len( self._planes_normal )) ])
    except ZeroDivisionError:
         pass


  @classmethod  
  def _from_dict_helper(cls, geometry, args, periodicity):
    return cls(geometry,periodicity, args["planes_normal"],
      args["planes_miller"], args["shift_vector"],args["point_inside_body"], 
      args["order"], args["shift_vector_coordsys"],args[
      "planes_normal_coordsys"], args["point_inside_body_coordsys"])

  def containing_cuboid(self,periodicity):
    '''Calculates the boundaries of the containing cuboid determined by axis'
    projection on boundary planes'''
    
    axis = periodicity.get_axis("cartesian")

    #Places extreme points in cuboid by projecting axis points on plane
    #intersection lines and returns cuboid
    corners = numpy.array([[0,0,0]])
    
    for line in self._lines:
      corner = numpy.dot( line[3:],  line[:3].T
           ) * line[:3] + line[3:]
      corners = numpy.vstack((corners, corner))
    
    #Removes possible bad values (NaN, Inf) from corners
    corners = corners[1:]
    for index in range( len( corners )):
      if ( numpy.isnan( corners[index] ).any() or numpy.isinf( corners[index]
          ).any() or numpy.isneginf( corners[index] ).any() ):
        corners = numpy.delete(corners, index, 0)
    
    corners = numpy.vstack(( corners + self._shift_vector, corners + axis +
        self._shift_vector ))
    
    
    return numpy.vstack(( corners.min(axis=0), corners.max(axis=0) ))
  
  
  def atoms_inside(self, atoms, periodicity=None):
    '''Creates boolean array assigning True and False values towards points in
        and out of plane boundaries respectively'''
    
    atoms_inside_body = numpy.zeros(atoms.shape[0], bool)
    
    #Retrieves periodic axis from periodicity
    axis = periodicity.get_axis("cartesian")
    
    #Determines for each point given if it shares the same position related to
    #each plane as the point_inside_body and if it's projection is within the
    #axis range
    for idx in range( len( atoms )):
      TF_planes = numpy.array([
          (self._planes_normal[plane_idx,3]
              - sum( ( atoms[idx,:3] - self._shift_vector )[0]
              *  self._planes_normal[plane_idx,:3]) ) /
              sum( self._planes_normal[plane_idx,:3]**2 ) <= 0
              for plane_idx in range( len( self._planes_normal ))
          ])
      atoms_inside_body[idx] = ( TF_planes==self._parameter ).all()
    
    
    return atoms_inside_body
                        
  def miller_to_normal(self, geometry, plane_miller):
    '''Calculates the normal form of a plane defined by Miller indices'''
    
    return ( plane_miller[0] * numpy.cross(geometry._lattice_vectors[1],
        geometry._lattice_vectors[2]) + plane_miller[1] * numpy.cross(
        geometry._lattice_vectors[2], geometry._lattice_vectors[0] ) +
        plane_miller[2] * numpy.cross( geometry._lattice_vectors[0], 
        geometry._lattice_vectors[1] ) )