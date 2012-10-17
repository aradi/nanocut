# Max. rounding errors when investigating periodic boundary conditions.
# (planes in periodic directions are pushed outwards by that amount to make
# sure all necessary atoms are inside the body)
PERIODIC_TOLERANCE = 1e-10

# Max rounding error in relative coordinates. Current value should safely cover
# the inaccuracies introduced by PERIODIC_TOLERANCE for all physically
# meaningful structures 
RELATIVE_PERIODIC_TOLERANCE = 1e-4

# Tolerance for considering two atoms being on the same position
DISTANCE_TOLERANCE = 1e-8

# General numerical tolerance (for comparing real numbers)
EPSILON = 1e-12
