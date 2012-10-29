.. _sec-inifile:

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


.. _sec-geometry:

Geometry
********

The `[geometry]` section contains all information regarding the crystal
structure. Following options can be specified:

`lattice_vectors`
  Defines the three lattice vectors of the crystal structure in Cartesian
  coordinates in Angstrom units.

  For example the diamond fcc lattice would look like::

    lattice_vectors: 
      0.000  1.785  1.785
      1.785  0.000  1.785
      1.785  1.785  0.000

`basis`
  Chemical symbol of each basis atom followed by its coordinates. Coordinates
  are interpreted as fractional coordinates, unless specified differently in the
  option `basis_coordsys`.

  Again taking the diamond unit cell as example, you would have to use::

    basis:
      C     0.00     0.00   0.00
      C     0.25     0.25   0.25

`basis_coordsys` (optional)
  Defines the coordinate system of the basis. Possible values are ``lattice``
  (fractional coordinates) and ``cartesian`` (Cartesian coordinates in Angstrom)
  with ``lattice`` being the default.

  To indicate that coordinates in the `basis` section are Cartesian coordinates
  in Angstrom (instead of fractional coordinates), you would have to write::

    basis_coordsys: cartesian

`shift_vector` (optional) 
  It shifts the coordinates of the basis atoms by the given amount. You can
  use it to create structures with a different origin as the one you would
  obtain based on the specified coordinates. It is specified in
  fractional coordinates, unless set in `shift_vector_coordsys` differently.

  If you wanted the diamond lattice from the example above being centered around
  a tetrahedral interstitial site (instead of the atom in the origin), you could
  issue::

    shift_vector: 0.25 0.25 0.25

`shift_vector_coordsys` (optional)
  Coordinate system of the shift vector: ``lattice`` (default) or ``cartesian``.

`bravais_cell` (optional)
  Specifies the conventional Bravais cell as linear combination of the primitve
  lattice vectors (3x3 integers). If set, the axis specifications in the
  `periodicity` section and any Miller indices in the input file will
  interpreted with respect to the conventional Bravais cell. (The `superlattice`
  option in the `periodicity` section can be used to find out the transformation
  vector for the conventional Bravais cell.)

  The cubic Bravais cell of diamond would require the input::

    bravais_cell:
      -1  1  1
       1 -1  1
       1  1 -1


Periodicity
***********

Structures with periodicity in one or two dimensions require the
`[periodicity]` section defining the type of periodicity and the axis or axes
of the translations. Following options can be specified:

`period_type`
  Defines the number of directions in which the structure is periodic. Possible
  values are ``0D``, ``1D``, ``2D`` or ``3D``. Specifying ``0D`` is equivalent
  to leaving out the whole section.

`axis` (mandatory for 1D, optional for 2D and 3D)
  Defines the axis/axes alongside which the supercell is periodic for the
  ``1D``, ``2D`` and ``3D`` cases. You must specifiy one vector (3 elements) for
  1D, two vectors (6 elements) for 2D and 3 vectors (9 elements) for 3D,
  respectively. Depending on the settings in the `[geometry]` section
  (:ref:`sec-geometry`), the numbers are interpreted as fractional coordinates
  of either the primitive lattice or the conventional Bravais
  lattice. The numbers must be integers. For 2D and 3D periodicity you can
  alternatively use the keywords `miller_indices` or `superlattice`.

  A nanowire along the 001 direction can be specified as::

    period_type: 1D
    axis: 0 0 1

  A slab in the plane of the vectors 100 and 010 can be specified as::
  
    period_type: 2D
    axis:
      1 0 0
      0 1 0

  A possible 3D supercell definition could look like::
  
     period_type: 3D
     axis:
       -1  1  1
        1 -1  1
        1  1 -1

`axis_repetition` (optional)
  Integer scaling factors for the translational vectors. Nanocut creates per
  default the smallest possible unit cell.  It requires one (1D), two (2D) or
  three (3D) integer numbers, respectively. Default value is one for all axis
  (no enlargment of the cell).

  In order to enlarge a 3D supercell by a factor of 2 along every direction,
  you would have to enter::

    axis_repetition: 2 2 2

`miller_indices` (optional, only for 2D)
  In the case of 2D periodicity, you can specify the Miller indices of the slab
  plane with this keyword (instead of specfying two axis vectors with the `axis`
  keyword). It needs 3 integer numbers. The program will create the shortes
  possible unit cell on the surface, which you can enlarge using the
  `axis_repetition` keyword if needed. Depending on the settings in the
  `[geometry]` section (:ref:`sec-geometry`), the numbers are interpreted with
  respect to the primitive lattice or the conventional Bravais lattice.

  The following example shows the input for a 211 surface slab::

    miller_indices: 2 1 1

`superlattice` (optional, only for 3D)
  Allows to specify the Cartesian coordinates of a superlattice (instead of
  specifying the relative coordinates with the `axis` keyword). It needs 9 real
  numbers (components of the three superlattice vectors). Nanocut will try to
  build an integer linear combination of the lattice vectors of the primitive
  lattice (or the Bravais lattice, if specified) to create a superlattice
  similar to the specified one. The absolute size of the superlattice vectors is
  irrelevant, but their relative size and their angles must yield a lattice
  which is compatible with the original one. Nanocut will create the smallest
  possible 3D cell, which can be enlarged using the `axis_repetition` keyword if
  necessary.

  To search for a cubic supercell for a given lattice, you should specify::

    superlattice:
      1.0  0.0  0.0
      0.0  1.0  0.0
      0.0  0.0  1.0



