INT = python -OO
MAIN = ../main.py

all:  surf circwire 



circwire: w111-2.0.wire_florian.xyz w011-2.0.wire_florian.xyz w001-2.0.wire_florian.xyz

surf: surf2-162-periodic_florian_reapeat.xyz

%.xyz: %.ini
	$(INT) $(MAIN) -w $@ $< 

surf2-162-periodic_florian_reapeat.xyz: surf2-162-periodic_florian.xyz
	./repeatxyz -l lattice_vectors surf2-162-periodic_florian.xyz  6 6 1 > surf2-162-periodic_florian_reapeat.xyz
