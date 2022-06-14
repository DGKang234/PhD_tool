import numpy as np
import os, sys
import shutil


cat = 'Al'
an = 'F  '

def file_len(fname):
    with open(fname) as f:
        f = f.readlines()
            
    return len(f) 

cwd = os.getcwd()
parent = os.path.join(cwd, 'gap_pre')
ext_fpath = os.path.join(parent, 'ext_movie.xyz')

flength = file_len(ext_fpath)

From = []
To = []
d = {}
with open(ext_fpath, 'r') as f:
    lines = f.readlines()
        
for numi, i in enumerate(lines):
    if len(i) <= 5:
        From.append(numi)
        To.append(numi)

#From = From[1:]
#From.insert(0, 0)
To.append(len(lines))
To = To[1:]
#mod =  To[0]-1
#To = To[1:]
#To.insert(0, mod)
#print(From)
#print(To)
#print()

block = {From[i]: To[i] for i in range(len(From))}        

even_block_key = []
odd_block_key = []
for numi, i in enumerate(block):
    if (numi+1) % 2 == 0:
        even_block_key.append(i) 
    else:
        odd_block_key.append(i)

FIT_path = os.path.join(parent, 'FIT')
os.mkdir(FIT_path)

Training_xyz_path = os.path.join(FIT_path, 'Training_set.xyz')
Valid_xyz_path = os.path.join(FIT_path, 'Valid_set.xyz')


#
#   need to be modified to randomly choose 10~80% of data for training and valid 
#   but for now 50 : 50 distributed
#
with open(Training_xyz_path, 'a') as f:
    for numi, i in enumerate(lines):
        for j in odd_block_key:
            if j <= numi < block[j]:
                f.write(i)

with open(Valid_xyz_path, 'a') as f:
    for numi, i in enumerate(lines):
        for j in even_block_key:
            if j <= numi < block[j]:
                f.write(i)


# Add single atoms
with open(Training_xyz_path, 'a') as f:
    f.write('1\n')
    f.write(f'Lattice="0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0" Properties=species:S:1:pos:R:3:forces:R:3 energy=0.000000000000 free_energy=-13.975817 pbc="F F F"\n')
    f.write('Al 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000\n')
    f.write('1\n')
    f.write(f'Lattice="0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0" Properties=species:S:1:pos:R:3:forces:R:3 energy=0.000000000000 free_energy=-5.735796 pbc="F F F"\n')
    f.write('F 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000\n')




print("##############################")
print("# Proceeding the GAP fitting #")
print("##############################")
print()

os.system('gap_fit energy_parameter_name=energy force_parameter_name=forces do_copy_at_file=F sparse_separate_file=T gp_file=./gap_pre/FIT/GAP.xml at_file=./gap_pre/FIT/Training_set.xyz default_sigma={0.008 0.04 0 0} gap={distance_2b cutoff=4.0 covariance_type=ard_se delta=0.5 theta_uniform=1.0 sparse_method=uniform add_species=T n_sparse=10}')

print()
print("The GAP fitting has finished")
print()

os.system("quip E=T F=T atoms_filename=./gap_pre/FIT/Training_set.xyz param_filename=./gap_pre/FIT/GAP.xml | grep AT | sed 's/AT//' > ./gap_pre/FIT/quip_train.xyz")
os.system("quip E=T F=T atoms_filename=./gap_pre/FIT/Valid_set.xyz param_filename=./gap_pre/FIT/GAP.xml | grep AT | sed 's/AT//' > ./gap_pre/FIT/quip_validate.xyz")


import matplotlib.pyplot as plt
# ase API
import ase.io
from ase import Atoms, Atom
# quippy API
from quippy.potential import Potential
from quippy.descriptors import Descriptor

dimers = [Atoms("AlF", positions=[[0,0,0], [x, 0,0]]) for x in np.linspace(0.0,4.5,100)]
pot = Potential(param_filename='./gap_pre/FIT/GAP.xml')
dimer_curve = []
for dim in dimers:
    dim.set_calculator(pot)
    dimer_curve.append(dim.get_potential_energy())
plt.plot([dim.positions[1,0] for dim in dimers], np.array(dimer_curve)/2.0)
plt.savefig("./gap_pre/FIT/AlF_interaction")






