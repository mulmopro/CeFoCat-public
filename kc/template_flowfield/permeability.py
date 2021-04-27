import numpy as np
import pandas as pd
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

# function to get fluid volume


def get_vol(FILENAME):
    STARTER = "Checking geometry..."
    TARGET = "Total volume = "

    with open(FILENAME, 'r') as f:
        v = None
        start_seen = False
        for line in f:
            if line.strip() == STARTER:
                start_seen = True
                continue

            if TARGET in line and start_seen:
                _, v = line.split(TARGET)
                v, _ = v.split('.  Cell volumes OK.\n')
                break

    return float(v)

# Get total number of grid cells


def get_totCells(FILENAME):
    STARTER = "Mesh stats"
    TARGET = "    cells:            "

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
    return float(v)

# Get background mesh cells


def get_bgMesh(FILENAME):
    with open(FILENAME, 'r') as f:
        line = f.readlines()[0]
        bgM = float(re.split('C |;', line)[-2])
    return bgM

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
        lastline = f.readlines()[-1]
        U = np.array([float(item)
                      for item in re.split('[(|)]', lastline)[-2].split(' ')])
    return float(A), U

# function to extract walls surface area


def get_ssa(FILENAME):
    TARGET = "Area   :    "
    with open(FILENAME, 'r') as f:
        A = None
        for line in f:
            if TARGET in line.strip():
                _, A = line.split(TARGET)
                A, _ = A.split('\n')
                break
        lastline = f.readlines()[-1]
    return float(A)

# Get mean volume velocity


def get_meanVel(FILENAME):
    with open(FILENAME, 'r') as f:
        lastline = f.readlines()[-1]
        U = np.array([float(item)
                      for item in re.split('[(|)]', lastline)[-2].split(' ')])
    return U

# get pressure value

# def get_pickle(FILENAME):
    
#     with open(FILENAME,'rb') as f:
#         val = pk.load(f)
    
#     return val

def get_pressure(FILENAME):
    TARGET = "dp "
    with open(FILENAME, 'r') as f:
        for line in f:
            if TARGET in line.strip():
                _, p = line.split(TARGET)
                p, _ = p.split(';\n')
                break
    return float(p)
# get simple time


def get_simplet(FILENAME):
    with open(FILENAME, 'r') as f:
        run_raw = f.readlines()[-8]
    runt = float(re.split('ClockTime = | s\n', run_raw)[1])
    return runt

# get snappy time


def get_snappyt(FILENAME):
    with open(FILENAME, 'r') as f:
        snappy_raw = f.readlines()[-3]
    snappyt = float(re.split('Finished meshing in = | s.\n', snappy_raw)[1])
    return snappyt


# load a pickle file

def load_pkl(FILENAME):
    
    with open(FILENAME,'rb') as f:
        val = pk.load(f)
    
    return val


# Main

# Path to files
root_dir = os.getcwd() + '/'
surf_path = 'postProcessing/outletVelocity/0/surfaceFieldValue.dat'
meanVel_p = 'postProcessing/volMeanVel/0/volFieldValue.dat'
# dp_p = 'dp.pickle'    # root_dir + '0/p'
checkMesh_p = root_dir + 'log.checkMesh'
runtime_p = root_dir + 'run_time.txt'
bgmesh_p = root_dir + 'bgMesh'
simple_p = root_dir + 'log.simpleFoam'
snappy_p = root_dir + 'log.snappyHexMesh'
ssa_p = 'postProcessing/patchAverage(name=walls,p)/0/surfaceFieldValue.dat'
cwd = Path(root_dir)
out_f = 'kc_flowfield.csv'

# velocity and cross section surface
A, U = get_surf(root_dir + surf_path)
u_volMean = get_meanVel(root_dir + meanVel_p)
u_meanMag = np.linalg.norm(u_volMean)

# Box side length
ppi = float(os.path.basename(cwd).split('_')[1])
d_pore = 0.0254/ppi  # 0.0254 (m/inch) -> 0.0254/ppi -> meters/pore 
Lx,Ly,Lz = get_box(checkMesh_p)

# Constants

rho = 1e3
mu = 1e-03
dP = get_pressure(bgmesh_p)
print('dP=',dP)

# get the volumetric porosity

por = get_vol(checkMesh_p) / (Lx*Ly*Lz)
print('volumetric porosity=',por)

# get the bulk and solid specific surface

ssa_bulk = get_ssa(ssa_p) / (Lx*Ly*Lz)
print('ssa_bulk=',ssa_bulk)

solid_vol = (Lx*Ly*Lz) - get_vol(checkMesh_p)
ssa_solid = get_ssa(ssa_p) / solid_vol
print('ssa_solid=',ssa_solid)


# Surface velocity

eps_s = ( A / ( Ly * Lz ) )
q = np.linalg.norm(U) * eps_s
print('superficial porosity=', eps_s)

# permeability

k = mu * Lx * q/dP/rho
print('permeability is =', k)

# Reynolds number

Re = rho * u_meanMag * d_pore/mu
print('Reynolds number =', Re)


# tot mesh cells

tot_cells = get_totCells(checkMesh_p)
print('total grid cells =', tot_cells)

# background mesh cells

# bgMesh = get_bgMesh(bgmesh_p)

case = os.path.basename(cwd)

# save results in dictionary

d = {'porosity': por, 'k': k, 'Re': Re, 'eps_s': eps_s, 'ssa_bulk': ssa_bulk, 'ssa_solid': ssa_solid}

name_pickle = case + '.pickle'

with open(name_pickle, 'wb') as pkf:
    pk.dump(d, pkf)


# save Reynolds number and Nu in C file
re = 'RE {};'.format(Re) + '\n' + 'NU {};'.format(mu/rho)
with open('./REYNOLDS', 'a') as re_f:
    re_f.write(re)

# print results in file
# order in file results is:
# case,ppi,por,k,Re,eps_s,ssa_bulk,ssa_solid


ppi = float(case.split('_')[1])

out = '{},'.format(case) + '{:.0f},'.format(ppi) + '{:.2f},'.format(por) + '{:.5e},'.format(k) + '{:.5e},'.format(Re) + '{:.2f},'.format(
    eps_s) + '{:.2f},'.format(ssa_bulk) + '{:.2f},'.format(ssa_solid) + '\n'

resultsPath = cwd.parent / out_f

if out_f in os.listdir(cwd.parent):
    with open(resultsPath, 'a') as res_f:
        res_f.write(out)
else:
    with open(resultsPath, 'w+') as res_f:
        res_f.write('case,ppi,por,k,Re,eps_s,ssa_bulk,ssa_solid')
        res_f.write('\n')
        res_f.write(out)