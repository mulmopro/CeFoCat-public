This KC_readme.txt file was generated on 2021-03-31 by Enrico Agostini

GENERAL INFORMATION

1. Title of Dataset: Kelvin's Cell Workflow

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

4. Was data derived from another source? yes/no
	A. If yes, list source(s): 

5. Recommended citation for this dataset: 


DATA & FILE OVERVIEW
```
1. File List:					# KC = Kelvin's Cell, OF = OpenFOAM

kc 								# Main directory
├── creatorCase.py    			# Python script for OF cases generation
│
├── geom_kc						# Folder for the creation of the geometry
│   ├── blend_dir				# Folder containing the geometry Blender files (.blend)
│   ├── generate.py 			# Python script used by Blender to generate the geometries
│   ├── Geomrun.sh 				# Shell file to lauch the all geometry creation process
│   ├── kc_foam.py 				# Python script to generate the KC edges and nodes coordinates (set to 1 KC)
│   ├── new_connectivity.csv	# KC nodes connectivity
│   ├── new_coord.csv			# KC nodes coordinates
│   └── stl_dir					# Folder containing the geometry STL files (.stl)
│
├── template_flowfield 			# OF flowfield case template
│   ├── 0						# Simulation initial boundary conditions for p and U
│   ├── Allclean				# Shell script to erase simulation data
│   ├── bgMesh					# Text file with initial informations (initial dp, meshing)
│   ├── constant				# Contains Geometry, transportProperties and turbulenceProperties
│   ├── fScale.py 				# Python script to calculate the scaling factor
│   ├── meshLink.py 			# Python script to retrieve the external Mesh directory
│   ├── permeability.py 		# Python script to post-processes simulation data and generate results file
│   ├── runCase.sh 				# Shell script that contains all the commands to exec the OF case
│   └── system 					# Contains the simulation control dictionaries
│
├── template_mesh				# OF mesh creation case template
│   ├── Allclean				# Shell script to erase simulation data
│   ├── bgMesh					# Text file with initial informations (meshing subdivisions, dimensions)
│   ├── constant				# Contains Geometry
│   ├── runMeshing.sh			# Shell script that contains all the commands to exec
│   └── system					# Contains the simulation meshing dictionaries
│
└── template_scalar				# OF scalar transport case template
    ├── 0						# Simulation initial boundary conditions for p,U (from flowfield), scalar T 
    ├── Allclean				# Shell script to erase simulation data
    ├── collProp.py				# Python script to post-processes simulation data and generate results file
    ├── constant				# Contains Geometry, transportProperties and turbulenceProperties
    ├── DT.py					# Python script to calculate diffusivity (starting from Re and Pe)
    ├── runCase.sh				# Shell script that contains all the commands to exec
    └── system					# Contains the simulation control dictionaries
```
2. Relationship between files, if important: 

	1) Geometry generation:
		a. Access 'kc/geom_kc'
		b. Set the porosity values editing 'Geomrun.sh' and launch it
			NB: change the Blender Alias accordingly to your system!
		c. Blender and STL Files are saved in their respective folders
	
	2) OF cases generation:
		a. Access 'kc'
		b. Edit "creatorCase.py" with "pores per inch (PPI)" values & 
			copy the same porosity values as in 'Geomrun.sh' 
		c. OF cases are created with the following format:
			MESH_CASES --> 'mesh_<porosity_values>'
			FLOWFIELD_CASES --> '<geometry_model>_<ppi_value>_<porosity_value>'
			SCALAR_CASES (within each FLOWFIELD_CASE)--> 'Pe_<peclet_number_value>'
	
	3) Run OF cases:
		a. Run each flowfield case launching 'runCase.sh'
		b. Flowfiled data are collected in results .csv file named '<geometry_model>_flowfield.csv'
			located in the main directory (cfr. 'permeability.py')
		c. Inside each flowfield directory, enter each scalar simulation folder 'Pe_<peclet_number>'
			and launch 'runCase.sh'
		d. Scalar transport data are collected in a results .csv file named '<geometry_model>_scalar.csv'
			located in the main directory (cfr. 'collProp.py')



METHODOLOGICAL INFORMATION

1. Description of methods used for generation of data: 
   
   The geometry workflow generate a single Kelvin's Cell with cylinders in place of edges and icospheres 
   in place of nodes. The diameter of the cylinder is chosen based on the required porosity of the geometry.
   The estimation of the diamter is done by a quadratic empirical correlation that can be changed. 
   It can be edited in 'generate.py' (line 145).

   For Simulations set-up consults article at: <link of the article>

2. Instrument- or software-specific information needed to interpret the data: 

   Required software:

   Python 3.7.7 (Tested)

   Blender 2.81 or Blender 2.83.5 (Tested) at https://download.blender.org/release/

   Please be shure to install 'Pandas' module (https://pandas.pydata.org/) in the 
   bundled Python distribution of Blender (use pip install inside Blender python console)

   Required Python modules:

   pandas (https://pandas.pydata.org/)
   tess (https://pypi.org/project/tess/, https://tess.readthedocs.io/en/latest/, https://github.com/wackywendell/tess)

   Modules distributed with standard Anaconda distribution:

   argparse (https://docs.python.org/3/library/argparse.html)
   math (https://docs.python.org/3/library/math.html)
   numpy (https://numpy.org/)
   os (https://docs.python.org/3/library/os.html)
   pathlib (https://docs.python.org/3/library/pathlib.html)
   pickle (https://docs.python.org/3/library/pickle.html)
   re (https://docs.python.org/3/library/re.html)
   shutil (https://docs.python.org/3/library/shutil.html)
   sys (https://docs.python.org/3/library/sys.html)
   time (https://docs.python.org/3/library/time.html)

   Blender python module (included in Blender budled python distribution):
   bpy (https://docs.blender.org/api/current/index.html)

3. Environmental conditions: POSIX OS required

   Tested OS:

   Ubuntu 18.04.5 LTS