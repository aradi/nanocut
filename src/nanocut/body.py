import numpy as np
from .output import error

class Body:
    """Parent class for all geometrical bodies.
    
    Attributes:
        shift_vector: Origin of the body.
    """
        
    # (type, shape, optional, has_coordsys_version)
    arguments = {
                 "shift_vector": ( "floatarray", (3,), True, True ),    
    }
        
    
    def __init__(self, geometry, period, **kwargs):
        """Initializes instance.
        
        It processes following keywords in the passed dictionaries:
            shift_vector: Origin of the body.
            additive: Signalizes whether body is additive or subtractive.
        
        Args:
            geometry: Geometry of the base crystal (for coord. transformations)
            period: Periodicity of the target system.
        
        Keyword args:
            shift_vector: origin of the body as (3,) array.
            shift_vector_coordsys: coordinate system of the origin ("lattice"
                or "cartesian")
        """
        self.shift_vector = geometry.coord_transform(
            kwargs.get("shift_vector", np.zeros((3,), dtype=float)),
            kwargs.get("shift_vector_coordsys", "lattice"))


    @classmethod
    def fromdict(cls, geometry, period, configdict):
        """Create object from configuration dictionary.
        
        Args:
            geometry: Geometry of the base crystal.
            periodicity: Periodicity of the target object
            configdict: Dictionary with text representation of the objects
                keyword arguments.
                
        Returns:
            Initialized object.
        """
        argdict = cls.parse_arguments(cls.arguments, configdict)
        return cls(geometry, period, **argdict)
        

    @staticmethod
    def parse_arguments(arguments, configdict=None):
        """Selects body related items from configuration dictionary and converts
        them to their python type.
            
        Args:
            arguments: Dict of arguments to process.
            configdict: Dictionary with configuration items or None.
        
        Returns:
            Dictionary of body related entries only with values converted
            to their python type.
        """ 
        if configdict is None:
            return {}
        init_args = {}
        for arg, spec in arguments.items():
            
            # If non-optional argument is missing, stop.
            argvalue = configdict.get(arg, None)
            if argvalue is None:
                if spec[2]:
                    continue
                else:
                    error("Mandatory field '" + arg + "' missing.")
            
            if spec[0] == "floatarray":
                try:
                    argvalue = np.array([ float(el)
                                         for el in argvalue.split() ])
                except ValueError:
                    error("Supplied string for " + arg + 
                          " not convertible to float-array.")
                try:
                    argvalue.shape = spec[1]
                except ValueError:
                    error("Wrong number of elements supplied for " + arg + "'")

            elif spec[0] == "intarray":
                try:
                    argvalue = np.array([ int(el)
                        for el in argvalue.split() ])
                except ValueError:
                    error("Error:\n Supplied string for " + arg + 
                        " not convertible to integer-array")
                try:
                    argvalue.shape = spec[1]
                except ValueError:
                    error("Wrong number of elements supplied for " + arg + "'")

            elif spec[0] == "integer":
                try:
                    argvalue = int(argvalue)
                except ValueError:
                    error("Supplied string for " + arg +
                        " not convertible to integer.")

            elif spec[0] == "float":
                try:
                    argvalue = float(argvalue)
                except ValueError:
                    error("Supplied string for " + arg +
                        " not convertible to float.")
                    
            elif spec[0] == "logical":
                argvalue = argvalue.lower()
                if argvalue in [ "true", "on", "yes" ]:
                    argvalue = True
                elif argvalue in [ "false", "off", "no" ]:
                    argvalue = False
                else:
                    error("Invalid logical value '" + argvalue + "'")
                    
            else:
                error("Internal error:\n There is no valid argument type "
                      + spec[0] + " can't use fromdict() with this class.")
                
            init_args[arg] = argvalue
            
            if spec[3]:
                argcoordsys = arg + "_coordsys"
                argvalue = configdict.get(argcoordsys, "lattice")
                if argvalue in [ "lattice", "cartesian" ]:
                    init_args[argcoordsys] = argvalue
                else:
                    error("Supplied string '" + argvalue + 
                        "' for " + arg + "_coordsys is invalid.")
        return init_args


    def containing_cuboid(self):
        """Returns the edges of the containing cuboid.
        
        This method must be overriden in the child classes.
        
        Returns:
            Array of two 3D-vectors, the first one containing the lowest, the
            second one the highest x, y and z-values, which a point inside the
            body can have.
        """
        raise NotImplementedError
    
    
    def atoms_inside(self):
        """Decides which atoms are inside the body.
        
        This method must be overriden in the child classes.
        
        Returns:
            Logical array with True for all atoms inside the body.
        """
        raise NotImplementedError
    
