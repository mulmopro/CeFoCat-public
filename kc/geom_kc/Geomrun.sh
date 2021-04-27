blender='/usr/local/blender-2.83.5-linux64/blender'

python kc_foam.py

for i in {77,79,85,89,95}; # Set the porosities
do 
    $blender -b -P generate.py -- -p $i; 
done
