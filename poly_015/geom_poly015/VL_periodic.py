import numpy as np
import tess as t
import pickle
import time
import sys
import os
import pandas as pd
import math as m 

cwd = os.getcwd() + '/'

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

# Funtions

    
def foam_iter(ctr,rd,box,itr=250):
    for i in range(itr):
        foam_it = t.Container(ctr, limits=box, periodic=True, radii=rd)
        ctr = np.array([item.centroid() for item in foam_it])
        rd = np.array([item.radius for item in foam_it])
    return foam_it

"""
This function takes all the faces vertices list of each cell in the tessellation
and reconstruct the edges connecivity. It return a list of list, in which each
element is the connection between two points in the cell vertices list
"""


def edgy(faces):
    edges = [[], []]
    for facet in faces:
        edges[0].extend(facet[:-1]+[facet[-1]])
        edges[1].extend(facet[1:]+[facet[0]])

    edges = np.vstack(edges).T
    edges = np.sort(edges, axis=1)
    edges = edges[:, 0] + 1j*edges[:, 1]  # Convert to imaginary
    edges = np.unique(edges)  # Remove duplicates
    edges = np.vstack((np.real(edges), np.imag(edges))).T  # Back to real

    return edges


"""
This function return only unique pairs of edges using sets
"""


def uniquify(edges):
    new = [tuple(row) for row in edges.reshape(len(edges), 6)]
    unique = list(dict.fromkeys(new))
    out = np.array(unique).reshape(len(unique), 2, 3)
    return out


"""
This function return only unique vertices of the foam calculated frome edges
"""


def getPoints(edges):
    pp = edges.reshape(len(edges)*2, 3)
    pp_tup = [tuple(row) for row in pp]
    pp_unq = list(dict.fromkeys(pp_tup))
    return np.array(pp_unq)


"""
This function takes 4 INPUTS: 
- the tessellation container, 'foam'
- number of decimal to which round the coordinates (default is 5)
- which additional outputs enable ( default is False)
return up to 3 output:
- All the edges regrouped in a single array
- If 'edge_class=True': all the edges, in the form of Geom.py class,
    regrouped in a single list
- If 'edge_cell=True':all the edges, regrouped per cell, in a single array
"""


def allEdgy(cells, decim=5, edge_class=False, edges_cell=False):
    faces = [elem.face_vertices() for elem in cells]
    vertices = [np.array(elem.vertices()) for elem in cells]
    links = [np.array(edgy(elem), dtype=int) for elem in faces]
    edges_cells = [elem[item] for elem, item in zip(vertices, links)]
    edge_unsort = np.around(np.vstack(edges_cells), decimals=decim)
    edge_sorted = np.array([t[::-1] if ((t[0, 0] < t[1, 0]) or (t[0, 0] == t[1, 0]
                                                                and t[0, 1] < t[1, 1]) or (t[0, 0] == t[1, 0])
                                        and t[0, 1] == t[1, 1] and t[0, 2] < t[1, 2])
                            else t for t in edge_unsort])
    allEdges = uniquify(edge_sorted)

    if edge_class == True and edges_cell == False:
        edgeClass = [Edge(Point(elem[0]), Point(elem[1])) for elem in allEdges]
        return allEdges, edgeClass

    elif edge_class == True and edges_cell == True:
        edgeClass = [Edge(Point(elem[0]), Point(elem[1])) for elem in allEdges]
        return allEdges, edgeClass, edges_cells

    return allEdges


def inside(arr, lbox, max_z=None):
    ll_box = np.array([-lbox, -lbox, 0])  # lower left of the box
    ur_box = np.array([lbox, lbox, max_z])  # upper right of the box
    indix = np.all(np.logical_and(ll_box <= arr,
                                  arr <= ur_box), axis=1)  # get indices
    return indix


def inside_rev(arr, lbox):
    ll_box = np.array([-lbox, -lbox, -lbox])  # lower left of the box
    ur_box = np.array([lbox, lbox, lbox])  # upper right of the box
    indix = np.all(np.logical_and(ll_box <= arr,
                                  arr <= ur_box), axis=1)  # get indices
    return indix


