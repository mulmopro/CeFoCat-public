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

# module load intel/python/3
# module load openfoam/7
# source /share/apps/openfoam/7/OpenFOAM-7/etc/bashrc
# source /opt/openfoam7/etc/bashrc

# running the solver
start=`date +%s`

echo 'make backup 0 directory'
cp -r 0 0.orig

# Calculate transport coefficient to constant/transportProperties
echo 'calculating transport coefficient'
python DT.py

# link to mesh from flowfield case
echo 'make symbolic link to polymesh '
. ./mesh_sclr
ln -s $mesh_path ./constant

# checkMesh
# echo 'checkin Mesh...'
# checkMesh > log.checkMesh 2>&1
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
