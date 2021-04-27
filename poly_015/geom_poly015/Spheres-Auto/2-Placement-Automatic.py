#!/usr/bin/python3
import random
import math
import bpy
import mathutils
from mathutils import noise
pi=math.pi
Nr=noise.random

def deselect_all():
	for i in bpy.context.selected_objects:
		bpy.context.selected_objects[0].select=False
		#The reason this refers to [0] every iteration of the loops is that each loop cycle the object [0] gets DEselected,
        #and exits the bpy.context.selected_objects array. Thus, each cycle [0] is actually a new object.
def select_all():
	for i in bpy.context.selectable_objects:
		i.select=True
####################CONTAINER DEFINITION####################
def box_create(sob):
    bpy.ops.mesh.primitive_plane_add(location=(0,0,0), rotation=(0,0,0))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.context.object.name="MinZ"
    bpy.data.objects["MinZ"].scale[0]=(sob/2)
    bpy.data.objects["MinZ"].scale[1]=(sob/2)
    #MinX side
    bpy.ops.mesh.primitive_plane_add(location=(-sob/2,0,sob/2), rotation=(0,pi/2,0))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.context.object.name="MinX"
    bpy.data.objects["MinX"].scale[0]=(sob/2)
    bpy.data.objects["MinX"].scale[1]=(sob/2)
    #MaxX side
    bpy.ops.mesh.primitive_plane_add(location=(sob/2,0,sob/2), rotation=(0,pi/2,0))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.context.object.name="MaxX"
    bpy.data.objects["MaxX"].scale[0]=(sob/2)
    bpy.data.objects["MaxX"].scale[1]=(sob/2)
    #MinY side
    bpy.ops.mesh.primitive_plane_add(location=(0,-sob/2,sob/2), rotation=(pi/2,0,0))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.context.object.name="MinY"
    bpy.data.objects["MinY"].scale[0]=(sob/2)
    bpy.data.objects["MinY"].scale[1]=(sob/2)
    #MaxY side
    bpy.ops.mesh.primitive_plane_add(location=(0,sob/2,sob/2), rotation=(pi/2,0,0))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    bpy.context.object.name="MaxY"
    bpy.data.objects["MaxY"].scale[0]=(sob/2)
    bpy.data.objects["MaxY"].scale[1]=(sob/2)

    #TABLEMAT ADDITION (FOR BOXES)
    #The tablemat will be of height=2.
    bpy.ops.mesh.primitive_cube_add(radius=1,location=(0,0,-1.1))
    obj=bpy.context.active_object #pointer to active object
    bpy.ops.transform.resize(value=(sob/2,sob/2,1))
    #Set it as a rigid-body object
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj.rigid_body.collision_shape='MESH'
    bpy.context.object.name="Tablemat"


def cylinder_create(d,h):
    r=d/2
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=h,location=(0,0,h/2))
    obj=bpy.context.active_object #pointer to active object


    bpy.ops.object.mode_set(mode='EDIT', toggle=False)      # set to Edit Mode
    #EDIT MODE ON 
    bpy.ops.mesh.select_all(action='DESELECT') #deselect all, just to be sure
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #OBJECT MODE ON 
    obj.data.polygons[-4].select = True #Select only those to delete (-4 is top face, -1 is bottom face)
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)      # set to Edit Mode AGAIN
    #EDIT MODE ON
    bpy.ops.mesh.delete(type='FACE') #Finally delete the faces
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #OBJECT MODE ON 
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj.rigid_body.collision_shape='MESH'

    #TABLEMAT ADDITION (FOR CYLINDERS)
    #The tablemat will be of height=2.
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=10,location=(0,0,-6))
    obj=bpy.context.active_object #pointer to active object
    #Set it as a rigid-body object
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj.rigid_body.collision_shape='MESH'
    bpy.context.object.name="Tablemat"
    ##SECOND TABLEMAT BECAUSE FUCK ALL
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=1,location=(0,0,-0.5))
    obj=bpy.context.active_object #pointer to active object
    #Set it as a rigid-body object
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj.rigid_body.collision_shape='MESH'
    bpy.context.object.name="Tablemat2"
    ##THIRD TABLEMAT BECAUSE FUCK ALL
    bpy.ops.mesh.primitive_cylinder_add(radius=r,depth=1,location=(0,0,-1.5))
    obj=bpy.context.active_object #pointer to active object
    #Set it as a rigid-body object
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj.rigid_body.collision_shape='MESH'
    bpy.context.object.name="Tablemat3"
