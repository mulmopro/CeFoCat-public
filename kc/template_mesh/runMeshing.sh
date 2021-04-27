source /opt/openfoam7/etc/bashrc
l='ls -CF'
# #### create planes function Object
# python funcObj_setup.py

# ##### blockMesh 
blockMesh | tee log.blockMesh 2>&1

echo 'get .stl file name'
echo "stl \"$($l ./constant/triSurface/)\";" > stl_name

# ##### snappyhexMesh
echo 'snappyHexMesh running...'
snappyHexMesh -overwrite | tee log.snappyHexMesh 2>&1
