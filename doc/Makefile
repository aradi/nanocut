MAIN = nanocut

.PHONY: doc

doc: xyz png
	pdflatex -interaction=nonstopmode 'main.tex' > /dev/null && pdflatex -interaction=nonstopmode 'main.tex' > /dev/null && pdflatex -interaction=nonstopmode 'main.tex' > /dev/null
	mv ./main.pdf ./manual.pdf

xyz: srcexamples/basic.xyz srcexamples/convex_polyhedron.xyz srcexamples/cylinder.xyz srcexamples/geometry.xyz srcexamples/order.xyz srcexamples/periodic_1D_convex_prism.xyz srcexamples/periodic_1D_cylinder.xyz srcexamples/periodic_2D_plane.xyz srcexamples/periodicity.xyz srcexamples/sphere.xyz

png: srcexamples/basic.png srcexamples/convex_polyhedron.png srcexamples/cylinder.png srcexamples/geometry.png srcexamples/order.png srcexamples/periodic_1D_convex_prism.png srcexamples/periodic_1D_cylinder.png srcexamples/periodic_2D_plane.png srcexamples/periodicity.png srcexamples/sphere.png


srcexamples/%.xyz: srcexamples/%.ini
	$(MAIN) -w $@ $<

srcexamples/%.png: srcexamples/%.xyz
	rm -f pymolscript.pml
	cat $<.view pymolscript.base > ./pymolscript.pml
	pymol $< pymolscript.pml -W 1024 -H 768 -g $@ -c -q
	rm -f pymolscript.pml

doc-clean:
	rm -f ./*~ ./*.backup ./*.toc ./*.aux ./*.log ./srcexamples/*~ ./srcexamples/*.xyz ./srcexamples/*.png ./*.pdf

clean:
	make doc-clean
