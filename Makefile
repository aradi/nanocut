INT = python
MAIN = main.py

nothing:


doc: doc/srcexamples/basic.xyz doc/srcexamples/periodicity.xyz doc/srcexamples/cylinder.xyz doc/srcexamples/geometry.xyz doc/srcexamples/convex_polyhedron.xyz doc/srcexamples/periodic_1D_convex_prism.xyz

doc/srcexamples/%.xyz: doc/srcexamples/%.ini
	$(INT) $(MAIN) -w $@ $<

doc-clean:
	rm ./doc/*~ ./doc/*.backup ./doc/*.toc ./doc/*.aux ./doc/*.log ./doc/srcexamples/*~ ./doc/srcexamples/*.xyz ./doc/*.pdf

test-clean:
	rm ./testoutput/*

test-landscape: 
	$(INT) $(MAIN) ./testinis/house-base.ini -w ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/house-roof.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-body.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-nose.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-hat.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/steps.ini -a ./testoutput/landscape.xyz

test-circular-wire:
	$(INT) $(MAIN) ./testinis/circular-wire.ini -w ./testoutput/circular-wire.xyz

test-prism-wire:
	$(INT) $(MAIN) ./testinis/prism-wire.ini -w ./testoutput/prism-wire.xyz

test-plane:
	$(INT) $(MAIN) ./testinis/plane.ini -w ./testoutput/plane.xyz

test-steps:
	$(INT) $(MAIN) ./testinis/steps.ini -w ./testoutput/steps.xyz

test-house:
	$(INT) $(MAIN) ./testinis/house-base.ini -w ./testoutput/house.xyz
	$(INT) $(MAIN) ./testinis/house-roof.ini -a ./testoutput/house.xyz

test-snowman:
	$(INT) $(MAIN) ./testinis/snowman-body.ini -w ./testoutput/snowman.xyz
	$(INT) $(MAIN) ./testinis/snowman-nose.ini -a ./testoutput/snowman.xyz
	$(INT) $(MAIN) ./testinis/snowman-hat.ini -a ./testoutput/snowman.xyz
