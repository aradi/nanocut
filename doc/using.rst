Using Nanocut
=============

Command line options
--------------------

The behaviour of Nanocut is controlled via a few command line options and
through specifications in a configuration file. You can get a short summary of
the command line options by invoking the program with the ``-h`` or ``--help``
option::

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

As most programs want three dimensional periodic structures as input, Nanocut
allows you to extend the periodicity of your resulting structure to 3D using the
``-o`` option. For example after executing::

  nanocut -o 30 mycut.ini mycut.xyz mycut.latvecs

you would obtain a file `mycut.latvecs` with 3 lattice vectors. The length of
the additional lattice vectors (not determined by the resulting structure) would
be 30 Angstrom, and those lattice vector(s) would be orthogonal to the
translation vector(s) of your resulting structure.


Configuration file
------------------

The configuration file uses the INI-format. In the configuration file you tell
Nanocut

* the structure of the original bulk 3D crystal,
* the periodicity of the resulting object,
* the shape of the resulting object.

Each of them corresponds to a section in the file with additional options
within. For example, in order to cut out a spherical diamond cluster with radius
10 Angstrom, the configuration file would look as follows::

  [geometry]
  # Diamond lattice vectors in Angstrom
  lattice_vectors:
    0.000 1.790 1.790
    1.790 0.000 1.790
    1.790 1.790 0.000

  basis:
    C  0.0  0.0  0.0
    C  0.25 0.25 0.25

  [periodicity]
  period_type: 0D
  
  [sphere:1]
  radius: 10

Please note, that option values going over more than one line require that the
continuation lines are indented by at least one whitespace character (like for
``lattice_vectors`` and ``basis`` above).  Lines starting with hashmark (``#``)
are treated as comments.

Below you find the formal description of the different options. For more
examples see the chapter :ref:`sec-examples`.


Geometry
********

The ``[geometry]`` section contains all information regarding the crystal
structure. Following options can be specified:

`lattice_vectors`
  Defines the three lattice vectors of the crystal structure in Cartesian
  coordinates in Angstrom units.

`basis`
  Chemical symbol of each basis atom followed by its coordinates. Coordinates
  are interpreted as fractional coordinates, unless specified differently in the
  option `basis_coordsys`.

`basis_coordsys` (optional)
  Defines the coordinate system of the basis. Possible values are ``lattice``
  (fractional coordinates) and ``cartesian`` (cartesian coordinates in Angstrom)
  with first being the default.


Periodicity
***********

Structures with periodicity in one or two dimensions require the
``[periodicity]`` section defining the type of periodicity and the axis or axes
of the translations. Following options can be specified:

`period_type`
  Defines the number of directions in which the structure is periodic. Possible
  values are ``0D``, ``1D``, ``2D`` or ``3D``. Specifying ``0D`` is equivalent
  to leaving out the whole section.

`axis`
  Defines the axis alongside which the supercell is periodic for the ``1D``,
  ``2D`` and ``3D`` cases. You must specifiy one vector (3 elements), two
  vectors (6 elements) or 3 vectors (9 elements), respectively. The numbers are
  interpreted as fractional coordinates of the crystal lattice and must be
  integer numbers.



Cutting bodies
**************

The configuration file can contain an arbitrary number of sections defining
bodies. Each body section is opened by ``[BODY: NAME]`` where ``BODY`` defines
the body's type and ``NAME`` is an unique name to distinguish different bodies
with equal types. The bodies are cut from the crystal in the order they appear
in the configuration file. Depending on their flag, they are added to or removed
from the result of previous cut. Consequently, the first cut should be additive.

Below you find the specification for each body. All of them support support the
following options:

`shift_vector` (optional)
  Shifts the defined body with the given vector.

`shift_vector_coordsys` (optional)
  Coordinate system of the shift vector. Values ``lattice`` (default) and
  ``cartesian`` can be used to interprete the components of `shift_vector` as
  fractional or Cartesian coordinates, 

`additive` (optional)
  Specifies whether the atoms inside the given body should be added to or
  subtracted from the previous structure.


Sphere
^^^^^^
Specified as ``[sphere: NAME]`` with following options:

`radius`
  Radius of the sphere.


Cylinder
^^^^^^^^

The section ``[cylinder: NAME]`` section specifies a body with circular base and
top areas which are orthogonal to the difference vector of their centers. The
circumference of the circles at the top and the bottom are connected by the
smallest lateral area possible. As the radius of the circles can be different,
you can also create truncated cones.

`point1`, `point2`
  Position vectors to the center of the first and second circular area.

`radius1`, `radius2`
  Radius of the circular areas.

`point1_coordsys`, `point2_coordsys` (optional)
  Coordinate system for the position vectors (``lattice`` or ``cartesian``).


Polyhedron
^^^^^^^^^^

The section ``[polyhedron: NAME]`` specifies a convex polyhedron defined by
its delimiting planes. Planes can be defined using Miller indices or their
normal vector.

`planes_miller` 
  Miller indices of the delimiting planes (except those defined using normal
  vectors) followed by their distance from the origin.

`planes_normal` 
  Orthogonal vectors for each plane (except those defined using Miller
  indices) followed by their distance from the origin. The vectors do not need to
  be normalized.

`planes_normal_coordsys`
  Coordinate system for the normal vectors of the planes (``lattice`` or
  ``cartesian``). 


Periodic cylinder (1D)
^^^^^^^^^^^^^^^^^^^^^^

The section ``[periodic_1D_cylinder: NAME]`` specifies a supercell of an
infinitely long cylinder with a circular base area. The base area's center is
the origin and its normal vector is parallel to the axis specified in the
``[periodicity]`` section.

`radius`
  The cylinders radius.


Periodic convex prism (1D)
^^^^^^^^^^^^^^^^^^^^^^^^^^

The section ``[periodic_1D_prism: NAME]`` specifies an infinitely long prism
with a convex polygon as base area. The prism is defined by its lateral
planes. A plane can be defined using it's Miller indices or it's normal
vector. The planes must be parallel to the periodicity axis specified in the
``[periodicity]`` section.

`planes_miller`
  Miller indices of the delimiting planes (except those defined using normal
  vectors) followed by their distance from the origin.


`planes_normal`
  Vector orthogonal to each plane (except those defined using Miller indices)
  followed by its distance from the origin. 

`planes_normal_coordsys`
  Coordinate system for the normal vectors of the planes (``lattice`` or
  ``cartesian``).


Slab (2D)
^^^^^^^^^

The ``[periodic_2D_plane]`` section specifies a slab delimited by two parallel
planes and being periodic along the planes. The upper and lower limiting planes
are equidistant from the origin. The direction of the limiting planes are
automatically derived from the periodicity specified in the ``[periodicity]``
section.

`thickness`
  Thickness of the slab.


Supercell (3D)
^^^^^^^^^^^^^^

The ``[periodic_3D_supercell]`` section specifies a supercell built from the
unit cell of the original crystal.
