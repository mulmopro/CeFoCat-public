This Eagostini_POLY_readme.txt file was generated on 2021-03-31 by Enrico Agostini

GENERAL INFORMATION

1. Title of Dataset: Voronoi-Laguerre geometric model foam workflow

2. Author Information
	A. Principal Investigator Contact Information
		Name: Enrico Agostini
		Institution: Dept. Applied science and technology, Politecnico di Torino
		Address: Corso Duca degli Abruzzi, 24, 10129, Torino, Italy
		Email: enrico.agostini@polito.it

	B. Associate or Co-investigator Contact Information
		Name: Gianluca Boccardo
		Institution: Dept. Applied science and technology, Politecnico di Torino
		Address: Corso Duca degli Abruzzi, 24, 10129, Torino, Italy
		Email: gianluca.boccardo@polito.it

	C. Alternate Contact Information
		Name: Daniele Marchisio
		Institution: Dept. Applied science and technology, Politecnico di Torino
		Address: Corso Duca degli Abruzzi, 24, 10129, Torino, Italy
		Email: daniele.marchisio@polito.it

3. Date of data collection (single date, range, approximate date): 2021-03-31

4. Geographic location of data collection: Torino,Italy

5. Information about funding sources that supported the collection of the data:
	Ministry of University and Research (https://www.mur.gov.it/it)


SHARING/ACCESS INFORMATION

1. Licenses/restrictions placed on the data: 

2. Links to publications that cite or use the data: 

3. Links to other publicly accessible locations of the data: 

4. Was data derived from another source? yes
	A. If yes, list source(s): 
		"BSands" code developed by: Boccardo, Gianluca, et al. "Validation of a novel open-source work-flow for the
		simulation of packed-bed reactors." Chemical Engineering Journal 279 (2015): 809-820.

5. Recommended citation for this dataset: 


DATA & FILE OVERVIEW

1. File List:							# VL = Voronoi-laguerre, VO = Voronoi, OF = OpenFOAM

poly_015								# Main directory
│
├── creatorCase.py						# Python script for OF cases generation
│
├── geom_poly015						# Folder for the creation of the geometry
│   ├── blend_dir						# Folder containing the geometry Blender files (.blend)
│   ├── generate.py						# Python script used by Blender to generate the geometries
│   ├── Geomrun.sh						# Shell script to lauch the all geometry creation process
│   ├── Spheres-Auto					# Folder containing "BSands" (Hard-sphere packing code)
│   │   ├── 1-Setup.py					# Python script to set up the sphere-packing simulation parameters
│   │   ├── 2-Placement-Automatic.py	# Python script to initialize the hard-sphere discrete-time simulation
│   │   ├── blendRun.sh					# Shell	script to run "BSands"
│   │   ├── export_blender.py			# Python script to export sphere coordinates, dimensions and names
│   │   └── test.blend					# Blender template empty case
│   │
│   ├── stl_dir							# Folder containing the geometry STL files (.stl)
│   │
│   └── VL_periodic.py					# Python script to calculate the VO/VL tessellation
│
├── perm.csv							# CSV file to initialize the pressure drop
│
├── permeability.pkl					# PICKLE file to initialize the pressure drop
│
├── template_flowfield					# OF flowfield case template
│   ├── 0								# Simulation initial boundary conditions for p and U
│   ├── Allclean						# Shell script to erase simulation data
│   ├── bgMesh							# Text file with initial informations (initial dp, meshing parameters)
│   ├── constant						# Contains Geometry, transportProperties and turbulenceProperties
│   ├── dPore.py						# Python script to retrieve the mean pore diameter from tessellation data
│   ├── dp.py							# Python script to initialize pressure drop from Darcy Law
│   ├── fScale.py						# Python script to calculate the scaling factor
│   ├── meshLink.py						# Python script to retrieve unscaled mesh and needed meshing log files 
│   ├── permeability.py					# Python script to post-process simulation data and to generate results
│   ├── runCase.sh						# Shell script that contains all the commands to exec the OF case
│   └── system							# Contains the simulation control dictionaries
│
├── template_mesh						# OF mesh creation case template
│   ├── 0								# Initial condition (dummy folder)
│   ├── Allclean						# Shell script to erase simulation data
│   ├── bgMesh							# Text file with initial meshing parameters
│   ├── constant						# Contains Geometry STL file
│   ├── dPore.py						# Python script to retrieve the mean pore diameter from tessellation data
│   ├── runMeshing.sh					# Shell script that contains all the commands to exec meshing of the geometry
│   ├── splitMesh.py					# Python script that remove secondary regions (separated from main comp. domain)
│   └── system							# Contains the simulation meshing dictionaries
│
└── template_scalar						# OF scalar transport case template
    ├── 0								# Simulation initial boundary conditions for p,U (from flowfield), scalar T 
    ├── Allclean						# Shell script to erase simulation data
    ├── collProp.py						# Python script to post-processes simulation data and generate results file
    ├── constant						# Contains Mesh, transportProperties and turbulenceProperties
    ├── DT.py							# Python script to calculate diffusivity (starting from Re and Pe)
    ├── runCase.sh						# Shell script that contains all the commands to exec the OF case
    └── system							# Contains the simulation control dictionaries


2. Relationship between files, if important: 

	1) Random hard-sphere packing generation with "BSand":
		
		a. Access 'poly_015/geom_poly015/Sphere-Auto'
		
		b. Edit:
				- mean grain size for gaussian distribution "mu"
				- coefficient of variation "cv" in range [0;0.35] (default set to 0.15)
				- number of grains 
				- container == "box" and "box_side" in range [0.5;1.5 or higher]
				- number of frames "max_frame" (default set to 400) 

		c. Launch 'blendRun.sh' --> USE Blender 2.79 <-- 
			NB: change aliases for Blender 2.79 accordingly to your system!
			The hard-sphere simulation can take up to 2/3 hours for 6000 spheres!
			Total time is printed in log file
		
		d. The simulation generate 3 .blend files and 1 .stl file:

			- 'b1-start' --> Ignore!
			- 'b2-endSimulation' --> Needed
			- 'b3-forExport' --> Ignore!
			- 'merged.stl' --> Ignore!

		e. Open 'b2-endSimulation' with --> Blender 2.8x <--:
			In "scripting mode" launch 'export_blender.py'
			The following files are created in 'poly_015/geom_poly015':

			- 'centroids.pickle'
			- 'radii.pickle'
			- 'names.pickle'

	2) VO/VL tessellation calculation:

		a. In 'VL_periodic.py' edit:
			- "pores per REV side" at line 261, variable 'l_rev' (default value == 4)

		b. Run 'VL_periodic.py' (at least Python 3.7)

		c. Output files:
			- 'postProcessFoam.pkl'	  # tessellation quantities distributions, see script for details (DataFrame)
			- 'foamDistr.pickle'      # tessellation quantities distributions, see script for details (python dictionary)
			- 'foamPore_D.pkl'        # mean foam pore diameter & mean grain diameter
			- 'edgesData.pickle'      # foam edges data, stored in custom Class, see script
			- 'pointData.pickle'      # foam nodes data, stored in custom Class, see script

	3) Generate foam geometry:
		
		a. Set the porosity values editing 'Geomrun.sh' and run it
		  	NB: change the Blender Alias accordingly to your system!
		b. Blender and STL Files are saved in their respective folders

	4) OF cases generation:
		a. Access 'poly_015'
		b. Edit "creatorCase.py" with "pores per inch (PPI)" values & 
			copy the same porosity values as in 'Geomrun.sh' 
		c. OF cases are created with the following format:
			MESH_CASES --> 'mesh_<porosity_values>'
			FLOWFIELD_CASES --> '<geometry_model>_<ppi_value>_<porosity_value>'
			SCALAR_CASES (within each FLOWFIELD_CASE)--> 'Pe_<peclet_number_value>'
	
	5) Run OF cases:
		a. Run each flowfield case launching 'runCase.sh'
		b. Flowfiled data are collected in results .csv file named '<geometry_model>_flowfield.csv'
			located in the main directory (cfr. 'permeability.py')
		c. Inside each flowfield directory, enter each scalar simulation folder 'Pe_<peclet_number>'
			and launch 'runCase.sh'
		d. Scalar transport data are collected in a results .csv file named '<geometry_model>_scalar.csv'
			located in the main directory (cfr. 'collProp.py')



