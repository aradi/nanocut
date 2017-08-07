import numpy as np
import nanocut.common as nc 
from nanocut.output import error, printstatus

__all__ = [ "Periodicity", ]


def gcd(numbers):
    """Calculates greatest common divisor of a list of numbers."""
    
    aa = numbers[0]
    for bb in numbers[1:]:
        while bb:
            aa, bb = bb, aa % bb
    return aa


def plane_axis_from_miller(miller):
    """Returns two vectors in a plane with given miller index.
    
    Args:
        miller: Miller indices of the plane (array of 3 integers)
       
    Returns:
        Two 3D vectors in relative coordinates, both being vectors
        in the plane. It returns the shortest possible vectors.
    """
    # Separate zero and nonzero components of Miller vector
    nonzero = np.flatnonzero(np.not_equal(miller, 0))
    zero = np.flatnonzero(np.equal(miller, 0))
    miller_nonzero = miller[nonzero]
    # Get smallest possible intersections along lattice vectors
    factor = np.prod(miller_nonzero)
    relintersecs = factor / miller_nonzero
    relintersecs /= gcd(relintersecs)
    axis = np.zeros((2, 3), dtype=int)
    if len(relintersecs) == 1:
        # 2 zero components in Miller indices: plane parallel to the
        # corresponding lattice vectors 
        axis[0, zero[0]] = 1
        axis[1, zero[1]] = 1
    elif len(relintersecs) == 2:
        # 1 zero component: plane contains corresponding lattice vector.
        # other vector: difference of intersection points along the
        # other two lattice vectors.
        axis[0, zero[0]] = 1
        axis[1, nonzero[0]] = -relintersecs[0]
        axis[1, nonzero[1]] = relintersecs[1]
    else:
        # all components non-zero: Vectors from intersection point along
        # first lattice vector to the intersection points along the second and
        # third lattice vectors will spawn the plane.
        axis[0, nonzero[0]] = -relintersecs[0]
        axis[0, nonzero[1]] = relintersecs[1]
        axis[1, nonzero[0]] = -relintersecs[0]
        axis[1, nonzero[2]] = relintersecs[2]
    return axis


def cell_axis_from_superlattice(superlattice, latvecs):
    """Returns three vectors spawning a supercell similar to a given one.
    
    Args:
        superlattice: Lattice vectors of the supercell.
        latvecs: Original lattice vectors.
        
    Returns:
        Three vectors in relative coordinates (respective the original lattice
        vectors) which spawn a superlattice similar to the specified one.
    """ 
    # Transformation to build superlattice from current lattice vectors.
    trans = np.dot(superlattice, np.linalg.inv(latvecs))
    # Rescale transformation matrix to contain only elements >= 1.0.
    nonzero = np.nonzero(np.greater(np.abs(trans), nc.EPSILON))
    trans_nonzero = trans[nonzero]
    minelemind = np.argmin(np.abs(trans_nonzero))
    trans_nonzero /= abs(trans_nonzero[minelemind])
    # If biggest element greater tolerance: we would leave 64 bit integer range.
    if np.any(np.greater(np.abs(trans_nonzero), 11.0)):
        error("Target lattice coefficients too big")
    # Scale up transformation to ensure that all components are very close to
    # integers, if superlattice and lattice are commensurable
    factor = np.prod(np.arange(2, 11 + 1, dtype=int))
    trans_nonzero *= factor
    trans_nonzero_int = np.around(trans_nonzero).astype(int)
    # Check, whether all coefficients are close to integers.
    if np.any(np.abs(trans_nonzero_int - trans_nonzero) 
              > nc.RELATIVE_PERIODIC_TOLERANCE):
        error("Target lattice and source lattices probably incompatible")
    # Simplify transformation matrix with greatest common divisor.
    factor = gcd(abs(trans_nonzero_int.flatten()))
    trans_nonzero_int /= factor
    # Fill nonzero components into axis.
    axis = np.zeros((3, 3), dtype=int)
    axis[nonzero] = trans_nonzero_int
    return axis
    

