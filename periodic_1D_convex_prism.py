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
     "shift_vector":["0 0 0", "array", (1,3), True],
     "order":[1,"integer", None, False]
    }

  def __init__(self,geometry,periodicity, planes_normal,planes_miller,
               shift_vector, order=1, shift_vector_coordsys="lattice",
               planes_normal_coordsys="lattice"):
    #Initiating body using the lattice determined by geometry-object, planes
    #given by miller indices or normal shape and a possible shift_vector to 
    #determine it's distance from [0,0,0], as well
    #as each attribute's coordinate system
    
    #Type checking/conversion and initialisation of parent class
    body.body.__init__(self, geometry, shift_vector, order, 
        shift_vector_coordsys)
    
    if (planes_normal==0).all():
      pass
    else:
      planes_normal = numpy.array(planes_normal, dtype='float64')
      planes_normal.shape = (-1,4)
      planes_normal[:,:3] = geometry.coord_transform(planes_normal[:,:3],
          planes_normal_coordsys)
      for plane in planes_normal:
        if (plane[:3]==0).all():
          print 'Empty normal vector found. Are you sure input is correct?'
    
    if (planes_miller==0).all():
      pass
    else:
      planes_miller = numpy.array(planes_miller, dtype='float64')
      planes_miller.shape = (-1,4)
      for plane in planes_miller:
        if (plane[:3]==0).all():
          print 'Empty miller plane found. Are you sure input is correct?'

      #Transforms planes determined by miller indices into normal shape
      planes_miller = numpy.array([ numpy.hstack(( self.miller_to_normal(
          geometry,plane[:3]), plane[3] )) for plane in planes_miller ])

    #Appends planes calculated from miller indices to planes in normal form
    self._planes_normal = numpy.vstack(( planes_normal, planes_miller ))
    
    if (self._planes_normal[:,:3]==0).all():
      exit('Error:\n' +
          'No proper planes specified.'
          + '\nExiting...\n')
    
    idx = 0
    while idx < self._planes_normal.shape[0]:
      if (self._planes_normal[idx,:3]==0).all():
        self._planes_normal = numpy.delete(self._planes_normal, idx, 0)
      else:
        idx += 1
      
    #Retrieve periodic axis from module periodicity
    axis = periodicity.get_axis("cartesian")
    
    #Check for 
    for plane in self._planes_normal:
      if ( numpy.cross( plane[:3], axis ) == 0 ).all():
          raise ValueError, "Plane orthogonal to axis.\nProjection impossible."
    
    
    NumError = 10**(-10) #TODO Define NumError
    
    #Check if planes are parallel to axis, rotate plane if not so
    for plane in self._planes_normal:
      if numpy.abs( numpy.dot(plane[:3],axis.T) )- NumError > 0: 
          print "Given plane appears not parallel to axis.\n\
          Possibly numerical error.\n\
          Plane will be projected to fit axis!"
          plane[:3] = numpy.cross( numpy.cross( plane[:3],axis ),axis )
    
    #Normalizes planes
    for plane in self._planes_normal:
      plane[:3] = plane[:3] / numpy.linalg.norm(plane[:3])

    #Removes identical planes
    idx1 = 0
    idx2 = 1
    while idx1 < (self._planes_normal.shape[0]-1):
      while idx2 < self._planes_normal.shape[0]:
        if (self._planes_normal[idx1,3]==self._planes_normal[idx2,3] and
            (numpy.cross( self._planes_normal[idx1,:3],
            self._planes_normal[idx2,:3]) == 0).all() ):
            self._planes_normal = numpy.delete(self._planes_normal, idx2, 0)
            print 'Identical planes found. Double plane will be removed...'
        else:
          idx2 += 1
      idx1+=1
      idx2 = idx1 + 1
    
    #Computes intersection lines of planes if possible
    self._lines = numpy.array([0,0,0,0,0,0])
    for plane in self._planes_normal:
      self._lines = numpy.vstack((
          self._lines, numpy.hstack((
          numpy.cross( plane[:3], axis)[0], (numpy.dot(plane[:3],
          self._shift_vector.T) + plane[3]) * plane[:3] - self._shift_vector[0]
          ))
        ))
      
    #Properly shaping and norming self._lines
    self._lines = self._lines[1:] 
    
    idx = 0
    while idx < self._lines.shape[0]:
      if (self._lines[idx]==0).all():
        self._lines = numpy.delete(self._lines, idx, 0)
      else:
        self._lines[idx,:3] = self._lines[idx,:3] / numpy.linalg.norm(self._lines[idx,:3])
        idx += 1
    
    
    #Places extreme points in cuboid by projecting axis points on plane
    #intersection lines and returns cuboid
    self._corners = numpy.array([[0,0,0]])
    
    for line in self._lines:
      corner = numpy.dot( line[3:],  line[:3].T
           ) * line[:3] + line[3:]
      self._corners = numpy.vstack(( self._corners, corner))
    
    #Removes possible bad values (NaN, Inf) from corners
    self._corners = self._corners[1:]
    
    idx = 0
    while idx < self._corners.shape[0]:
      
      
