#!/bin/bash
shopt -s expand_aliases
source /home/eagostini/.bash_aliases
START=$(date +%s)
#START

#Setup
p 1-Setup.py
#Actual Blender Run
blender27 -b test.blend -P 2-Placement-Automatic.py
#END
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds" > runtime.txt

