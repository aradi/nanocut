import numpy as np
from nanocut.body import Body

class Cylinder(Body):
    """Class for right circular cylinders"""
    
    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "shift_vector": ( "floatarray", (3,), True, True ),
                 "point1": ( "floatarray", (3,), False, True ),
                 "point2": ( "floatarray", (3,), False, True ),
                 "radius1": ( "float", None, False, False ),
                 "radius2": ( "float", None, False, False )                 
                }
    
  
    def __init__(self, geometry, period, **kwargs):
        """Creates a Cylinder instance.
        
        Keyword args:
            point1: Middle point of the base circle.
            point2: Middle point of the top circle.
            radius1: Radius of the base circle.
            radius2: Radius of the top circle. 
        """
        Body.__init__(self, geometry, period, **kwargs)
        self._point1 = geometry.coord_transform(
            kwargs.get("point1"),
            kwargs.get("point1_coordsys", "lattice"))
        self._point2 = geometry.coord_transform(
            kwargs.get("point2"),
            kwargs.get("point2_coordsys", "lattice"))
        self._radius1 = kwargs.get("radius1")
        self._radius2 = kwargs.get("radius2")
        self._dir_vector = self._point2 - self._point1
        self._norm = np.linalg.norm(self._dir_vector)
  
  
    def containing_cuboid(self,periodicity=None):
        """Returns the edges of the containing cuboid (see Body class)."""
         
        dirvec0 = self._dir_vector / self._norm
        tmp = np.cross(dirvec0, np.eye(3, dtype=float))
        projs = np.sqrt(np.sum(tmp**2, axis=1))
        bounds = (np.vstack((
            self._point1 + self._radius1 * projs,
            self._point1 - self._radius1 * projs,
            self._point2 + self._radius2 * projs,
            self._point2 - self._radius2 * projs ))
            + self.shift_vector)
        return np.vstack(( bounds.min(axis=0), bounds.max(axis=0) ))
  
  
    def atoms_inside(self, atoms, periodicity=None):
        """Decides which atoms are inside the body (see Body class)."""

        dirvec0 = self._dir_vector / self._norm
        relpos = atoms - self._point1 - self.shift_vector
        dists = np.sqrt(np.sum(np.cross(relpos, dirvec0)**2, axis=1))
        heights = np.dot(relpos, dirvec0) / self._norm
        # maximal allowed distance at given height
        maxdists = self._radius1 + (self._radius2 - self._radius1) * heights
        atoms_inside = np.logical_and(
            np.logical_and(np.less_equal(dists, maxdists),
                           np.less_equal(heights, 1.0)),
            np.greater_equal(heights, 0.0))
        return atoms_inside
    