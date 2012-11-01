Invoking the program
====================

The behaviour of Nanocut is controlled via a few command line options and
through specifications in a configuration file. Latter is described in the
section :ref:`sec-inifile`.

You can get a short summary of the command line options by invoking the program
with the ``-h`` or ``--help`` option::

  nanocut -h

The usual way of invoking Nanocut is to pass it the name of the configuration
file and the name of the file, which the resulting structure should be stored
in::

  nanocut mycut.ini mycut.xyz

If your resulting structure is periodic, you may want to store the lattice
vectors in a separate file (instead in the xyz-file as comment line). This can
be achieved by specifying also the name of a lattice vector file on the command
line, e.g.::

  nanocut mycut.ini mycut.xyz mycut.latvecs


Command line options
--------------------

``-a``, ``--append``
  Append the resulting structure to the result file instead of overwriting it.

``-g``, ``--gen-format``
  Creates the result file in GEN format (suitable for the `DFTB+ program
  <http://www.dftb-plus.info>`_) instead  of XYZ.

``-h``, ``--help``
  Prints a short help about the usage of the program and exits.

``-o``, ``--orthogonal-latvecs``
  As most programs expect three dimensional periodic structures as input,
  Nanocut allows you to extend the periodicity of your resulting 0D, 1D or 2D
  structure to 3D using this option. You have to specify the length of the
  additional lattice vectors.

  For example after executing ::

    nanocut -o 30 mycut.ini mycut.xyz mycut.latvecs

  you would obtain in `mycut.latvecs` 3 lattice vectors. The lattice
  vectors which are not determined by the inherent translation vector(s) of your
  structure will be orthogonal to the inherent ones and have the specified
  length of 30 Angstrom.

``-v``, ``--verbosity``
  Sets the verbosity level of the program. Currently the values ``0`` (no output
  except error messages) and ``1`` (normal output, default) are allowed.

``--version``
  Prints the version number of the program and exits.
