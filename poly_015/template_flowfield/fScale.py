import numpy as np
import os
import pickle as pk
from pathlib import Path


def load_pkl(FILENAME):
    with open(FILENAME,'rb') as f:
        val = pk.load(f)
    return val

# Main

cwd = Path(os.getcwd())
checkMesh_p = cwd / 'log.checkMeshMacro'
foamPost = cwd / 'foamPore_D.pkl'
dirname = os.path.basename(cwd) 
D = load_pkl(foamPost)
ppi = float(dirname.split('_')[1])

d_pore = 0.0254/ppi

fScale = d_pore / D['d_cell']

with open('./scale_setup','w+') as f:
	f.write('#!/bin/sh')
	f.write('\n')
	f.write('fx=\"({:.2e} '.format(fScale) + '{:.2e} '.format(fScale) + '{:.2e})\"'.format(fScale))
	f.write('\n')