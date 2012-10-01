import numpy as np
from nanocut.body import Body


class Periodic1DCylinder(Body):
    """Class for periodic cylinders determined by a central axis and radius"""
    
    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "radius": ( "float", None, False, False )
                 }

    def __init__(self, geometry, period, configdict=None, **kwargs):
        """Extends the constructor of the class Body.
        
        Additional keywords:
            radius: Radius of the cylinder.
        """
        Body.__init__(self, geometry, configdict=configdict, **kwargs)
        kwargs.update(self.parse_arguments(Periodic1DCylinder.arguments,
                                           configdict))
        self.radius = kwargs.get("radius")
        
        
    def containing_cuboid(self, periodicity):
        """Returns the edges of the containing cuboid (see Body class)."""
       
        # Creates cubes containing spheres with cylinder radius around axis'
        # beginning and end. (somewhat rude approximation)
        axis = periodicity.get_axis("cartesian") 
        bounds = np.vstack((
            self.shift_vector + self.radius,
            self.shift_vector - self.radius,
            axis + self.shift_vector + self.radius,
            axis + self.shift_vector - self.radius,
            ))
        return np.vstack((bounds.min(axis=0), bounds.max(axis=0)))


    def atoms_inside(self, atoms, periodicity):
        """Decides which atoms are inside the body (see Body class)."""

        # Checks if distance from axis is larger than radius for given atom        
        axis = periodicity.get_axis("cartesian")
        relpos = atoms - self.shift_vector[0]
        dirvec0 = axis[0] / np.linalg.norm(axis[0])
        dists = np.sqrt(np.sum(np.cross(relpos, dirvec0)**2, axis=1))
        atoms_inside = dists <= self.radius
        return atoms_inside
