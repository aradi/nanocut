INT = python
MAIN = main.py

nothing:

doc:
	echo "Make doc (TODO)"

test-clean:
	rm ./testoutput/*

test-landscape: test-snowman test-house



test-snowman: ./testoutput/snowman-nose.xyz
	echo "Built Snowman"

./testoutput/snowman-nose.xyz: ./testinis/snowman-nose.ini ./testoutput/snowman-body.xyz
	cp ./testoutput/snowman-body.xyz ./testoutput/snowman-nose.xyz
	$(INT) $(MAIN) ./testinis/snowman-nose.ini -a ./testoutput/snowman-nose.xyz

./testoutput/snowman-hat.xyz: ./testinis/snowman-hat.ini

./testoutput/snowman-coal.xyz: ./testinis/snowman-coal.ini ./testoutput/snowman-body.xyz

./testoutput/snowman-body.xyz: ./testinis/snowman-body.ini
	$(INT) $(MAIN) ./testinis/snowman-body.ini -w ./testoutput/snowman-body.xyz

