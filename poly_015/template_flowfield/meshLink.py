import os
from pathlib import Path

cwd = Path(os.getcwd())
por = os.path.basename(cwd).split('_')[-1]
mesh_dir = 'mesh_' + por 
mesh_dir = [s for s in os.listdir(cwd.parent) if mesh_dir in s][0] # check existence 

polyMesh_p = cwd.parent / mesh_dir / 'constant' / 'polyMesh'
check_p = cwd.parent / mesh_dir / 'log.checkMeshMacro'
path_mesh = 'mesh_p=\"{}\"'.format(str(polyMesh_p))
path_check = 'check_p=\"{}\"'.format(str(check_p))

with open('./mesh_path','w+') as f:
	f.write('#!/bin/sh')
	f.write('\n')
	f.write(path_mesh)
	f.write('\n')
	f.write(path_check)
	f.write('\n')
