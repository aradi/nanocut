import numpy as np
from nanocut.common import PERIODIC_TOLERANCE
from nanocut.polyhedron import Polyhedron

class Periodic3DSupercell(Polyhedron):
    """Class for plane elements with 2D periodicity"""
    
    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "shift_vector": ( "floatarray", (3,), True, True ),
                }

    def __init__(self, geometry, period, **kwargs):
        """Construct Periodic3DSupercell instance.
        
        Keyword args:
            shift_vector: Origin of the body.
            thickness: Distance between the upper and lower plane.
        """
        self.periodicity = period
        
        axis1, axis2, axis3 = self.periodicity.get_axis("cartesian")
        # Normal vector of the side planes of the polyhedron
        n12 = np.cross(axis1, axis2)
        n23 = np.cross(axis2, axis3)
        n31 = np.cross(axis3, axis1)
        n12 /= np.linalg.norm(n12)
        n23 /= np.linalg.norm(n23)
        n31 /= np.linalg.norm(n31)
        # Distances of the side planes from the origin
        d12 = np.dot(n12, axis3)
        d23 = np.dot(n23, axis1)
        d31 = np.dot(n31, axis2)
        # Sign of positive distance 
        s12 = np.sign(d12)
        s23 = np.sign(d23)
        s31 = np.sign(d31)
        # Assemble polyhedron
        kwargs["planes_normal"] = np.array(
            [[ n12[0], n12[1], n12[2], -s12 * PERIODIC_TOLERANCE ],
             [ n23[0], n23[1], n23[2], -s23 * PERIODIC_TOLERANCE ],
             [ n31[0], n31[1], n31[2], -s31 * PERIODIC_TOLERANCE ],
             [ n12[0], n12[1], n12[2], d12 + s12 * PERIODIC_TOLERANCE ],
             [ n23[0], n23[1], n23[2], d23 + s23 * PERIODIC_TOLERANCE ],
             [ n31[0], n31[1], n31[2], d31 + s31 * PERIODIC_TOLERANCE ],
             ])
        kwargs["planes_normal_coordsys"] = "cartesian"
        Polyhedron.__init__(self, geometry, period, **kwargs)


    def atoms_inside(self, atoms):
        """Decides which atoms are inside the body (see Body class)."""
        
        atoms_inside_body = Polyhedron.atoms_inside(self, atoms)
        atoms_inside_body *= self.periodicity.mask_unique(
            atoms - self.shift_vector, atoms_inside_body)
        return atoms_inside_body
