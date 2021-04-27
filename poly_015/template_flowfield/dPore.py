import os
import numpy as np
import pickle as pk 
from pathlib import Path 


# Funtions to load and dump pickle files

def load_pkl(FILENAME):
    with open(FILENAME,'rb') as f:
        val = pk.load(f)
    return val

def dump_pkl(FILENAME,k):
	with open(FILENAME,'wb') as f:
		pk.dump(k,f)

# Main

cwd = Path(os.getcwd())
f_path = 'foamPore_D.pkl'
bgMesh_p = 'bgMesh'

D = load_pkl( cwd / f_path)
line1 = 'DS {:.1f};\n'.format(D['d_sphr'])
line2 = 'DC {:.5f};\n'.format(D['d_cell'])

with open(cwd / bgMesh_p, 'a') as f:
	f.write(line1)
	f.write(line2)