#    for index in range( len( self._corners )):
#      try:
      if ( numpy.isnan( self._corners[idx] ).any()
          or numpy.isinf( self._corners[idx] ).any()
          or numpy.isneginf( self._corners[idx] ).any() ):
        self._corners = numpy.delete(self._corners, idx, 0)
      else:
        idx += 1
#      except IndexError:
#          pass
    
    if (self._corners==0).all() or self._corners.shape[0] < 3:
      exit('Error:\nNo or insufficient corners found.\nExiting...\n')

      
    self._corners = numpy.vstack(( self._corners + self._shift_vector,
        self._corners + axis + self._shift_vector ))
    

  @classmethod  
  def _from_dict_helper(cls, geometry, args, periodicity):
    return cls(geometry,periodicity, args["planes_normal"],
        args["planes_miller"], args["shift_vector"], args["order"],
        args["shift_vector_coordsys"],args["planes_normal_coordsys"])

  def containing_cuboid(self,periodicity):
    '''Calculates the boundaries of the containing cuboid determined by axis'
    projection on boundary planes'''
    
    return numpy.vstack(( self._corners.min(axis=0), self._corners.max(axis=0) ))
  
  
  def atoms_inside(self, atoms, periodicity=None):
    '''Creates boolean array assigning True and False values towards points in
        and out of plane boundaries respectively'''
    
    #Calculates point_inside_body
    point_inside_body = numpy.array([0,0,0])

    for corner in self._corners:
      point_inside_body = (point_inside_body + corner)
    point_inside_body = (point_inside_body /
         self._corners.shape[0])
    
    #Distributes True and False values towards point_inside_body's respective
    #position towards each plane
    try:
      parameter = numpy.array([ (self._planes_normal[plane_idx,3] -
          numpy.dot( point_inside_body - self._shift_vector[0], 
          self._planes_normal[plane_idx,:3].T) )
          <= 0 for plane_idx in range( len( self._planes_normal )) ])
    except ZeroDivisionError:
         pass
    
    atoms_inside_body = numpy.zeros(atoms.shape[0], bool)
    
    #Retrieves periodic axis from periodicity
    axis = periodicity.get_axis("cartesian")
    
    #Determines for each point given if it shares the same position related to
    #each plane as the point_inside_body and if it's projection is within the
    #axis range
    for idx in range( len( atoms )):
      TF_planes = numpy.array([
          (self._planes_normal[plane_idx,3]
              - numpy.dot( ( atoms[idx,:3] - self._shift_vector )[0],
              self._planes_normal[plane_idx,:3].T) ) <= 0
              for plane_idx in range( len( self._planes_normal ))
          ])
      atoms_inside_body[idx] = ( TF_planes == parameter ).all()
    
    
    return atoms_inside_body
                        
  def miller_to_normal(self, geometry, plane_miller):
    '''Calculates the normal form of a plane defined by Miller indices'''
    
    return ( plane_miller[0] * numpy.cross(geometry._lattice_vectors[1],
        geometry._lattice_vectors[2]) + plane_miller[1] * numpy.cross(
        geometry._lattice_vectors[2], geometry._lattice_vectors[0] ) +
        plane_miller[2] * numpy.cross( geometry._lattice_vectors[0], 
        geometry._lattice_vectors[1] ) )