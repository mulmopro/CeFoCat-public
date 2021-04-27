#! /usr/bin/python3
import numpy as np
###############USER INPUT#####################
###Normal distribution parameters and number of grains
mu=100 #[microns]
cv=0.15
sigma=cv*mu
n_grains=6000
n_bins=int(np.log2(n_grains) +1)
###Container Specification
#container=
#"box" for a box, "cyl" for a cylinder. 
#Sizes in [mm]
container="box"
box_side=1.5
cyl_diam=1.0
cyl_height=2

###Object Specification
#non_primitive_model=
#Options: 0 deactivated (spheres), "filename" for a filename.blend model, to be found in a ./Library subfolder
non_primitive_model=0

###Simulation data
mean_mass=0.1    #mass of a mean size particle (ATTENTION: Blender can not handle object mass smaller then 0.001)
refine_level=3   #refinement level for blender ico-spheres
max_frame=400  #max number of frames to render
bu_to_micron=100 #factor to convert blender units into microns

###############USER INPUT END#################


###############CONVERSION FACTORS#################
bu_to_mm=bu_to_micron/1000.0   #convertion bu to mm
micron_to_bu=1.0/bu_to_micron  #convertion micron to bu
mm_to_bu=1.0/bu_to_mm          #convertion mm to bu
mean_size=mu*micron_to_bu      #mean particle size in bu
mass_0=mean_mass/(mean_size*mean_size*mean_size) #mass of a particle of size=1bu
if non_primitive_model==0:
    mass_0=mean_mass/(mean_size*mean_size*mean_size) #mass of a particle of size=1bu
else:
    mass_0=mean_mass/(mean_size*mean_size*mean_size) #mass of a particle of size=1bu
###############CONVERSION FACTORS END#################



import math
import random
class Bin:
	"""docum"""
	nome="asd"
	binwidth=0
	value=0
	grains=0
	PDF=0
	normPDF=0
	def __init__(self,larghezza=None,valore=None):
		if larghezza is None:
			self.binwidth = None
		else:
			self.binwidth=larghezza
		if valore is None:
			self.value = None
		else:
			self.value=valore

print("Gaussian Grain Size Distribution Generator\n\n")

actual_n_grains=0

###############GAUSSIAN###############
width=6*sigma
variance=sigma**2
binwidth=width/n_bins

binlist=[]
integral=0
integralnorm=0
for i in range(n_bins):
	binlist.append(Bin(binwidth,(mu-3*sigma)+binwidth/2+i*binwidth))
	#First argument: width of the class
	#Second argument: the total span of the curve is taken as 6*sigma, thus
	# the "leftmost" limit of the gaussian curve is mean-3*sigma
	binlist[i].PDF=1/(sigma*(2*math.pi)**0.5) * math.exp(-(binlist[i].value-mu)**2/(2*sigma**2))

for i in range(n_bins):
	integral+=(binlist[i].PDF)

for i in range(n_bins):
	binlist[i].normPDF=binlist[i].PDF/integral

for i in range(n_bins):
	integralnorm+=(binlist[i].normPDF)
	
for i in range(n_bins):
	binlist[i].grains=round(n_grains*binlist[i].normPDF)
	actual_n_grains+=binlist[i].grains

###############OUTPUT###############
filename="1-CaseSetup.txt"
f=open(filename,'w')

#Add units
f.write("Dimensions in Blender Units. 1 BU equals X millimeters or Y microns. X= "+str(bu_to_mm)+"; Y= "+str(bu_to_micron)+"\n")
#Add density
f.write("Particle reference mass: mass_0="+str(mass_0)+"\n")
#Add refinement level
f.write("Refinement level for blender ico-spheres (-): refine_level="+str(refine_level)+"\n")
#Add max number of frames to render
f.write("Max number of frames to render (-): max_frame="+str(max_frame)+"\n")

#Add Container
if container=="box":
    f.write("Container: Box | Side: "+str(box_side*mm_to_bu)+"\n")
else:
    f.write("Container: Cylinder | Diameter: "+str(cyl_diam*mm_to_bu)+" , Height: "+str(cyl_height*mm_to_bu)+"\n")

if non_primitive_model==0: #Add Sphere model
    f.write("Classes:"+str(n_bins)+" - Total Grains:"+str(actual_n_grains)+" - Model:\"Spheres\"\n")
else: #Add NonPrimitive model
    f.write("Classes:"+str(n_bins)+" - Total Grains:"+str(actual_n_grains)+" - Model:\""+str(non_primitive_model)+"\"\n")

for i in range(n_bins): #Add Grain Distribution
    strout="Bin "+str(i+1)+": Size="+str(binlist[i].value*micron_to_bu)+" Grains="+str(binlist[i].grains)+"\n"
    f.write(strout)

f.close()
####################OUTPUT END################


####################REPORT################
print("List of grain diameters, by class:")
for i in range(n_bins):
	print(binlist[i].value)
print("\n")

print("List of PDFs, by class:")
for i in range(n_bins):
	print(binlist[i].PDF)
print("\n")

print("Integral PDF",integral,"\n")

print("List of normalized PDFs, by class:")
for i in range(n_bins):
	print(binlist[i].normPDF)
print("\n")

print("Integral normalized PDF",integralnorm,"\n")

print("Grains each class:\n")
for i in range(n_bins):
	print(binlist[i].grains)
print("\n")

print("Total actual grains (input grains)",actual_n_grains,n_grains)
####################REPORT END################
