INT = python -OO 
MAIN = main.py

nothing:

.PHONY: doc

xyz: doc/srcexamples/basic.xyz doc/srcexamples/convex_polyhedron.xyz doc/srcexamples/cylinder.xyz doc/srcexamples/geometry.xyz doc/srcexamples/order.xyz doc/srcexamples/periodic_1D_convex_prism.xyz doc/srcexamples/periodic_1D_cylinder.xyz doc/srcexamples/periodic_2D_plane.xyz doc/srcexamples/periodicity.xyz doc/srcexamples/sphere.xyz

png: doc/srcexamples/basic.png doc/srcexamples/convex_polyhedron.png doc/srcexamples/cylinder.png doc/srcexamples/geometry.png doc/srcexamples/order.png doc/srcexamples/periodic_1D_convex_prism.png doc/srcexamples/periodic_1D_cylinder.png doc/srcexamples/periodic_2D_plane.png doc/srcexamples/periodicity.png doc/srcexamples/sphere.png

doc: xyz png
	cd doc && pdflatex -interaction=nonstopmode 'main.tex' > /dev/null && pdflatex -interaction=nonstopmode 'main.tex' > /dev/null && pdflatex -interaction=nonstopmode 'main.tex' > /dev/null
	cp ./doc/main.pdf ./manual.pdf

doc/srcexamples/%.xyz: doc/srcexamples/%.ini
	$(INT) $(MAIN) -w $@ $<

doc/srcexamples/%.png: doc/srcexamples/%.xyz
	rm -f doc/pymolscript.pml
	cat $<.view doc/pymolscript.base > ./doc/pymolscript.pml
	pymol $< doc/pymolscript.pml -W 1024 -H 768 -g $@ -c -q
	rm -f doc/pymolscript.pml

doc-clean:
	rm -f ./doc/*~ ./doc/*.backup ./doc/*.toc ./doc/*.aux ./doc/*.log ./doc/srcexamples/*~ ./doc/srcexamples/*.xyz ./doc/srcexamples/*.png ./doc/*.pdf

test-clean:
	rm -f ./testoutput/*

src-clean:
	rm -f *~ *.pyo *.pyc

clean:
	make doc-clean
	make src-clean
	make test-clean

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
