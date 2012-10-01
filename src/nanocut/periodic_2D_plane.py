import numpy as np
from nanocut.body import Body

class Periodic2DPlane(Body):
    """Class for plane elements with 2D periodicity"""
    
    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "thickness": ( "float", None, False, False )
                }

    def __init__(self, geometry, period, configdict=None, **kwargs):
        """Extends the constructor of the class Body.
        
        Additional keywords:
            thickness: Slab thickness.
        """
        Body.__init__(self, geometry, configdict=configdict, **kwargs)
        kwargs.update(self.parse_arguments(Periodic2DPlane.arguments,
                                           configdict))
        self.thickness = kwargs.get("thickness")
        
 
    def containing_cuboid(self, periodicity):
        """Calculates the boundaries of the cuboid containing a plane element"""
        axis = periodicity.get_axis("cartesian")
        bounds = np.vstack((
            self.shift_vector + self.thickness,
            self.shift_vector - self.thickness,
            axis[0] + self.shift_vector + self.thickness,
            axis[0] + self.shift_vector - self.thickness,
            axis[1] + self.shift_vector + self.thickness,
            axis[1] + self.shift_vector - self.thickness,
            ))
        print("CUBOID:")
        print(np.vstack((bounds.min(axis=0), bounds.max(axis=0))))
        return np.vstack((bounds.min(axis=0), bounds.max(axis=0)))


    def atoms_inside(self, atoms, periodicity):
        """Decides which atoms are inside the body (see Body class)."""
        axis = periodicity.get_axis("cartesian")
        non_periodic_dir = np.cross(axis[0], axis[1]).astype(float)
        non_periodic_dir = non_periodic_dir / np.linalg.norm(non_periodic_dir)
        relcoords = atoms - self.shift_vector
        dists = np.abs(np.dot(relcoords, non_periodic_dir))
        atoms_inside = (dists <= self.thickness / 2.0) 
        return atoms_inside