####################CONTAINER DEFINITION END####################

#################### DISTRIBUTION OF PARTICLES ON A PLANE ####################
def get_plane_pos(distance,size,type,delta_corr,r_max_corr,xy_corr):
	# op1: delta_corr is to avoid grains being too packed and exploding
	# op2: r_max_corr is to have grains further from the wall
    # op3: xy_corr
    xy=[0,0]
    plane_pos=[]
    num_in_plane=0
    num_in_row=int(size/distance)
    delta=size/num_in_row*delta_corr
    r_max=(size-delta)/2*r_max_corr
    r_2_max=r_max*r_max
    xy_0=-r_max
    print(num_in_row,delta,xy_0)
    for i in range(num_in_row):
        xy[0]=xy_0+i*delta
        x_2=xy[0]*xy[0]
        for j in range(num_in_row):
            xy[1]=xy_0+xy_corr*j*delta
            r_2=x_2+xy[1]*xy[1]
            if (type=="Box"):
                plane_pos.append(xy[:])
                num_in_plane=num_in_plane+1
            elif (r_2<=r_2_max):
                plane_pos.append(xy[:])
                num_in_plane=num_in_plane+1
    return num_in_plane, plane_pos

#################### IMPORT DATA FROM FILE #################### 
rel_filename="1-CaseSetup.txt"
filename=bpy.path.abspath("//")+rel_filename
f=open(filename)
lines=f.readlines()
f.close()

l_num=0
bu_to_mm=float(lines[0][(lines[0].find("X=")+3):(lines[0].find(";"))])
mass_0=float(lines[1][(lines[1].find("mass_0=")+7):-1])
refine_level=float(lines[2][(lines[2].find("refine_level=")+13):-1])
max_frame=float(lines[3][(lines[3].find("max_frame=")+10):-1])
str_container=lines[4][(lines[4].find("Container: ")+11):(lines[4].find("|")-1)]
if str_container=="Box":
    bl_side=float(lines[4][(lines[4].find("Side: ")+6):-1])
if str_container=="Cylinder":
    bl_cyl_diameter=float(lines[4][(lines[4].find("Diameter: ")+10):(lines[4].find(",")-1)])
    bl_cyl_height=float(lines[4][(lines[4].find("Height: ")+8):-1])
str_classes=lines[5].find("Classes:")
str_totgrains=lines[5].find("- Total Grains:")
str_model=lines[5].find("- Model:")
n_bins=int((lines[5][(str_classes+8):(str_totgrains)]))
tot_grains=int((lines[5][(str_totgrains+15):(str_model)]))
model=lines[5][(str_model+8):-1]

matrix=[[0 for x in range(2)] for y in range (n_bins)]

max_distributed_size=0
for i in range(6,(6+n_bins)):
    str_size=lines[i].find("Size=")
    str_grains=lines[i].find("Grains=")
    grain_size=float((lines[i][(str_size+5):(str_grains)]))
    grain_num=int((lines[i][(str_grains+7):(str_grains+12)]))
    # In matrix[row][column]: row is bin, column(0) is grain_size and column(1) is grain_num
    matrix[i-6][0]=grain_size
    matrix[i-6][1]=grain_num
    if (grain_size>max_distributed_size):
        max_distributed_size=grain_size

#################### IMPORT DATA FROM FILE END #################### 

############### CREATION OF UNIDIMENSIONAL LIST OF ALL GRAINS (VALUE=grain_size)(Which is, grain diameter) ###############
grain_list=[]
for i in range(n_bins):
    for j in range(matrix[i][1]): #in each bin, for as many times as the number of grains in each bin...
        grain_list.append(matrix[i][0]) #... add a number equal to the bin diameter
#grain_list[] is now a 1D array of each grain diameter for the complete distribution. E.G.: 6 bins, 50 grains each, grain_list has 300 items.
############### CREATION OF UNIDIMENSIONAL LIST OF ALL GRAINS (VALUE=grain_size) END ###############

