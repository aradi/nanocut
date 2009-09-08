INT = python
MAIN = main.py

nothing:

doc:
	echo "Make doc (TODO)"

test-all: test-snowman

test-snowman: ./testoutput/snowman-body.xyz
	echo "Snowman successfully build."


./testoutput/snowman-body.xyz:
	$(INT) $(MAIN) ./testinis/snowman-body.ini ./testoutput/snowman-body.xyz