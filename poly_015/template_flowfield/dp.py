import numpy as np
import os
import re
import pickle as pk
from pathlib import Path


# function to extract the box dimensions


def get_box(FILENAME):
    STARTER = "Checking geometry..."
    TARGET = "    Overall domain bounding box "

    with open(FILENAME, 'r') as f:
        v = None
        start_seen = False
        for line in f:
            if line.strip() == STARTER:
                start_seen = True
                continue

            if TARGET in line and start_seen:
                _, v = line.split(TARGET)
                v, _ = v.split('\n')
                break
    v = v.replace(')', '$').replace('(', '$').split('$ $')
    v = [item.split(' ') for item in [item.replace('$', '') for item in v]]
    v = np.array([[float(elem) for elem in item] for item in v])
    vv = v[1] - v[0]
    return vv[0], vv[1], vv[2]

# function to extract slice surface area and velocity


def get_surf(FILENAME):
    TARGET = "Area   :    "
    with open(FILENAME, 'r') as f:
        A = None
        for line in f:
            if TARGET in line.strip():
                _, A = line.split(TARGET)
                A, _ = A.split('\n')
                break
    return float(A)

# Get pickle file variable


def get_pickle(FILENAME):
	with open(FILENAME,'rb') as f:
		val = pk.load(f)
	return val

# Main

cwd = Path(os.getcwd())
dirname = os.path.basename(cwd)
checkMesh_p = 'log.checkMesh'
surf_p = 'postProcessing/patchIntegrate(name=back,U)/0/surfaceFieldValue.dat'
k_path = 'k.pkl'
dp_out = 'dp.pkl'

outfile = 'bgMesh'

ppi = float(dirname.split('_')[1])

lx,ly,lz = get_box(cwd / checkMesh_p)
out_s = get_surf(cwd / surf_p)

nu = 1e-06
eps_s = out_s / (ly*lz)
d_pore =  0.0254/ppi  # in kelvin cell d_pore and lx coincide

Re = 0.00105
k = get_pickle(cwd / k_path)

dp = eps_s * lx/d_pore * nu**2 /k * Re

out_s = 'dp {:.5e};\n'.format(dp)
with open(cwd / outfile,'a') as f:
	f.write(out_s)

with open(cwd / dp_out,'wb') as f:
	pk.dump(dp,f)