if __name__ == "__main__":

    start_time = time.time()

    # Path to sphere packing data 
    
    spherePack = cwd + 'Spheres-Auto/'
    pathCen = 'centroids.pickle'
    pathRad = 'radii.pickle'
    pathName = 'names.pickle'
    pathBox = spherePack + '1-CaseSetup.txt'

    # Retrieve Box dimensions
    
    with open(pathBox, 'r') as f3:
        ll = f3.readlines()
    Bside = float(ll[4].split()[4])

    # Retrive names and find indices of non-icosphere elements
    
    with open(pathName, 'rb') as f0:
        names = pickle.load(f0)
    cs = 'Icosphere'
    ico = [i for i, s in enumerate(names) if cs in s]
    names = names[ico]
    
    # Retrieve centroids coordinates
    
    with open(pathCen, 'rb') as f1:
        centers = pickle.load(f1)
    centers = centers[ico]

    # Retrieve spheres dimensions
    
    with open(pathRad, 'rb') as f2:
        dims = pickle.load(f2)
    dims = dims[ico]

    # Calculate radii
    
    rads = np.mean(np.around(dims, decimals=5)/2, axis=1)
    max_z = max(rads+centers[:, 2])

    # Remove points with centers outside box

    indx = inside(centers, Bside, max_z)
    centers = centers[indx]
    rads = rads[indx]
    names = names[indx]

    # Calculate REV bounding box and translate centers around (0,0,0)

    r_mean = rads.mean()
    r_max = rads.max()
    l_rev = 4 * r_mean + r_max  # rev box has 4 cells per side + sorrounding sphere
    ptsOrig = centers - centers.mean(axis=0)  # translate around (0,0,0)

    # Get REV
    
    indx_rev = inside_rev(ptsOrig, l_rev)
    ptsRev = ptsOrig[indx_rev]
    ptsRev_0 = ptsRev - ptsRev.mean(axis=0)
    rads_rev = rads[indx_rev]
    names_rev = names[indx_rev]


    # Define tessellation box
#     BoxTess = ((-Bside/2, -Bside/2, 0), (Bside/2, Bside/2, max_z))
    BoxTess = ((-l_rev, -l_rev, -l_rev), (l_rev, l_rev, l_rev))
    
    # Create a Laguerre-Voronoi tessellation of the box with centroids and radii
    # using module tess

    foam = foam_iter(ptsRev_0,rads_rev,BoxTess) # t.Container(ptsRev_0, limits=BoxTess, periodic=True, radii=rads_rev)
    allEdges, edgeClass, edgeCells = allEdgy(foam, decim=4, edge_class=True, edges_cell=True)
    
    allPoints = getPoints(allEdges)

    # Post process calculations

    d = {} # dictionary to store distributions
	

    d['edges_length'] = np.array([item.lenght() for item in edgeClass])
    d['faces_areas'] = np.array([y for x in [item.face_areas() for item in foam] for y in x])
    d['cell_volumes'] = np.array([item.volume() for item in foam])
    d['cell_distances'] = np.array([item.max_radius_squared() for item in foam])
    d['cell_n_faces'] = np.array([item.number_of_faces() for item in foam])
    d['cell_n_edges'] = np.array([item.number_of_edges() for item in foam])
    d['sphere_initial'] = rads
    d['sphere_rev'] = rads_rev

    indx=['mean', 'max', 'min', 'std_dev', 'perc_1','perc_2.5',
             'perc_5', 'perc_10', 'perc_25', 'perc_50', 'perc_75']
    df = pd.DataFrame(index=indx) # Dataframe storing distribution analysis

    for key in d:
        df[key] = [d[key].mean(), d[key].max(), d[key].min(), d[key].std(), 
                    np.quantile(d[key], 0.01), np.quantile(d[key], 0.025),
                      np.quantile(d[key], 0.05), np.quantile(d[key], 0.1), 
                      np.quantile(d[key], 0.25), np.quantile(d[key], 0.5), 
                      np.quantile(d[key], 0.75)]


    D = {'d_sphr': 2*r_mean, 'd_cell': 2*np.cbrt(3*d['cell_volumes'].mean()/4/np.pi)}
    # Export analysis in .csv format

    # df.to_csv('postProcessFoam.csv')
    df.to_pickle('postProcessFoam.pkl')

    # Export distributions dictionary
    with open('foamDistr.pickle', 'wb') as f:
        pickle.dump( d, f)
    
    # Export distributions dictionary
    with open('foamPore_D.pkl', 'wb') as f:
        pickle.dump( D, f)
    # Export edges data to Blender with pickle file

    with open('edgesData.pickle', 'wb') as f:
        pickle.dump( edgeClass, f)

    # Export edges data to Blender with pickle file
    
    with open('pointData.pickle','wb') as f1:
        pickle.dump( allPoints, f1)
    
    print("Total number of edges is:", len(allEdges))
    print("Total number of vertices is:",len(allPoints))
    print("--- %s seconds ---" % (time.time() - start_time))
