import os
import numpy as np  
import pickle as pk
import re
from pathlib import Path

# functions


def get_kfiltr(FILENAME):
	with open(FILENAME) as f:
		K_raw = f.readlines()[-1]
		K = re.split(' |\n',K_raw)[1] 
	return float(K)


def get_T(FILENAME):
	with open(FILENAME) as f:
		t_raw = f.readlines()[-1]
		t = re.split('\t|\n',t_raw)[1]
	return float(t)

# Main

cwd = Path(os.getcwd())
parentDir = cwd.parent
T_volAve_p = cwd / 'postProcessing/volFieldValue/0/volFieldValue.dat'
T_outlet_p =  cwd / 'postProcessing/patchAverage(name=back,T)/0/surfaceFieldValue.dat'
K_filtr_p = cwd / 'breakthrough.dat'

case = os.path.basename(cwd.parent)

type_s = case.split('_')[0]
ppi_s = case.split('_')[1]
por_s = case.split('_')[2]
pe_s = os.path.basename(cwd).split('_')[-1]

out_f = 'kc_scalar.csv'

# constants
k_b = 1.38e-23
T = 293
nu = 1e-06
mu = 1e-03
rho = 1e03

# get Peclet number
Pe_n = float(pe_s)
print('Pe_n =', Pe_n)

# get Reynolds from flowfield results
res_file = [ s for s in  os.listdir(cwd.parent) if '.pickle' in s][0]
with open(parentDir / res_file,'rb') as f:
	d = pk.load(f)
Re_n = d['Re']
print('Re_n =', Re_n)

# calculate transport coefficient
DT = Re_n/Pe_n * nu
print('DT =', DT)

# calculate colloidal particle diameter

d_c = k_b*T/3/np.pi/mu/DT
print('d_c =', d_c)

K_filtr = get_kfiltr(K_filtr_p)
print('K_filtr =',K_filtr)

T_outlet = get_T(T_outlet_p)
print('T_outlet =',T_outlet)

T_volAve = get_T(T_volAve_p)
print('T_mean =',T_volAve)

# print results to .csv file 
# right order is:
# case,ppi,por,Pe,Re,DT,d_c,K_filtr,T_out,T_average

case_1 = case + '_' + pe_s
ppi = float(ppi_s)
por = float(por_s)

out = '{},'.format(case_1) + '{:.0f},'.format(ppi) + '{:.0f},'.format(por) + '{:.0f},'.format(
	Pe_n) + '{:.5e},'.format(Re_n) + '{:.5e},'.format(DT) + '{:.5e},'.format(
	d_c) + '{:.5e},'.format(K_filtr) + '{:.5f},'.format(T_outlet) + '{:.5f},'.format(T_volAve) + '\n'

resultsPath = cwd.parents[1] / out_f

if out_f in os.listdir(cwd.parents[1]):
	with open( resultsPath,'a') as f:
		f.write(out)

else:
	with open(resultsPath, 'w+') as f:
		f.write('case,ppi,por,Pe,Re,DT,d_c,K_filtr,T_out,T_average' + '\n')
		f.write(out)


with open( 'transProp_check.txt','w') as f:
	f.write('Pe_n = {:.0f}\n'.format(Pe_n))
	f.write('DT = {:.5e}\n'.format(DT))
	f.write('d_c = {:.2f} nm\n'.format(d_c / 1e-09))