############### CALCULATE SEPARATION MULTIPLIER ############### 
if model=="\"Spheres\"":
    sepmul=(max_distributed_size*1.05) #separation multiplier : place next grain at sepmul blender units from one another
else:
    sepmul=(max_distributed_size*0.5) #separation multiplier : place next grain at sepmul blender units from one another

primitive=0

####################NONPRIMITIVE MODEL IMPORT####################
if model.find("Spheres")!=-1:
    model_name=model[1:-1]
    primitive=1
else:
    model_name=model[1:-1]
    cwd=bpy.path.abspath("//")
    structure=cwd+"Library/"
    bpy.ops.wm.link_append(filepath=structure+model_name+".blend/Object/"+model_name,directory=structure+model_name+".blend/Object/",filename=model_name,link=False)
    bpy.ops.object.make_local(type='SELECT_OBJECT')
    bpy.data.objects[model_name].select=True
    bpy.ops.transform.translate(value=(0,0,-10))
    for i in range(len(list(bpy.data.objects))):
        if bpy.data.objects[i].name == model_name:
            i_index=i
#################### NONPRIMITIVE MODEL IMPORT END ####################
print(model_name)
if model_name=="Bead":
    op1=2.5
    op2=0.9
    op3=2.2
    sepmul_mult=2
    friction=0.5
    restitution=0
    mass=0.01
elif model_name=="Trilobe":
    op1=2.5
    op2=0.9
    op3=2.2
    sepmul_mult=10
    friction=0.325
    restitution=0.85
    mass=0.2
else: #Which means, for now, Spheres
    op1=1
    op2=0.9
    op3=1
    sepmul_mult=1
    friction=0.5
    restitution=0
    mass=0.05

############### CONTAINER CREATION ###############
start_height=6 #as a multiple of sepmul, look a few lines below
if str_container=="Box":
    box_create(bl_side)
    num_in_plane, plane_pos=get_plane_pos(sepmul,bl_side,"Box",op1,op2,op3)
    height=sepmul #place first grains at sepmul blender above the bottom of the box
if str_container=="Cylinder":
    cylinder_create(bl_cyl_diameter,bl_cyl_height)
    num_in_plane, plane_pos=get_plane_pos(sepmul,bl_cyl_diameter,"Cyl",op1,op2,op3)
    height=sepmul*start_height #place first grains at sepmul blender above the bottom of the cylinder
############### CONTAINER CREATION END ###############

#################### SPHERE PLACEMENT ####################

num_particles=0
num_count=0
if primitive==1:
    while (True):
        if (grain_list==[]):
            break
        else:
            #Choose one random grain from the 1D list, which means picking a diameter.
            posit=random.randint(0,(len(grain_list)-1))
            choice_size=grain_list[posit]
            #Get a position on the layer.
            x_pos=plane_pos[num_count][0]+(random.random()-0.5)*choice_size*0.1
            y_pos=plane_pos[num_count][1]+(random.random()-0.5)*choice_size*0.1
            #Add the icosphere
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=refine_level, size=(choice_size/2), location=(x_pos, y_pos, height), rotation=(0, 0, 0))
            bpy.ops.rigidbody.object_add(type='ACTIVE')
            bpy.context.object.game.physics_type = 'RIGID_BODY'
            new_radius=(choice_size/2.0)
            bpy.context.active_object.rigid_body.mass=mass_0*new_radius*new_radius*new_radius
            bpy.context.active_object.rigid_body.friction=friction
            bpy.context.active_object.rigid_body.restitution=restitution
            bpy.context.object.rigid_body.use_deactivation = True
            #When you'll have put num_count particles on a "layer" equal to num_in_plane, go to next layer
            num_count=num_count+1
            if (num_count==num_in_plane):
                num_count=0
                height=height+sepmul
            #Remove the grain just positioned from the 1D list
            grain_list.pop(posit)
            #Console book-keeping and status
            print(str(len(grain_list))+" grains remaining")
    deselect_all()

#################### SPHERE PLACEMENT END ################

