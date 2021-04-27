import os


case = os.path.basename(os.getcwd())

Pe_n = float(case.split('_')[-1])

str_out = 'PE {};'.format(Pe_n)

with open('PECLET','w') as out_f:
	out_f.write(str_out)
