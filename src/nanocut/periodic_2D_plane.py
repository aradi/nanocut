import numpy as np
from nanocut.common import PERIODIC_TOLERANCE
from nanocut.polyhedron import Polyhedron

class Periodic2DPlane(Polyhedron):
    """Class for plane elements with 2D periodicity"""
    
    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "shift_vector": ( "floatarray", (3,), True, True ),    
                 "thickness": ( "float", None, False, False )
                }

    def __init__(self, geometry, period, **kwargs):
        """Construct Periodic2DPlane instance.
        
        Keyword args:
            shift_vector: Origin of the body.
            thickness: Distance between the upper and lower plane.
        """
        self.periodicity = period
        self.thickness = kwargs.get("thickness") 
        axis1, axis2 = self.periodicity.get_axis("cartesian")
        # Surface normal vector
        surfnorm = np.cross(axis1, axis2).astype(float)
        surfnorm = surfnorm / np.linalg.norm(surfnorm)
        # Normal vector of the side planes of the polyhedron, pointing inwards
        n1 = np.cross(surfnorm, axis1)
        n1 /= np.linalg.norm(n1)
        n2 = np.cross(axis2, surfnorm)
        n2 /= np.linalg.norm(n2)
        # Distances of the side planes from the origin
        d1 = np.dot(n1, axis2)
        d2 = np.dot(n2, axis1)
        # Sign of the positive distance
        s1 = np.sign(d1)
        s2 = np.sign(d2)
        # Assemble polyhedron
        kwargs["planes_normal"] = np.array(
            [[ n1[0], n1[1], n1[2], 0.0 -s1 * PERIODIC_TOLERANCE ],
             [ n1[0], n1[1], n1[2], d1 + s1 * PERIODIC_TOLERANCE ],
             [ n2[0], n2[1], n2[2], 0.0 - s2 * PERIODIC_TOLERANCE ],
             [ n2[0], n2[1], n2[2], d2 + s2 * PERIODIC_TOLERANCE ],
             [ surfnorm[0], surfnorm[1], surfnorm[2], -self.thickness / 2.0 ],
             [ surfnorm[0], surfnorm[1], surfnorm[2], self.thickness / 2.0 ]
             ])
        kwargs["planes_normal_coordsys"] = "cartesian"
        Polyhedron.__init__(self, geometry, period, **kwargs)


    def atoms_inside(self, atoms):
        """Decides which atoms are inside the body (see Body class)."""
        
        atoms_inside_body = Polyhedron.atoms_inside(self, atoms)
        atoms_inside_body *= self.periodicity.mask_unique(
            atoms - self.shift_vector, atoms_inside_body)
        return atoms_inside_body