#################### MODEL PLACEMENT #################### 
else:
    while (True):
        if (grain_list==[]):
            break
        else:
            num_particles=num_particles+1
            #Choose one random grain from the 1D list, which means picking a diameter.
            posit=random.randint(0,(len(grain_list)-1))
            choice_size=grain_list[posit]
            #Get a position on the layer.
            x_pos=plane_pos[num_count][0]+(random.random()-0.5)*choice_size*0.1
            y_pos=plane_pos[num_count][1]+(random.random()-0.5)*choice_size*0.1
            deselect_all()
            #Select original model
            bpy.data.objects[model_name].select=True
            #Duplicate it
            bpy.ops.object.duplicate_move()
            #The object is selected
            selection = bpy.context.selected_objects
            for obj in selection: 
                bpy.context.scene.objects.active = obj
                bpy.ops.rigidbody.object_add(type='ACTIVE')
                bpy.context.object.game.physics_type = 'RIGID_BODY'
            #Move it to the specified place/height
                bpy.ops.transform.translate(value=(x_pos,y_pos,height+10))
                bpy.context.active_object.rigid_body.friction=friction
                bpy.context.active_object.rigid_body.restitution=restitution
                obj.scale[2]=(choice_size/2)
                new_radius=obj.scale[2]
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                bpy.ops.transform.rotate(value=random.randint(-2,2), axis=(1.0, 1.0, 0.5))
                obj.rigid_body.mass=mass_0*new_radius*new_radius*new_radius
                bpy.context.object.rigid_body.use_deactivation = True
            #bpy.context.object.rigid_body.use_start_deactivated = True
            #When you'll have put num_count particles on a "layer" equal to num_in_plane, go to next layer
            num_count=num_count+1
            if (num_count==num_in_plane):
                num_count=0
                height=height+sepmul*sepmul_mult
            grain_list.pop(posit)
            print(str(len(grain_list))+" grains to place remaining")
    deselect_all()
    #Now that every model is placed, let's remove the original one
    bpy.data.objects[model_name].select=True #Select original model
    bpy.ops.object.delete()
    deselect_all()
    
####################MODEL PLACEMENT END####################


####################BLENDER ANIMATION SETTINGS####################
bpy.context.scene.frame_end = max_frame
bpy.data.scenes['Scene'].rigidbody_world.point_cache.frame_end= max_frame
####################BLENDER ANIMATION SETTINGS END####################

####################COMMAND LINE AUTOMATION####################
#bpy.ops.screen.animation_play()
bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//")+"b1-start")
cnt=1
print('Max frame is: '+str(max_frame))
#while (bpy.context.scene.frame_current<=150):
while (cnt<=bpy.context.scene.frame_end):
    bpy.context.scene.frame_set(cnt)
    bpy.data.scenes["Scene"].frame_current=cnt
    cnt=cnt+1
    print('Current frame is '+str(cnt)+' of '+str(max_frame))
	
bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//")+"b2-endSimulation")
####################COMMAND LINE AUTOMATION END####################

#################### EXPORT
deselect_all()
bpy.data.objects['Camera'].select=True
bpy.ops.object.delete(use_global=True)
bpy.data.objects['Lamp'].select=True
bpy.ops.object.delete()

# TODO: This next 5 deletes are only useful for cube boxes, what about cylinders?
if str_container=="Box":
    bpy.data.objects['MaxX'].select=True
    bpy.ops.object.delete()
    bpy.data.objects['MinX'].select=True
    bpy.ops.object.delete()
    bpy.data.objects['MaxY'].select=True
    bpy.ops.object.delete()
    bpy.data.objects['MinY'].select=True
    bpy.ops.object.delete()
    bpy.data.objects['MinZ'].select=True
    bpy.ops.object.delete()
elif str_container=="Cylinder":
    #Here is the Cylinder (which is the container)
    bpy.data.objects['Cylinder'].select=True
    bpy.ops.object.delete()
else:
    print("No container?")
#Deletion of tablemats
bpy.ops.object.select_pattern(pattern="Tablemat*")
bpy.ops.object.delete()
# bpy.data.objects['Tablemat'].select=True
# bpy.ops.object.delete()

bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//")+"b3-forExport")
select_all()
bpy.ops.export_mesh.stl(filepath=bpy.path.abspath("//")+"merged.stl")
#################### EXPORT END