METHODOLOGICAL INFORMATION

1. Description of methods used for generation of data: 
   
   The geometry workflow generate a Voronoi/Voronoi-Laguerre REV with cylinders in place of edges and icospheres 
   in place of nodes. The diameter of the cylinder is chosen based on the required porosity of the geometry.
   The estimation of the diamter is done by a quadratic empirical correlation that can be changed. 
   It can be edited in 'generate.py' (line 145).

   For Simulations set-up consults article at: <link of the article>

2. Instrument- or software-specific information needed to interpret the data: 

   Required software:

   Python 3.7.7 (Tested)

   Blender 2.79 (Tested) at https://download.blender.org/release/

   Blender 2.81 or Blender 2.83.5 (Tested) at https://download.blender.org/release/

   Please be shure to install 'Pandas' module (https://pandas.pydata.org/) in Blender 
   bundled Python distribution (use pip install inside Blender python console)

   Required Python modules:

   pandas 		(https://pandas.pydata.org/)
   tess 		(https://pypi.org/project/tess/, https://tess.readthedocs.io/en/latest/)

   Modules distributed with standard Anaconda distribution:

   argparse 	(https://docs.python.org/3/library/argparse.html)
   math 		(https://docs.python.org/3/library/math.html)
   numpy 		(https://numpy.org/)
   os 			(https://docs.python.org/3/library/os.html)
   pathlib 		(https://docs.python.org/3/library/pathlib.html)
   pickle 		(https://docs.python.org/3/library/pickle.html)
   re 			(https://docs.python.org/3/library/re.html)
   shutil 		(https://docs.python.org/3/library/shutil.html)
   sys 			(https://docs.python.org/3/library/sys.html)
   time 		(https://docs.python.org/3/library/time.html)

   Blender python module (included in Blender budled python distribution):
   bpy 			(https://docs.blender.org/api/current/index.html)

3. Environmental conditions: POSIX OS required

   Tested OS: Ubuntu 18.04.5 LTS