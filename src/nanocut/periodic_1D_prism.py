import numpy as np
from nanocut.polyhedron import Polyhedron
from .output import error

class Periodic1DPrism(Polyhedron):
    """Class for periodic bodies bounded by a group of planes."""
    

    def __init__(self, geometry, period, configdict=None, **kwargs):
        """Extends the constructor of the Polyhedron class.
        """
        # Convert inidict entries to Python objects
        kwargs.update(self.parse_arguments(self.get_arguments(), configdict))

        # Check for plane normals not orthogonal to axis (plane cuts axis)        
        self.periodicity = period
        axis = self.periodicity.get_axis("cartesian")
        planes_normal = self.pop_planes(geometry, kwargs)
        projections = abs(np.dot(planes_normal[:,:3], axis.transpose())) 
        if np.any(projections > 1e-8):            
            error("Some plane(s) are not parallel to axis")
            
        # Determine basal planes. Shift them with a small amount to make sure
        # atoms do not stay outside due to arithmetic errors.
        axisnorm = np.linalg.norm(axis[0])
        axis0 = axis[0] / axisnorm
        basal_planes = np.array(
            [[ axis0[0], axis0[1], axis0[2], -1e-8 ],
             [ axis0[0], axis0[1], axis0[2], axisnorm + 1e-8 ]])
        
        # Extend planes by basal planes and call base class
        planes_normal = np.vstack(( basal_planes, planes_normal ))
        kwargs["planes_normal"] = planes_normal
        kwargs["planes_normal_coordsys"] = "cartesian"
        Polyhedron.__init__(self, geometry, period, **kwargs)
                       

    def atoms_inside(self, atoms):
        """Decides which atoms are inside the body (see Body class)."""
        
        atoms_inside_body = Polyhedron.atoms_inside(self, atoms)
        # Filtering here for periodic images needed
        
        atoms_inside_body *= self.periodicity.mask_unique(atoms,
                                                          atoms_inside_body)
        return atoms_inside_body
