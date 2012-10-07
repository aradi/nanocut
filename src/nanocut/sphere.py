import numpy as np
from nanocut.body import Body

class Sphere(Body):
    """Class for spheres"""
    
    # Create argument dictionary as union of parent class' dictionary
    # and extending keywords (only works since dictionary keys are stings)
    arguments = {
                 "shift_vector": ( "floatarray", (3,), True, True ),
                 "radius": ( "float", None, False, False ),
                 }

    
    def __init__(self, geometry, period, **kwargs):
        """Creates Sphere instance.
        
        Keyword args:
            shift_vector: Origin of the sphere.
            radius: Radius of the sphere.
        """
        Body.__init__(self, geometry, period, **kwargs)
        self.radius = kwargs.get("radius")
    
    
    def containing_cuboid(self, periodicity=None):
        """Returns the edges of the containing cuboid (see Body class).""" 
        return (self.radius * np.array([[ -1, -1, -1], [ 1, 1, 1 ]]) 
                + self.shift_vector)


    def atoms_inside(self, atoms, periodicity=None):
        """Decides which atoms are inside the body (see Body class)."""
        dists = np.sqrt(np.sum((atoms - self.shift_vector)**2, axis=1))
        return (dists <= self.radius)
    