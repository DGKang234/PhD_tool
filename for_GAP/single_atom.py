# general imports
import os
import aims as AIMS
import subprocess

Al_dir = 'Al_atom'
os.mkdir(Al_dir)
os.chdir(Al_dir)
AIMS = AIMS.AIMS()

cwd = os.getcwd()
AIMS.Prepare_con_sub_files(cwd, 'Al')
with open('geometry.in', 'w') as f:
    f.write('atom 0.0000  0.0000  0.0000 Al')
#subprocess.check_output(["qsub", "trash.in"])
#os.system(f"qsub {Al_dir}/trash.in")
os.chdir('../')




F_dir = 'F_atom'
os.mkdir(F_dir)
os.chdir(F_dir)
cwd = os.getcwd()
AIMS.Prepare_con_sub_files(cwd, 'F')
with open('geometry.in', 'w') as f:
    f.write('atom 0.0000 0.0000 0.0000 F')
#subprocess.check_output(["qsub", "trash.in"])
#os.system(f"qsub {F_dir}/trash.in")

