source /opt/openfoam7/etc/bashrc
. ../mesh_path

# running the solver
start=`date +%s`

echo 'make backup 0 directory'
cp -r 0 0.orig

# Calculate transport coefficient to constant/transportProperties
echo 'calculating transport coefficient'
python DT.py

# link to mesh from flowfield case


echo 'make symbolic link to polymesh '
ln -s $mesh_p ./constant

# map flowfield solution on 0 folder 
echo 'map latestTime solution to initialize flowfield '
mapFields ../ -sourceTime latestTime -consistent

# checkMesh
echo 'checkin Mesh...'
checkMesh > log.checkMesh 2>&1
echo 'decomposing domain...'
decomposePar > log.decomposePar 2>&1
echo 'scalarTransportFoam running...'
mpirun -np 4 scalarTransportFoam -parallel  > log.scalarTransportFoam
if [ $? -eq 0 ]; then
	echo 'reconstructing domain'
	reconstructPar > log.reconstructPar 2>&1
	rm -rf processor*
fi

end=`date +%s`
runtime=$((end-start))
echo 'run time is:' $runtime 'seconds' > run_time.txt 

# running postProcessing
echo 'postProcessing...'
postProcess -latestTime -func 'patchAverage(name=back, T)' > log.postProcess_T_outlet 2>&1
postProcess -latestTime -func volFieldValue > log.postProcess_T 2>&1
postProcess -latestTime -func "grad(T)"

# Calculate transport coefficient to constant/transportProperties
python collProp.py
