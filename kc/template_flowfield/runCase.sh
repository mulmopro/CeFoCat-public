source /opt/openfoam7/etc/bashrc
l='ls -CF'
 
start=`date +%s`

cp -r bgMesh bgMesh.orig

# link to mesh
echo 'make symbolic link to polymesh '
python meshLink.py
. ./mesh_path
ln -s $mesh_p ./constant

# ##### checkMesh Macro
echo 'checkin Mesh...'
checkMesh | tee log.checkMeshMacro 2>&1

# get scaling factor
echo 'calculating scaling factor...'
python fScale.py 
. ./scale_setup

# ##### transformPoints and topoSet
echo 'downscaling the computational domain...'
transformPoints -scale "$fx" | tee log.transformPoints 2>&1

echo 'checkin Mesh...'
checkMesh | tee log.checkMesh 2>&1

# running the solver
echo 'decomposing domain...'
decomposePar | tee log.decomposePar 2>&1
echo 'simpleFoam running...'
mpirun -np 4 simpleFoam -parallel  | tee log.simpleFoam 2>&1
if [ $? -eq 0 ]; then
	echo 'reconstructing domain'
	reconstructPar | tee log.reconstructPar 2>&1
	rm -rf processor*
fi


# running postProcessing
echo 'postProcessing...'
postProcess -func time -latestTime > latestTime
postProcess -func writeCellVolumes -latestTime 
postProcess -latestTime -func volMeanVel
postProcess -latestTime -func 'patchAverage(name=walls,p)'
simpleFoam -postProcess -dict system/outletVel -latestTime

# python data_postProcessing.py
end=`date +%s`
runtime=$((end-start))
echo 'total run time is:' $runtime 'seconds' | tee run_time.txt 

python permeability.py