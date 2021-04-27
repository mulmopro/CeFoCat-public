import numpy as np
import pandas as pd
import pickle as pk
import math as m
import os
from pathlib import Path

# Geometrical Classes


"""
Define the "Point" class:
it contains the three coordinates and can return them as a numpy array
"""


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

    def line_x(self, n_p):

        if (n_p % 2) == 0:
            t = np.concatenate((np.linspace(0,0.5,int(n_p/2),endpoint=False),np.linspace(0.5,1,int(n_p/2))))
        
        elif (n_p % 2) != 0:
            t = np.linspace(0,1,n_p)
        
        line = np.array([self.start.vec() + elem * self.dP for elem in t])
        
        return line

# paths
cwd = Path(os.getcwd())
coord_p = cwd / 'new_coord.csv'
conn_p = cwd / 'new_connectivity.csv'

# import edges data

coord = pd.read_csv(coord_p)
pts = coord.to_numpy() / np.sqrt(2)

conn = pd.read_csv(conn_p)
lnks = conn.to_numpy().astype(int)

edges = pts[lnks]

# fill a list of Point class istances with vertices

# nodes = []
# for pt in pts:
# 	nodes.append(Point(pt))

struts = []

for e in edges:
	start = Point(e[0])
	end = Point(e[1])
	struts.append(Edge(start,end))

# export as pickle files

with open('pointData.pickle','wb') as f:
	pk.dump(pts,f)

with open('edgesData.pickle','wb') as f:
	pk.dump(struts,f)
