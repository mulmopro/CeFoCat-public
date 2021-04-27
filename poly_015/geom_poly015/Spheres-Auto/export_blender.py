import bpy
import pandas as pd
import pickle
import numpy as np
import os

cwd = os.getcwd() + '/'

# Select all Icosphere objects

print('selecting icosphere...')
for o in bpy.data.objects:
    # Check for given object names
    if 'Icosphere' in o.name:
        o.select_set(True)

# Bake position to keyframe

print('Baking position...')
bpy.ops.rigidbody.bake_to_keyframes(frame_start=399, frame_end=400)

# Save names, locations, rotations and dimensions of objects


allObj = bpy.data.collections[0].objects

name = []
loc = []
rot = []
dim = []
scal  = []

print('retrieving icosphere data')
for i in range( 0, len(allObj)):
    name.append(allObj[i].name)
    loc.append(list(allObj[i].location[:]))
    rot.append(list(allObj[i].rotation_euler[:]))
    dim.append(list(allObj[i].dimensions[:]))
    scal.append(list(allObj[i].scale[:]))

print('saving names')
with open(cwd + '../names.pickle','wb') as f0_out:
    pickle.dump(np.array(name) , f0_out)

print('saving centroids')    
with open(cwd + '../centroids.pickle','wb') as f_out:
    pickle.dump(np.array(loc) , f_out)

print('saving dimensions')
with open(cwd + '../radii.pickle', 'wb') as f2_out:
    pickle.dump(np.array(dim), f2_out)
    
    
########## Per riaprire il file .pickle in un terminale/IDE/journal

# import pickle
# with open('./pack.pickle','rb') as file:
#     pickled=pickle.load(file)