class Periodicity:
    """Holds information about type of periodicity, and axes.
    
    Attributes:
        period_type: Type of the periodicity ("0D", "1D", "2D" or "3D")
        axis: Axis vector(s) in relatvie coordinates.
        axis_cart: Axis vector(s) in cartesian coordinates.
    """

    def __init__(self, geometry, period_type, axis=None):
        """Initialized Periodicity instance.
        
        Args:
            geometry: Geometry object to provide transformation.
            period_type: Periodicity type ("0D", "1D", "2D", "3D").
            axis: (3, -1) array with periodicity vectors in relative coords.
        """
        self.period_type = period_type
        if self.period_type not in [ "0D", "1D", "2D", "3D" ]:
            raise ValueError("Value of period_type is invalid.")
        if self.period_type == "0D":
            self.axis = None
            self.axis_cart = None
            return
        self.axis = np.array(axis, dtype=int)
        self.axis.shape = (-1, 3)
        self.axis_cart = geometry.coord_transform(self.axis, "lattice")


    def rotate_coordsys(self, atoms_coords):
        """Rotates coordinate system to have standardized z-axis.
        
        Args:
            atom_coords: Cordinate to rotate.
            
        Returns:
            New translational vectors and rotated coordinates. For 0D systems it
            returns an empty list and the original coordinates.
            For 1D systems periodicity will be along the z-axis,
            for 2D sytems z-axis will be orthogonal to the periodic directions
            and the first lattice vector will be along the x-axis.
            For 3D systems it returns lattice vectors and atom coordinates
            unchanged.
        """
        if self.period_type == "0D":
            return [], atoms_coords
        elif self.period_type == "1D":
            z_axis = self.axis_cart[0]
        elif self.period_type == "2D":
            z_axis = np.cross(self.axis_cart[0], self.axis_cart[1])
        elif self.period_type == "3D":
            return self.axis_cart, atoms_coords            

        # Calculate rotation angle and rotation axis
        z_axis= z_axis / np.linalg.norm(z_axis)
        angle = np.arccos(np.dot(z_axis, np.array([0,0,1])))
        rot = np.cross(z_axis, np.array([0,0,1]))
        norm = np.linalg.norm(rot)
        if norm > nc.EPSILON:
            rot /= norm
        sin = np.sin(angle)
        cos = np.cos(angle)

        # Calculate rotation matrix
        rotation_matrix = np.array([
            [ cos + rot[0] * rot[0] * (1 - cos),
             rot[1] * rot[0] * (1 - cos) + rot[2] * sin,
             rot[2] * rot[0] * (1 - cos) - rot[1] * sin ],  
            [ rot[0] * rot[1] * (1 - cos)- rot[2] * sin, 
             cos + rot[1] * rot[1] * (1 - cos),
             rot[2] * rot[1] * (1-cos) + rot[0] * sin, ],
            [ rot[0] * rot[2] * (1 - cos) + rot[1] * sin,
             rot[1] * rot[2] * (1 - cos) - rot[0] * sin,
             cos + rot[2] * rot[2] * (1 - cos) ]])

        # If 2D rotate first lattice vector to the x-axis
        axis = np.dot(self.axis_cart, rotation_matrix)
        if self.period_type == "2D":
            cos2 = axis[0,0] / np.linalg.norm(axis[0])
            sin2 = axis[0,1] / np.linalg.norm(axis[0])
            rot2 = np.array([[ cos2, -sin2, 0.0 ],
                             [ sin2, cos2, 0.0 ],
                             [ 0.0, 0.0, 1.0 ]], dtype=float)
            axis = np.dot(axis, rot2)
            rotation_matrix = np.dot(rotation_matrix, rot2)
        
        # Rotate atoms
        atoms_coords = np.dot(atoms_coords, rotation_matrix)
        
        return axis, atoms_coords


    def get_axis(self, coordsys="lattice"):
        """Returns axis.
        
        Args:
            coordsys: Coordinate system type ("lattice" or "cartesian").
            
        Returns:
            Periodicity axis in the given coordinate system.
        """
        if self.period_type  in [ "1D", "2D", "3D" ]:
            if coordsys == "lattice":
                return self.axis
            elif coordsys == "cartesian":
                return self.axis_cart
            else:
                raise ValueError("Value of coordsys is invalid.")
        else:
            raise ValueError("get_axis() called, but period_type is not 1D,"
                             " 2D or 3D.")


    def splitcoords(self, coords):
        """Splits Cartesian coordinates into relative and absolute parts.
        
        Args:
            coords: Cartesian coordinates to split.
            
        Returns:
            Tuple of relative and absolute coordinates. The original Cartesian
            coordinates can be obtained by calculating matrix product of the
            relative coordinates with the Cartesian axis vectors and adding the
            absolute coordinates to it. 
        """
        coords = np.array(coords)
        if self.period_type == "0D":
            return np.empty(( len(coords), 0 ), dtype=float), coords
        elif self.period_type == "1D":
            axis_norm = np.linalg.norm(self.axis_cart[0])
            relcoords = np.dot(coords, np.transpose(self.axis_cart[0])) 
            relcoords /= axis_norm**2
            relcoords.shape = (len(relcoords), 1)
        elif self.period_type == "2D":
            axis_3D = np.array(
                [ self.axis_cart[0], self.axis_cart[1],
                np.cross(self.axis_cart[0], self.axis_cart[1]) ])
            invbasis = np.linalg.inv(axis_3D)
            relcoords = np.dot(coords, invbasis)[:,0:2]
        elif self.period_type == "3D":
            invbasis = np.linalg.inv(self.axis_cart)
            relcoords = np.dot(coords, invbasis)
        shifts = coords - np.dot(relcoords, self.axis_cart)
        return relcoords, shifts
        

    def fold_to_unitcell(self, atoms_coords):
        """Folds atoms in the central unit cell, with relative coordinates
        between 0.0 and 1.0.
        
        Args:
            atoms_coords: Cartesian coordinates of the atoms. 
            
        Returns:
            Cartesian coordinates of the atoms in the unit cell.
        """
        atoms_coords = np.array(atoms_coords)
        if self.period_type == "0D":
            return atoms_coords
        relcoords, shifts = self.splitcoords(atoms_coords)        
        relcoords_folded = relcoords % 1.0
        atoms_coords = shifts + np.dot(relcoords_folded, self.axis_cart)  
        return atoms_coords


    def mask_unique(self, coords, mask=None):
        """Masks points being unique in the unit cell.
        
        Args:
            coords: Cartesian coordinates of the points (atoms).
            mask: Only those coordinates are considered, where mask is True
            
        Returns:
           Logical list containing True for unique atoms and False otherwise.
        """
        if mask is not None:                     
            unique = np.array(mask, dtype=bool)
        else:
            unique = np.ones(( coords.shape[0], ), dtype=bool)                
        if self.period_type == "0D":
            return unique
        relcoords, shifts = self.splitcoords(coords)
        relcoords = np.where(
            np.greater(relcoords, 1.0 - nc.RELATIVE_PERIODIC_TOLERANCE), 
            relcoords - 1.0, relcoords)
        onbounds = np.flatnonzero(np.any(np.less(relcoords, 0.01), axis=1))
        onbounds_rel = relcoords[onbounds]
        onbounds_cart = np.dot(onbounds_rel, self.axis_cart) + shifts[onbounds]
        for ii in range(len(onbounds_cart)):
            if not unique[onbounds[ii]]:
                continue
            diff = onbounds_cart[ii+1:] - onbounds_cart[ii]
            equiv = np.flatnonzero(np.less(np.sum(diff**2, axis=1),
                                           nc.DISTANCE_TOLERANCE**2))
            unique[onbounds[equiv + ii + 1]] = False
        return unique


    @classmethod
    def fromdict(cls, geometry, inidict):
        """Builds instance from dictionary."""

        period_type = inidict.get("period_type", "0D")
        if period_type not in [ "0D", "1D", "2D", "3D"]:
            error("Invalid periodicty type '" + period_type + "'")
        
        # 0D periodicity
        if period_type == "0D":
            return cls(geometry, "0D")

        # 1D periodicity        
        if period_type == "1D":
            axis = inidict.get("axis", None)
            if axis is None:
                error("Missing axis specification for 1D periodicity.")
            try:
                axis = np.array([ int(s) for s in axis.split() ])
                axis.shape = (1, 3)
            except ValueError:
                error("Invalid axis specification.")
            if np.all(axis == 0):
                error("Invalid axis direction.")
        
        # 2D periodicity
        elif period_type == "2D":
            axis = inidict.get("axis", None)
            miller = inidict.get("miller_indices", None)
            if axis is None and miller is None:
                error("Either 'axis' or 'miller_indices' needed for "
                      "periodicity specification.")
            elif axis is not None and miller is not None:
                error("Only one of the keywords 'axis' or 'miller_indices' can "
                      "be used for periodicity specification.")
            if miller:
                try:
                    miller = np.array([ int(s) for s in miller.split() ])
                    miller.shape = (3, )
                except ValueError:
                    error("Invalid miller index for 2D periodicity")
                if np.all(miller == 0):
                    error("Invalid miller index for 2D periodicity")
                axis = plane_axis_from_miller(miller)                 
            else:
                try:
                    axis = np.array([ int(s) for s in axis.split() ])
                    axis.shape = (2, 3)
                except ValueError:
                    error("Invalid axis specification.")
                if np.all(axis == 0):
                    error("Invalid axis direction.")
                if np.all(np.cross(axis[0], axis[1]) == 0):
                    error("Axis are parallel.")

        # 3D periodicity                
        else:
            axis = inidict.get("axis", None)
            superlattice = inidict.get("superlattice", None)
            if axis is None and superlattice is None:
                error("Either 'axis' or 'superlattice' needed for "
                      "periodicity specification.")
            elif axis is not None and superlattice is not None:
                error("Only one of the keywords 'axis' or 'superlattice'"
                      "can be used for periodicity specification.")                
            if superlattice:
                try:
                    superlattice = np.array([ float(s) 
                                             for s in superlattice.split() ])
                    superlattice.shape = (3, 3)
                except ValueError:
                    error("Invalid superlattice specification")
                if np.abs(np.linalg.det(superlattice)) < nc.EPSILON:
                    error("Linearly dependent superlattice vectors")
                axis = cell_axis_from_superlattice(superlattice,
                    np.dot(geometry.bravais_cell, geometry.latvecs))
            else: 
                try:
                    axis = np.array([ int(s) for s in axis.split() ])
                    axis.shape = (3, 3)
                except ValueError:
                    error("Invalid axis specification.")
                if np.all(axis == 0):
                    error("Invalid axis direction.")
                if np.abs(np.linalg.det(axis)) < nc.EPSILON:
                    error("Linearly dependent axis")

        # Switch back to primitive lattice, if necessary                    
        if np.any(geometry.bravais_cell != np.eye(3, dtype=int)):
            printstatus("Axis with respect to Bravais lattice:")
            for vec in axis:
                printstatus("{:3d} {:3d} {:3d}".format(
                    *[ int(ss) for ss in vec ]), indentlevel=1)
            axis = np.dot(axis, geometry.bravais_cell)
            
        # Get smallest possible unit cell
        for ii in range(len(axis)):
            divisor = gcd(abs(axis[ii]))
            axis[ii] = axis[ii] // divisor
                    
        printstatus("Axis with respect to primitive lattice:")
        for vec in axis:
            printstatus("{:3d} {:3d} {:3d}".format(
                *[ int(ss) for ss in vec ]), indentlevel=1)
                
        # Repeat unit cell
        cellrep = inidict.get("axis_repetition", None)
        if cellrep:
            try:
                cellrep = np.array([ float(s) for s in cellrep.split() ])
                cellrep.shape = (int(period_type[0]), )
            except ValueError:
                error("Invalid axis repetition specification.")
            axis = np.array(axis * cellrep[:,np.newaxis], int)
            printstatus("Axis repetition:"
                + " ".join([ "{:3d}".format(int(s)) for s in cellrep ]))

        return cls(geometry, period_type, axis)
