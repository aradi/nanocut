import numpy as np
from .output import error

class Body:
    """Parent class for all geometrical bodies.
    
    Attributes:
        additive: Signalizes whether content should be added or subtracted.
        shift_vector: Origin of the body.
        periodicity: Stores information about periodicity.
        
    Class attributes:
        arguments: Dictionary of names which can occure as arguments in the
            configuration dictionary for that class. The correpsonding values
            [ type_string, shape, optional, is_coord_sys_definable ]
            Child classes should define it according their needs.
    """
    
    arguments = {
                 "shift_vector": ( "floatarray", (1, 3), True, True ),
                 "additive": ( "logical", None, True, False ),
                 }

    
    def __init__(self, geometry, period, configdict=None, **kwags):
        """Initializes instance.
        
        It processes following keywords in the passed dictionaries:
            shift_vector: Origin of the body.
            additive: Signalizes whether body is additive or subtractive.
        
        Args:
            geometry: Geometry of the base crystal (for coord. transformations)
            period: Periodicity object.
            configdict: Configuration dictionary with text representation of
                keywords.
            **kwags: Dictionary Python values for the keywords.
        """
        kwags.update(self.parse_arguments(self.get_arguments(), configdict))
        self.shift_vector = geometry.coord_transform(
            kwags.get("shift_vector", np.zeros((3,), dtype=float)),
            kwags.get("shift_vector_coordsys", "lattice"))
        self.additive = kwags.pop("additive", True)
        self.periodicity = period


    @staticmethod
    def get_arguments():
        """Returns a dictioniary of the defintions of the configuration settings
        the object can process.
        """ 
        return Body.arguments


    @staticmethod
    def parse_arguments(arguments, configdict=None):
        """Selects body related items from configuration dictionary and converts
        them to their python type.
            
        Args:
            arguments: Dict of arguments to process.
            configdict: Dictionary with configuration items or None.

        
        Returns:
            Dictionary of body related entries only with Python values.
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
    
