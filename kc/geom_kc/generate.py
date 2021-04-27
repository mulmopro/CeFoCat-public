import pickle
import pandas as pd
import numpy as np
import bpy
import time
import sys
import os
import math as m
import argparse
from pathlib import Path 

def object_duplication(n_dup):
	# create array of object equal to number of struts
	print('array modifier')
	bpy.ops.object.modifier_add(type='ARRAY')
	bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 1.1
	bpy.context.object.modifiers["Array"].count = n_dup
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")

	# Separate array into individual objects 
	print('separate individuals')
	bpy.ops.object.editmode_toggle()
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.separate(type='LOOSE')
	bpy.ops.object.editmode_toggle()

	# Change origin to geometry for all abjects
	print('origin to geometry')
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')


# import geometry module

class Point(object):

    def __init__(self,pos_arr):
        self.x = pos_arr[0]
        self.y = pos_arr[1]
        self.z = pos_arr[2]

    def __eq__(self, other):
        if isinstance(other, Point):
            equal_x = m.isclose(other.x, self.x, rel_tol=5e-3, abs_tol=1e-5)
            equal_y = m.isclose(other.y, self.y, rel_tol=5e-3, abs_tol=1e-5)
            equal_z = m.isclose(other.z, self.z, rel_tol=5e-3, abs_tol=1e-5)
            if equal_x and equal_y and equal_z:
                return True

        return False

    def __hash__(self):

        return hash((self.x,self.y, self.z))

    def vec(self):

        pVect = np.array([self.x, self.y, self.z])
        return pVect


"""
Define the "Edge" class:
it is initialized by the Point(class) in input
it caculate all the information needed to be created: lenght, phi, theta,
center and store the information regarding his actual creation
"""


class Edge(object):

    def __init__(self, start, end):

        self.start = start
        self.end = end
        self.dP = end.vec() - start.vec()

    def __eq__(self, other):
        if  isinstance(other, Edge):
            if other.start == self.start and other.end == self.end:
                return True
            elif other.start == self.end and other.end == self.start:
                return True
        return False

    def lenght(self):

        dist = abs(m.sqrt(self.dP[0]**2 + self.dP[1]**2 + self.dP[2]**2))
        return dist

    def phi(self):

        phiAngle = m.atan2(self.dP[1], self.dP[0])
        return phiAngle

    def theta(self):

        thetaAngle = m.acos(self.dP[2]/self.lenght())
        return thetaAngle


# Get arguments from command line
# blender -b -P generate.py -- -p <porosity> 


arguments = sys.argv[sys.argv.index("--")+1:]
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--porosity', dest='por', type=float)
        
args = parser.parse_args(arguments)

start_time = time.time()
cwd = Path(os.getcwd())
sys.path.append(cwd)


# Import edges and points data


with open(cwd / 'edgesData.pickle','rb') as f:
	edges = pickle.load(f)

n_ed = len(edges)

print('total number of edges is =',n_ed)

with open(cwd / 'pointData.pickle','rb') as f:
    points = pickle.load(f)

n_p = len(points)


# Main body

# import object
print('create first cylindr')
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))

# create array modifier with n_e elements

object_duplication(n_ed)


# struts placement
d_cyl = -2.01 * (args.por/100)**2 + 1.5 * (args.por/100) + 0.646# from porosity/diameter fitting "d_cyl = -2.01*por^2 +1.5*por +0.646"

obj_s =  bpy.data.objects
print('move cylinders')
for i in range( 0, n_ed):
    print('creating strut n',i,'of',n_ed)
    obj_s[i].location = edges[i].start.vec() + edges[i].dP/2
    obj_s[i].rotation_euler = (0, edges[i].theta(), edges[i].phi())
    obj_s[i].dimensions = (d_cyl,d_cyl,edges[i].lenght())


# create first vertex
print('create first vertex')

d_n = d_cyl*1.5#3/(6)**0.5 

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions= 4, radius= d_n/2, location=(0,0,0))

# create array modifier with n_p elements

object_duplication(n_p)

for i in range( n_ed, n_ed + n_p ):
    print("moving vertex number:",i-n_ed)
    obj_s[i].location = points[i-n_ed]


name_out = 'kc_%d' %(args.por)
blend_name = str(cwd / 'blend_dir' / (name_out + '.blend'))
stl_name = str(cwd / 'stl_dir' / (name_out + '.stl'))

print('Saving .blend file')
bpy.ops.wm.save_as_mainfile(filepath= blend_name)
print('Exporting to .stl')

bpy.ops.export_mesh.stl(filepath= stl_name, check_existing=True, filter_glob='*.stl', use_selection=True, global_scale=1.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OFF', axis_forward='X', axis_up='Z')
end_time = time.time()

print('time=',end_time -start_time)
