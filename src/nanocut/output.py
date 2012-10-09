import sys

# Verbosity level
verbosity = 1

# Indentation string in messages
INDENT_STR = " " * 2

def write_crystal(geometry, atoms_coords, atoms_idx, axis, resultfilename,
                  append, latvecsfilename):
    """Write out the resulting crystaline structure.
    
    Args:
        geometry: Geometry of the original crystal.
        atoms_coords: Coordinates of the atoms.
        atoms_idx: Type indices of the atoms.
        axis: Translational vectors.
        resultfilename: Name of the file to write the resulting structure.
        append: Whether the result file should be overwritten or appended.
        latvecsfilename: Name of the file to write the lattice vectors to
            instead to the xyz-file (or "").
    """
    # Write lattice vectors to file or to a comment line
    if latvecsfilename:
        printstatus("Writing lattice vector file '{}'".format(
            latvecsfilename))
        try:
            fp2 = open(latvecsfilename, "w")
        except IOError:
            error("Can't open '" + latvecsfilename + "'")
        for axisvec in axis:
            fp2.write("{:18.10f} {:18.10f} {:18.10f}\n".format(*axisvec))
        fp2.close()
        axis_string = ""
    else:
        tmp = [ "TV:"]
        for axisvec in axis:
            tmp.append(
                "({:.10f} {:.10f} {:.10f})".format(*axisvec))
        axis_string = " ".join(tmp)

    # Write xyz file
    natom = atoms_idx.shape[0]
    mode = "w+" if append else "w"
    printstatus("Writing structrure file '{}'".format(resultfilename))
    try:
        fp = open(resultfilename, mode)
    except IOError:
        error("Can't open '" + resultfilename + "'.")
    fp.write("{:d}\n{:s}\n".format(natom, axis_string))
    for it in range(len(atoms_coords)):
        fp.write(" {:<3s} {:18.10f} {:18.10f} {:18.10f}\n".format(
                geometry.get_name_of_atom(atoms_idx[it]),
                *atoms_coords[it,:]))
    fp.close()


def error(msg):
    """Write error message and exit.
    
    Args:
        msg: Error message.
    """
    print("Error: " + msg)
    print("Exiting...")
    sys.exit(1)


def warning(msg):
    """Print a warning.
    
    Args:
        msg: Warning message.
    """
    print("Warning: " + msg)


def printstatus(msg, indentlevel=0):
    """Print a status message, provided verbosity level is > 0.
    
    Args:
        msg: Message to be printed.
        indentlevel: Indentation level for the message.
    """
    if verbosity > 0:
        print(INDENT_STR * indentlevel + msg)


def set_verbosity(verbosity_level):
    """Set the verbosity level for the printstatus command.
    
    Args:
        verbosity_level: New verbosity level.
    """
    global verbosity
    verbosity = verbosity_level
    
    
def printheader():
    """Print header."""
    printstatus("*** Nanocut ***")
