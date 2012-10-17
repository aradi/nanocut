import numpy as np
from nanocut.common import PERIODIC_TOLERANCE
from nanocut.cylinder import Cylinder


class Periodic1DCylinder(Cylinder):
    """Class for periodic cylinders determined by a central axis and radius"""
    
    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "shift_vector": ( "floatarray", (3,), True, True ),
                 "radius": ( "float", None, False, False )
                 }

    def __init__(self, geometry, period, **kwargs):
        """Creates a Periodic1DCylinder instance.
        
        Keyword args:
            shift_vector: Origin of the body.        
            radius: Radius of the cylinder.
        """
        self.radius = kwargs.pop("radius")
        self.periodicity = period
        kwargs["radius1"] = self.radius
        kwargs["radius2"] = self.radius
        axis = period.get_axis("cartesian")[0]
        axisnorm = np.linalg.norm(axis) 
        kwargs["point1"] = -axis / axisnorm * PERIODIC_TOLERANCE 
        kwargs["point2"] = axis  + axis / axisnorm * PERIODIC_TOLERANCE 
        kwargs["point1_coordsys"] = "cartesian"
        kwargs["point2_coordsys"] = "cartesian"
        Cylinder.__init__(self, geometry, period, **kwargs)

        
    def atoms_inside(self, atoms):
        """Decides which atoms are inside the body (see Body class)."""
        
        atoms_inside = Cylinder.atoms_inside(self, atoms)
        atoms_inside *= self.periodicity.mask_unique(atoms - self.shift_vector,
                                                     atoms_inside)
        return atoms_inside
