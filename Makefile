INT = python
MAIN = main.py

nothing:


doc: doc/srcexamples/basic.xyz doc/srcexamples/periodicity.xyz doc/srcexamples/sphere.xyz doc/srcexamples/cylinder.xyz

doc/srcexamples/%.xyz: doc/srcexamples/%.ini
	$(INT) $(MAIN) -w $@ $<


test-clean:
	rm ./testoutput/*

test-landscape: ./testinis/house-base.ini ./testinis/house-roof.ini ./testinis/snowman-nose.ini ./testinis/snowman-body.ini
	$(INT) $(MAIN) ./testinis/house-base.ini -w ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/house-roof.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-body.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-nose.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-hat.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/steps.ini -a ./testoutput/landscape.xyz


test-circular-wire: ./testinis/circular-wire.ini
	$(INT) $(MAIN) ./testinis/circular-wire.ini -w ./testoutput/circular-wire.xyz

test-prism-wire:  ./testinis/prism-wire.ini
	$(INT) $(MAIN) ./testinis/prism-wire.ini -w ./testoutput/prism-wire.xyz

test-plane: ./testinis/plane.ini
	$(INT) $(MAIN) ./testinis/plane.ini -w ./testoutput/plane.xyz

test-steps: ./testinis/steps.ini
	$(INT) $(MAIN) ./testinis/steps.ini -w ./testoutput/steps.xyz



test-house: ./testoutput/house-roof.xyz ./testinis/house-base.ini ./testinis/house-roof.ini
	cp ./testoutput/house-roof.xyz ./testoutput/house.xyz

./testoutput/house-base.xyz: ./testinis/house-base.ini
	$(INT) $(MAIN) ./testinis/house-base.ini -w ./testoutput/house-base.xyz

./testoutput/house-roof.xyz: ./testinis/house-roof.ini ./testoutput/house-base.xyz
	cp ./testoutput/house-base.xyz ./testoutput/house-roof.xyz
	$(INT) $(MAIN) ./testinis/house-roof.ini -a ./testoutput/house-roof.xyz







test-snowman: ./testoutput/snowman-hat.xyz
	cp ./testoutput/snowman-hat.xyz ./testoutput/snowman.xyz
	echo "Built snowman"
        
./testoutput/snowman-hat.xyz: ./testinis/snowman-hat.ini ./testoutput/snowman-nose.xyz 
	cp ./testoutput/snowman-nose.xyz ./testoutput/snowman-hat.xyz
	$(INT) $(MAIN) ./testinis/snowman-hat.ini -a ./testoutput/snowman-hat.xyz

./testoutput/snowman-nose.xyz: ./testinis/snowman-nose.ini ./testoutput/snowman-body.xyz
	cp ./testoutput/snowman-body.xyz ./testoutput/snowman-nose.xyz
	$(INT) $(MAIN) ./testinis/snowman-nose.ini -a ./testoutput/snowman-nose.xyz

./testoutput/snowman-body.xyz: ./testinis/snowman-body.ini
	$(INT) $(MAIN) ./testinis/snowman-body.ini -w ./testoutput/snowman-body.xyz

