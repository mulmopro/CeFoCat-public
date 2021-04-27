import re
import subprocess as sb

with open('log.checkMeshMacro','r') as f:
    log = f.readlines()

target1 = 'Number of regions: '
target2 = '(OK).\n'

for line in log:
    if target1 in line:
        if target2 in line:
            n_reg = int(re.split( 'Number of regions: |\(OK\).\n', line)[-2])
        else:
            n_reg = int(re.split( 'Number of regions: |\n',line)[-2])

if n_reg > 1:
    print('Number of regions > 1')
    proc = sb.run(["splitMeshRegions", "-largestOnly","-overwrite"], capture_output=True, text=True)
    print(proc.stdout)
    print(proc.stderr)
    with open('log.splitMeshRegion','w') as f:
        f.write(proc.stdout)
        f.write('\n')
        f.write(proc.stderr)
    with open('log.checkMeshMacro', 'w+') as f:
        check = sb.run(['checkMesh'], text=True, stdout=f, stderr= sb.STDOUT)
else:
    print('Only one partition!')