Cutting bodies
**************

The configuration file can contain an arbitrary number of sections defining
bodies. Each body section is opened by `[BODY: NAME]` where `BODY` defines
the body's type and `NAME` is an unique name to distinguish different bodies
with equal types. The bodies are cut from the crystal in the order they appear
in the configuration file. Depending on their flag, they are added to or removed
from the result of the previous cut. Trivially, the first cut should be
additive.

Below you find the individual specification for each body. All of them support
the following options:

`shift_vector` (optional)
  Shifts the defined body with the given vector.

  To shift the origin of the cutting body by 1 Angstrom along the z-axis, you
  should specify::

    shift_vector: 0.0  0.0  1.0
    shift_vector_coordsys: cartesian

`shift_vector_coordsys` (optional)
  Coordinate system of the shift vector. Values ``lattice`` (default) and
  ``cartesian`` can be used to interprete the components of `shift_vector` as
  fractional or Cartesian coordinates, 

`additive` (optional)
  Specifies whether the atoms inside the given body should be added to or
  subtracted from the previous structure.

  In order to subtract a given body from the previous results, specify::

    additive: false


Sphere
^^^^^^
Specified as `[sphere: NAME]` with following options:

`radius`
  Radius of the sphere.

In order to cut a sphere with radius 10 Angstrom::

  [sphere: 1]
  radius = 5



Cylinder
^^^^^^^^

Specified as `[cylinder: NAME]`. It creates a body with circular base and top
areas which are orthogonal to the difference vector of their centers. The
circumference of the circles at the top and the bottom are connected by the
smallest lateral area possible. As the radius of the circles can be different,
you can also create truncated cones.

`point1`, `point2`
  Position vectors to the center of the first and second circular area.

`point1_coordsys`, `point2_coordsys` (optional)
  Coordinate system for the position vectors (``lattice`` or ``cartesian``).

`radius1`, `radius2`
  Radius of the circular areas.

Example for a truncated cone along the 111 Cartesian directon::

  [cylinder: 1]
  point1: 0 0 0
  point2: 10 10 10
  point2_coordsys: cartesian
  radius1: 5
  radius2: 9



Polyhedron
^^^^^^^^^^

Specified as `[polyhedron: NAME]` for a convex polyhedron defined by its
delimiting planes. Planes can be defined by their Miller indices or by their
normal vectors.

`planes_miller` 
  Miller indices of the delimiting planes (except those defined using normal
  vectors) followed by their distance from the origin.

`planes_normal` 
  Orthogonal vectors for each plane (except those defined using Miller indices)
  followed by their distance from the origin. The vectors do not need to be
  normalized.

`planes_normal_coordsys`
  Coordinate system for the normal vectors of the planes (``lattice`` or
  ``cartesian``). 

Example for an octahedron defined via the Miller indices of eight planes, each
of them being displaced by 5 Angstrom from the origin::

  [polyhedron: 1]
  planes_miller:
    1  1  1   5
   -1  1  1   5
    1 -1  1   5
   -1 -1  1   5
    1  1 -1   5
   -1  1 -1   5
    1 -1 -1   5
   -1 -1 -1   5


Periodic cylinder (1D)
^^^^^^^^^^^^^^^^^^^^^^

The section `[periodic_1D_cylinder: NAME]` specifies a supercell of an
infinitely long cylinder with a circular base area. The base area's center is
the origin and its normal vector is parallel to the axis specified in the
`[periodicity]` section.

`radius`
  The cylinders radius.

A cylindrical nanowire of the radius 5 Angstrom can be defined as::

  [periodic_1D_cylinder:1]
  radius: 5


Periodic convex prism (1D)
^^^^^^^^^^^^^^^^^^^^^^^^^^

Using `[periodic_1D_prism: NAME]` one specifies an infinitely long prism
with a convex polygon as base area. The prism is defined by its lateral
planes. A plane can be defined using it's Miller indices or it's normal
vector. The planes must be parallel to the periodicity axis specified in the
`[periodicity]` section.

`planes_miller`
  Miller indices of the delimiting planes (except those defined using normal
  vectors) followed by their distance from the origin. Depending on the settings
  in the `[geometry]` section, the Miller indices are interpreted with respect
  to the primitive lattice or the Bravais lattice.

`planes_normal`
  Vector orthogonal to each plane (except those defined using Miller indices)
  followed by its distance from the origin. 

`planes_normal_coordsys`
  Coordinate system for the normal vectors of the planes (``lattice`` or
  ``cartesian``).

Example for a 001 wire with quadratic cross section::

  [periodic_1D_prism:1]
  planes_miller:
     1  1  0  10.0
     1 -1  0  10.0
    -1  1  0  10.0
    -1 -1  0  10.0



Slab (2D)
^^^^^^^^^

The `[periodic_2D_plane]` section specifies a slab delimited by two parallel
planes and being periodic along the planes. The upper and lower limiting planes
are equidistant from the origin. The direction of the limiting planes are
automatically derived from the periodicity specified in the ``[periodicity]``
section.

`thickness`
  Thickness of the slab.

Slab with thickness of 20 Angstrom::

  [periodic_2D_plane:slab]
  thickness: 20



Supercell (3D)
^^^^^^^^^^^^^^

The `[periodic_3D_supercell]` section specifies a supercell built from the
unit cell of the original crystal. It does not take any further options,
everything is derived from the settings in the `[periodicity]` section::

  [periodic_3D_supercell:mycell]


