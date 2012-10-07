import sys

verbosity = 1
INDENT_STR = " " * 2

def write_crystal(geometry, atoms_coords, atoms_idx, axis_string, 
                  resultfilename, append):
    
    natom = atoms_idx.shape[0]
    mode = "w+" if append else "w"
    try:
        fp = open(resultfilename, mode)
    except IOError:
        exit("Error: Can't open '" + resultfilename + "'.\nExiting...")
    fp.write("{:d}\n{:s}\n".format(natom, axis_string))
    for it in range(len(atoms_coords)):
        fp.write(" {:<3s} {:18.10E} {:18.10E} {:18.10E}\n".format(
                geometry.get_name_of_atom(atoms_idx[it]),
                *atoms_coords[it,:]))
    fp.close()


def error(msg):
    print("Error: " + msg)
    print("Exiting...")
    sys.exit(1)


def warning(msg):
    print("Warning: " + msg)


def printstatus(msg, level=0):
    if verbosity > 0:
        print(INDENT_STR * level + msg)


def set_verbosity(verbosity_level):
    verbosity = verbosity_level
    
    
def printheader():
    printstatus("*** Nanocut ***")
