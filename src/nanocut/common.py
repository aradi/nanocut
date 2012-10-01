import numpy as np

def miller_to_normal(latvecs, miller_indices):
    """Calculates the normal form of a plane defined by Miller indices.
    
    Args:
       latvecs: Lattice vectors.
       miller_indices: Miller indices.
       
    Returns:
        Normal vector(s) of the plane(s).
    """
    invlatvecs = np.linalg.inv(latvecs)
    normals = np.dot(miller_indices, invlatvecs)
    return normals
