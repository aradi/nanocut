import numpy as np
from .body import Body
from nanocut.common import EPSILON
from nanocut.output import error


class Polyhedron(Body):
    """Class for bodies cut via planes"""

    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "shift_vector": ( "floatarray", (3,), True, True ),
                 "planes_normal": ( "floatarray", (-1,4), True, True ),
                 "planes_miller": ( "floatarray", (-1,4), True, False ),
    }

    def __init__(self, geometry, period, **kwargs):
        """Constructs Polyhedron instance.

        Keyword args:
            shift_vector: Origin of the body.
            planes_normal: Plane definitions with normal vectors and distances.
            planes_miller: Plane definitions with miller indices and distances.
        """
        Body.__init__(self, geometry, period, **kwargs)

        # Norm normal vectors
        planes_normal = self.pop_planes(geometry, kwargs)
        norms = np.sqrt(np.sum(planes_normal[:,0:3]**2, axis=1))
        planes_normal[:,0:3] /= norms[:,np.newaxis]

        # Remove identical planes (identical = parallel, but not antiparallel,
        # with similar distance from origin)
        unique = np.ones(( len(planes_normal), ), dtype=bool)
        for i1 in range(len(planes_normal)):
            if not unique[i1]:
                continue
            for i2 in range(i1 + 1, len(planes_normal)):
                if not unique[i2]:
                    continue
                ddiff = planes_normal[i1, 3] - planes_normal[i2, 3]
                cross = np.cross(planes_normal[i1, 0:3], planes_normal[i2, 0:3])
                vsum = planes_normal[i1, 0:3] + planes_normal[i2, 0:3]
                unique[i2] = (abs(ddiff) > EPSILON
                              or np.any(abs(cross)) > EPSILON
                              or np.all(abs(vsum) < EPSILON))
        self.planes_normal = planes_normal[unique]

        # Solve a linear equation for each triplet of planes returning their
        # vertex, ignore parallel planes
        self.corners = []
        for i1 in range(0, len(self.planes_normal)):
            for i2 in range(i1 + 1, len(self.planes_normal)):
                for i3 in range(i2 + 1, len(self.planes_normal)):
                    coeffs = np.vstack((
                                        self.planes_normal[i1, 0:3],
                                        self.planes_normal[i2, 0:3],
                                        self.planes_normal[i3, 0:3] ))
                    det = np.linalg.det(coeffs)
                    if abs(det) < EPSILON:
                        continue
                    rhs = np.vstack((
                                     self.planes_normal[i1, 3],
                                     self.planes_normal[i2, 3],
                                     self.planes_normal[i3, 3] ))
                    corner = np.dot(np.linalg.inv(coeffs), rhs)
                    self.corners.append(corner.flatten())
        self.corners = np.array(self.corners)

        if np.all(len(self.corners) < 4 or abs(self.corners) < EPSILON):
            exit('Error:\nNo or insufficient corners found.\nExiting...\n')
        self.corners += self.shift_vector


    @staticmethod
    def pop_planes(geometry, kwargs):
        # Convert miller index specifications to normal vectors
        miller_defs = kwargs.pop("planes_miller", None)
        if miller_defs is not None:
            if np.any(np.all(abs(miller_defs[:,0:3]) < EPSILON, axis=1)):
                error("Emtpy miller index tuple")
            miller_defs[:,0:3] = miller_to_normal(
                np.dot(geometry.latvecs, geometry.bravais_cell),
                miller_defs[:,0:3])
        else:
            miller_defs = np.zeros((0, 4), dtype=float)

        # Convert plane normal vector specifications into cartesian coords.
        normal_defs = kwargs.pop("planes_normal", None)
        if normal_defs is not None:
            normal_defs[:,0:3] = geometry.coord_transform(
                normal_defs[:,0:3],
                kwargs.pop("planes_normal_coordsys", "lattice"))
            if np.any(np.all(abs(normal_defs[:,0:3]) < EPSILON, axis=1)):
                error("Emtpy normal vector definition")
        else:
            normal_defs = np.zeros((0, 4), dtype=float)

        # Append two defintions
        planes_normal = np.vstack(( miller_defs, normal_defs ))
        return planes_normal


    def containing_cuboid(self):
        """Returns the edges of the containing cuboid (see Body class)."""
        return np.vstack(( self.corners.min(axis=0),
                           self.corners.max(axis=0) ))


    def atoms_inside(self, atoms):
        """Decides which atoms are inside the body (see Body class)."""
        # An atom is inside, if projections along all plane normals have the
        # same sign as an arbitrary point (center of mass) in the polyhedron.
        point_inside = (np.sum(self.corners, axis=0) / float(len(self.corners))
                        - self.shift_vector)
        atoms_relative = atoms[:,:3] - self.shift_vector
        normvecs = np.transpose(self.planes_normal[:,0:3])
        normdists = self.planes_normal[:,3]
        sign_point = (normdists - np.dot(point_inside, normvecs) <= 0.0)
        sign_atoms = (normdists - np.dot(atoms_relative, normvecs) <= 0.0)
        compared = (sign_atoms == sign_point)
        atoms_inside_body = np.all(compared, axis=1)
        return atoms_inside_body


def miller_to_normal(latvecs, miller_indices):
    """Calculates the normal form of a plane defined by Miller indices.

    Args:
       latvecs: Lattice vectors.
       miller_indices: Miller indices.

    Returns:
        Cartesian normal vector(s) of the plane(s).
    """
    invlatvecs = np.linalg.inv(latvecs)
    normals = np.dot(miller_indices, invlatvecs)
    return normals
