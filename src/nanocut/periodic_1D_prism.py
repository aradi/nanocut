import numpy as np
from nanocut.common import EPSILON, PERIODIC_TOLERANCE
from nanocut.polyhedron import Polyhedron
from nanocut.output import error

class Periodic1DPrism(Polyhedron):
    """Class for periodic bodies bounded by a group of planes."""
    

    def __init__(self, geometry, period, **kwargs):
        """Construct Periodic1DPrism instance.
        
        Keyword args:
            shift_vector: Origin of the body.
            planes_normal: Plane definitions with normal vectors and distances.
            planes_miller: Plane definitions with miller indices and distances.
        """
        # Check for plane normals not orthogonal to axis (plane cuts axis)        
        self.periodicity = period
        axis = self.periodicity.get_axis("cartesian")
        planes_normal = self.pop_planes(geometry, kwargs)
        projections = abs(np.dot(planes_normal[:,:3], axis.transpose())) 
        if np.any(projections > EPSILON):            
            error("Some plane(s) are not parallel to axis")
            
        # Determine basal planes. Shift them with a small amount to make sure
        # atoms do not stay outside due to arithmetic errors.
        axisnorm = np.linalg.norm(axis[0])
        axis0 = axis[0] / axisnorm
        basal_planes = np.array(
            [[ axis0[0], axis0[1], axis0[2], -PERIODIC_TOLERANCE ],
             [ axis0[0], axis0[1], axis0[2], axisnorm + PERIODIC_TOLERANCE ]])
        
        # Extend planes by basal planes and call base class
        planes_normal = np.vstack(( basal_planes, planes_normal ))
        kwargs["planes_normal"] = planes_normal
        kwargs["planes_normal_coordsys"] = "cartesian"
        Polyhedron.__init__(self, geometry, period, **kwargs)
                       

    def atoms_inside(self, atoms):
        """Decides which atoms are inside the body (see Body class)."""
        
        atoms_inside_body = Polyhedron.atoms_inside(self, atoms)
        atoms_inside_body *= self.periodicity.mask_unique(
            atoms - self.shift_vector, atoms_inside_body)
        return atoms_inside_body
