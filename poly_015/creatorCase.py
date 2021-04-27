import os
import shutil
import numpy as np
import pandas as pd
import pickle as pk
from pathlib import Path

# file write function

def pickle_k(FILENAME,k):
	with open(FILENAME,'wb') as f:
		pk.dump(k,f)


cwd = Path(os.getcwd())
perm_p = 'perm.csv'
k_out = 'k.pkl'

perm = pd.read_csv(cwd / perm_p)

ppi_l = [10,20,30,45]
por_l = [77,79,85,89,95]
pe_l = np.logspace(np.log10(5),np.log10(500),5).round().astype(int)
g_type = 'poly02'
g_path = 'geom_' + g_type

geom_dir = cwd / g_path
stl_dir = geom_dir / 'stl_dir'
foamPost = 'foamPore_D.pkl'
job_name = '#SBATCH --job-name='
# create mesh cases
for por in por_l:
	mesh_case = './mesh_%d' %(por)    # name of meshing case based on porosity
	shutil.copytree(cwd / 'template_mesh', mesh_case)    # copy meshing case template in cwd
	stl_name = [s for s in os.listdir(stl_dir) if '%d' %por in s][0] # get .stl fil name based on porosity
	shutil.copy(stl_dir / stl_name, cwd / mesh_case / 'constant' / 'triSurface') # copy .stl file in case/constant/triSurface
	shutil.copy(geom_dir / foamPost, cwd / mesh_case )    # copy foam postProcess informations file to mesh_case

for ppi in ppi_l:
    for por in por_l:
        case = '%s_%d_%d' %(g_type,ppi,por)    # case is named <type>_<ppi>_<porosity>
        nameK = 'kc_%d_%d' %(ppi,por)

        print('copy case:',case)
        shutil.copytree(cwd / 'template_flowfield', case)    # copy template case with new name
        shutil.copy(geom_dir / foamPost, cwd / case )    # copy foam postProcess informations file to case

        os.chdir(cwd / case )    # change dir to case
        print('cwd:',os.getcwd())

        k = perm.loc[perm['case'] == nameK, 'k'].values[0]
        pickle_k(Path(os.getcwd()) / k_out, k)

        with open('runCase.sh','r') as run_f:    # Open runCase.sh to add job name
            lines = run_f.readlines()
            lines[2] = job_name + case
        
        with open('runCase.sh','w') as run_f:    # Write runCase.sh
            run_f.writelines(lines)

        for pe in pe_l:
        	pe_case = 'Pe_%d' %(pe)
        	shutil.copytree(cwd / 'template_scalar', pe_case)    # copy scalarTransport template to case directory with new name

        	pe_path = cwd / case / pe_case
        	with open(pe_path / 'runCase.sh','r') as run_f:
        		lines = run_f.readlines()
        		lines[2] = job_name + case + '_%d' %(pe)

        	with open(pe_path / 'runCase.sh','w') as run_f:
        		run_f.writelines(lines)

        os.chdir(cwd)

