import os
from pathlib import Path
import shutil as sh

def get_time(FILENAME):
    TARGET = "Time = "
    with open(FILENAME, 'r') as f:
        for line in f:
            if TARGET in line.strip():
                _, t = line.split(TARGET)
                t, _ = t.split('\n')
                break
    return t

cwd = Path(os.getcwd())
flow_dir = cwd.parent
dir_0 = cwd / '0'

# get absolut path for mesh
polyM = str(cwd.parent / 'constant/polyMesh') 
out_mesh = '#!/bin/sh\nmesh_path=\"' + polyM + '\"\n'
with open('mesh_sclr','w') as f:
    f.write(out_mesh)

# Write Peclet file
case = os.path.basename(cwd)

Pe_n = float(case.split('_')[-1])

str_out = 'PE {};'.format(Pe_n)

with open('PECLET','w') as out_f:
	out_f.write(str_out)

# copy flow field in 0 directory
latestTime = get_time(flow_dir / 'latestTime')
latestDir = cwd.parent / latestTime

for item in os.listdir(latestDir):
	if '.gz' in item:
		sh.copy(latestDir / item, dir_0 )
