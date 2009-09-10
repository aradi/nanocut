INT = python
MAIN = main.py

nothing:

doc:
	echo "Make doc (TODO)"

test-clean:
	rm ./testoutput/*

test-landscape: ./testinis/house-base.ini ./testinis/house-roof.ini ./testinis/snowman-nose.ini ./testinis/snowman-body.ini
	$(INT) $(MAIN) ./testinis/house-base.ini -w ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/house-roof.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-body.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/snowman-nose.ini -a ./testoutput/landscape.xyz
	$(INT) $(MAIN) ./testinis/steps.ini -a ./testoutput/landscape.xyz



test-steps: ./testinis/steps.ini
	$(INT) $(MAIN) ./testinis/steps.ini -w ./testoutput/steps.xyz



test-house: ./testoutput/house-roof.xyz
	echo "Built house"

./testoutput/house-base.xyz: ./testinis/house-base.ini
	$(INT) $(MAIN) ./testinis/house-base.ini -w ./testoutput/house-base.xyz

./testoutput/house-roof.xyz: ./testinis/house-roof.ini ./testoutput/house-base.xyz
	cp ./testoutput/house-base.xyz ./testoutput/house-roof.xyz
	$(INT) $(MAIN) ./testinis/house-roof.ini -a ./testoutput/house-roof.xyz







test-snowman: ./testoutput/snowman-nose.xyz
	echo "Built snowman"

./testoutput/snowman-nose.xyz: ./testinis/snowman-nose.ini ./testoutput/snowman-body.xyz
	cp ./testoutput/snowman-body.xyz ./testoutput/snowman-nose.xyz
	$(INT) $(MAIN) ./testinis/snowman-nose.ini -a ./testoutput/snowman-nose.xyz

./testoutput/snowman-body.xyz: ./testinis/snowman-body.ini
	$(INT) $(MAIN) ./testinis/snowman-body.ini -w ./testoutput/snowman-body.xyz

