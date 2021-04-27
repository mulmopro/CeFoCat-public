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

ppi_l = [10,20,30,45]		# PPI values
por_l = [77,79,85,89,95]	# Porosity values (same as in Blender directory)
pe_l = np.logspace(np.log10(5),np.log10(500),5).round().astype(int)
g_type = 'kc'

geom_dir = cwd / 'geom_kc/stl_dir'

# create mesh cases
for por in por_l:
	mesh_case = './mesh_%d' %(por)
	shutil.copytree(cwd / 'template_mesh', mesh_case)
	stl_name = [s for s in os.listdir(geom_dir) if '%d' %por in s][0]
	shutil.copy(geom_dir / stl_name, cwd / mesh_case / 'constant' / 'triSurface')

# create flowfield and scalar cases
for ppi in ppi_l:
	for por in por_l:
		case = './%s_%d_%d' %(g_type,ppi,por)
		shutil.copytree(cwd / 'template_flowfield', case)
		os.chdir(cwd / case )
		for pe in pe_l:
			shutil.copytree(cwd / 'template_scalar','./Pe_%d' %(pe))
		os.chdir(cwd)

