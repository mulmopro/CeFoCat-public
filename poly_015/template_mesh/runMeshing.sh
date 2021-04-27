#!/bin/bash

#SBATCH --mail-user=enrico.agostini@polito.it
#SBATCH --mail-type=ALL		# NONE, BEGIN, END, FAIL, REQUEUE, ALL, TIME_LIMIT, TIME_LIMIT_90
#SBATCH -e foamErr.err                  # standard error file
#SBATCH -o foamLog.log                  # standard output file
#SBATCH --account=eagostini              # account name
#SBATCH --mem=15G                        # Memory Size (maximum of 128G per node)
#SBATCH -t 10:00:00                     # Wall Clock Limit

######################################

#SBATCH --job-name=meshing           # Name of job
#SBATCH -p global                       # Queue
#SBATCH -N1 -n4                         # <n> cores on <N> nodes

## Please note that Casper has 17 nodes each with 36 cores (AMD Bulldozer)
##              and Hactar has 24 nodes each with 24 cores (Intel XEON v3)

######################################
/bin/echo "Loading OpenFOAM ..."
module load intel/python/3
module load openfoam/7
source /share/apps/openfoam/7/OpenFOAM-7/etc/bashrc
# source /opt/openfoam7/etc/bashrc
source /opt/openfoam7/etc/bashrc
l='ls -CF'
cp bgMesh bgMesh.orig
python dPore.py

##### blockMesh 
blockMesh | tee log.blockMesh 2>&1

echo 'get .stl file name'
echo "stl \"$($l ./constant/triSurface/)\";" > stl_name

##### snappyhexMesh
echo 'snappyHexMesh running...'
snappyHexMesh -overwrite | tee log.snappyHexMesh 2>&1

echo 'checkin Mesh...'
checkMesh | tee log.checkMeshMacro 2>&1

echo 'check for multiple region'
echo 'remove non-connected independent regions'

python splitMesh.py
