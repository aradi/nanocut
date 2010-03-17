INT = python -OO
MAIN = ../main.py

all: surf2-162-periodic_florian.xyz r6.68_new.xyz r5.39_new.xyz r-04.85_new.xyz r5.58_new.xyz

%.xyz: %.ini
	$(INT) $(MAIN) -w $@ $< 
