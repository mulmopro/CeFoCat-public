#!/bin/bash



#SBATCH --nodes=1           		# number of nodes
#SBATCH --ntasks-per-node=1 		# number of tasks per node
#SBATCH --cpus-per-task=4			# number of cpus per node
#SBATCH --time=10:00:00              # time limits: here 1 hour
#SBATCH --mem=12GB             		# total memory per node requested in GB (optional)
#SBATCH --error=myJob.err            # standard error file
#SBATCH --output=myJob.out           # standard output file
#SBATCH --partition=gll_usr_prod	 # partition name
#SBATCH --account=IscrC_NeTraPoM
#SBATCH --mail-type=ALL
#SBATCH --mail-user=aanri.ago@gmail.com


/bin/echo "Loading OpenFOAM ..."
module load profile/eng 
module load intel/pe-xe-2018--binary
module load intelmpi/2018--binary

module load boost/1.61.0--intelmpi--2018--binary
module load fftw/3.3.8--intelmpi--2018--binary
module load openfoam/7.0
module load python/3.6.4

# source /share/apps/openfoam/7/OpenFOAM-7/etc/bashrc
# source /opt/openfoam7/etc/bashrc
# source /opt/openfoam7/etc/bashrc
l='ls -CF'


# ##### blockMesh 
start=`date +%s`

# cp -r bgMesh bgMesh.orig

# link to mesh
echo 'make symbolic link to polymesh '
python meshLink.py
. ./mesh_path
cp -r $mesh_p ./constant
cp $check_p .

##### checkMesh

# get scaling factor
echo 'calculating scaling factor...'
python fScale.py 
. ./scale_setup

##### transformPoints and topoSet
echo 'downscaling the computational domain...'
transformPoints -scale "$fx" | tee log.transformPoints 2>&1

echo 'checkin Mesh...'
checkMesh | tee log.checkMesh 2>&1

#set pressure gradient
echo 'setting pressure gradient'
postProcess -func 'patchIntegrate(name=back,U)'
python dp.py

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
