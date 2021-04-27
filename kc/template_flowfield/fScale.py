import numpy as np
import pandas as pd
import os
import re
import pickle as pk
from pathlib import Path

# Function get blockMesh box dimensions

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
    return vv

# Main

cwd = Path(os.getcwd())
checkMesh_p = cwd / 'log.checkMeshMacro'
dirname = os.path.basename(cwd) 

ppi = float(dirname.split('_')[1])

l = get_box(checkMesh_p)


d_pore = 0.0254/ppi

fScale = d_pore / l

with open('./scale_setup','w+') as f:
	f.write('#!/bin/sh')
	f.write('\n')
	f.write('fx=\"({:.2e} '.format(fScale[0]) + '{:.2e} '.format(fScale[1]) + '{:.2e})\"'.format(fScale[2]))
	f.write('\n')