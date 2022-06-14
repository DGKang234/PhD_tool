import os, sys
import time
import subprocess
import re
import shutil
import operator
import math
import numpy as np
from colored import fg, bg, attr



class AIMS:
    def __init__(self):
        self.job_sub_V = 'trash.sh'

    def get_list(self, path):
        lists = [os.path.join(path, x) for x in os.listdir(path)]
        lists.sort()
        return lists

    def Prepare_con_sub_files(self, FINAL_PATH_FULL, MOD_XYZ_LABEL):
        control = 'control.in' #'control.in.single'
        job_sub = 'trash_1.sh'
       
        storage = '/home/uccatka/auto/aims_auto/copy_this_for_new/'

        shutil.copy(storage + control, FINAL_PATH_FULL + '/control.in')
        shutil.copy(storage + job_sub, FINAL_PATH_FULL)
        
        #
        # Preparing job submission file        
        #
        with open(f'{FINAL_PATH_FULL}/{job_sub}', 'r') as f:
            edit = f.read().replace("target_1", FINAL_PATH_FULL)
            edit = edit.replace("target_2", MOD_XYZ_LABEL) 
            with open(f'{FINAL_PATH_FULL}/{self.job_sub_V}', 'w') as f:
                f.write(edit)
       
        os.remove(f'{FINAL_PATH_FULL}/{job_sub}')
        
        return None 
   
   
    
    def xyz_to_Geometry(self, FINAL_PATH_FULL, xyz):
        #xyz = [FINAL_PATH_FULL + '/' + x for x in os.listdir(FINAL_PATH_FULL) if '.xyz' in x]
        
        with open(xyz, 'r') as f:
            lines = f.readlines()
            del lines[0]
            del lines[0]

            coord = [x.split() for x in lines]
            atom = [x[0] for x in coord]
            coord = [x[1:] for x in coord]

            for numi, i in enumerate(coord):
                i.append(atom[numi])
                i.insert(0, 'atom')
                edit = ' '.join(i)
                
                with open(FINAL_PATH_FULL + '/geometry.in', 'a') as f:
                    f.write(edit)
                    f.write('\n')
        return None

   
    
    def Aims_submit(self, FINAL_PATH_FULL):
        command = f'qsub {FINAL_PATH_FULL}/{self.job_sub_V}'
        print(command)
        os.system(command)
        return None



    def Aims_grep_data(self, FINAL_PATH_FULL):
        with open(f'{FINAL_PATH_FULL}/aims.out', 'r') as f:
            lines = f.readlines()

            no_of_atoms = 0
            marker_F = {}
            marker_C = {}
            FORCES = []
            CART = []
            ATOM = []
            AIMS_ENERGY = []
            AIMS_FINAL_ENERGY = []
            for numi, i in enumerate(lines):
                if '| Number of atoms                   :' in i:
                    no_of_atoms += int(i.split()[-1])

                if '| Total energy                  :' in i:
                    AIMS_ENERGY.append(i.split()[-2])
                 
                if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation' in i:
                    AIMS_FINAL_ENERGY.append(i.split()[11])

                if 'Total atomic forces (unitary forces cleaned)' in i:
                    marker_F[numi+1] = numi + no_of_atoms + 1

                if 'Updated atomic structure:' in i:
                    marker_C[numi+2] = numi + no_of_atoms + 2 

            
            ## sort in reverse order to get optimised data
            marker_C = dict(sorted(marker_C.items(), key=operator.itemgetter(1), reverse=True))
            for k, v in marker_C.items():
                cart = []
                atom = []
                for numj, j in enumerate(lines):
                    if numj in range(k, v):
                        cart.append(j.split()[1:-1])
                        atom.append(j.split()[-1])
                 
                CART.append(np.asarray(cart)) #.astype(float))
                ATOM.append(np.asarray(atom))
            
            marker_F = dict(sorted(marker_F.items(), key=operator.itemgetter(1), reverse=True))
            for k, v in marker_F.items():
                force = []
                for numj, j in enumerate(lines):
                    if numj in range(k, v):
                        force.append(j.split()[2:])
                FORCES.append(np.asarray(force).astype(float))

        FORCES = np.asarray(FORCES).astype(float)
        FORCES = np.round_(FORCES, decimals=8)
        CART = np.asarray(CART) #.astype(float)
        ATOM = np.asarray(ATOM)
        
        return AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, no_of_atoms 



    def Aims_extended_xyz(self, FINAL_PATH_FULL, AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, no_of_atoms):
        for numi, i in enumerate(CART):
            coord = i
            atom_coord = np.c_[ATOM[numi], coord]
            atom_coord_force = np.c_[atom_coord, FORCES[numi]] 
            atom_coord_force = atom_coord_force.tolist()            
 
            ext_xyz = os.path.join(FINAL_PATH_FULL, 'aims_ext.xyz')

            with open(ext_xyz, 'a') as f:
                f.write(str(no_of_atoms))
                f.write('\n')
                f.write(f'Lattice="0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0" Properties=species:S:1:pos:R:3:forces:R:3 energy={AIMS_ENERGY[numi]} pbc="F F F"')
                f.write('\n')
                for i in atom_coord_force:
                    new = [str(x) for x in i]
                    new = '\t\t'.join(new) + '\n'
                    f.write(new)

            with open('the_ext_movie.xyz', 'a') as f:
                f.write(str(no_of_atoms))
                f.write('\n')
                f.write(f'Lattice="0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0" Properties=species:S:1:pos:R:3:forces:R:3 energy={AIMS_ENERGY[numi]} pbc="F F F"')
                f.write('\n')
                for i in atom_coord_force:
                    new = [str(x) for x in i]
                    new = '\t\t'.join(new) + '\n'
                    f.write(new)

        return None



    def Aims_GAP_FIT(self):
        with open('the_ext_movie.xyz', 'r') as f:
            lines = f.readlines()
        
        From = []
        To = []
        d = {}
        for numi, i in enumerate(lines):
            if len(i) <=5:
                From.append(numi)
                To.append(numi)

        To.append(len(lines))
        To = To[1:]

        block = {From[i]: To[i] for i in range(len(From))}
        even_block_key = []
        odd_block_key = []
        for numi, i in enumerate(block):
            if (numi+1) % 2 == 0:
                even_block_key.append(i)
            else:
                odd_block_key.append(i)

        FIT_path = os.path.join(os.getcwd(), 'FIT')
        os.mkdir(FIT_path)
        
        Training_xyz_path = os.path.join(FIT_path, 'Training_set.xyz')
        Validation_xyz_path = os.path.join(FIT_path, 'Validation_set.xyz')

        with open(Training_xyz_path, 'a') as f:
            for numi, i in enumerate(lines):
                for j in odd_block_key:
                    if j <= numi < block[j]:
                        f.write(i)
        
        with open(Validation_xyz_path, 'a') as f:
            for numi, i in enumerate(lines):
                for j in even_block_key:
                    if j <= numi < block[j]:
                        f.write(i)

        with open('/home/uccatka/auto/for_GAP/Al_atom/aims.out', 'r') as f:
            lines = f.readlines()
        for i in lines:
            if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation' in i: 
                Al_AIMS_FINAL_ENERGY = i.split()[-2] 
        
        with open('/home/uccatka/auto/for_GAP/F_atom/aims.out', 'r') as f:
            lines = f.readlines()
        for i in lines:
            if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation' in i:
                F_AIMS_FINAL_ENERGY = i.split()[-2]

        with open(Training_xyz_path, 'a') as f:
            f.write('1')
            f.write('\n')
            f.write(f'Lattice="0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0" Properties=species:S:1:pos:R:3:forces:R:3 energy={Al_AIMS_FINAL_ENERGY} pbc="F F F')   
            f.write('\n')
            f.write('Al 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000')
            f.write('\n')

        with open(Training_xyz_path, 'a') as f:
            f.write('1')
            f.write('\n')
            f.write(f'Lattice="0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0" Properties=species:S:1:pos:R:3:forces:R:3 energy={F_AIMS_FINAL_ENERGY} pbc="F F F')
            f.write('\n')
            f.write('F 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000')

        print("##############################")
        print("# Proceeding the GAP fitting #")
        print("##############################")
        print()
        
        path = os.path.join(os.getcwd(), 'FIT')
        print(path) 
        
        
        os.system('gap_fit \
energy_parameter_name=energy \
force_parameter_name=forces \
do_copy_at_file=F \
sparse_separate_file=T \
gp_file=%s/GAP.xml \
at_file=%s/Training_set.xyz \
default_sigma={0.008 0.04 0 0} \
gap={distance_2b \
cutoff=4.0 \
covariance_type=ard_se \
delta=0.5 \
theta_uniform=1.0 \
sparse_method=uniform \
add_species=T \
n_sparse=10}' %  (path, path))
        
#        os.system('gap_fit at_file=%s/Training_set.xyz \
#gap={distance_Nb order=2 \
#                 cutoff=5.0 \
#                 covariance_type=ARD_SE \
#                 theta_uniform=1.0 \
#                 n_sparse=15 \
#                 delta=1.0:\
#     distance_Nb order=3 \
#                 cutoff=4.0 \
#                 covariance_type=ARD_SE \
#                 theta_uniform=1.0 \
#                 n_sparse=50 \
#                 delta=0.004} \
#default_sigma={0.005 0.5 0.0 0.0} \
#do_copy_at_file=F sparse_separate_file=F \
#gp_file=%s/GAP.xml' % (path, path))
        
        print(os.getcwd())
        print("##############################")
        print("The GAP fitting has finished")
        print("##############################")
        
        os.system(f"quip E=T F=T atoms_filename={path}/Training_set.xyz param_filename={path}/GAP.xml | grep AT | sed 's/AT//' > ./FIT/quip_train.xyz")
        os.system(f"quip E=T F=T atoms_filename={path}/Validation_set.xyz param_filename={path}/GAP.xml | grep AT | sed 's/AT//' > ./FIT/quip_validate.xyz")
        
        
        import matplotlib.pyplot as plt
        # ase API
        import ase.io
        from ase import Atoms, Atom
        # quippy API
        from quippy.potential import Potential
        from quippy.descriptors import Descriptor
        
        dimers = [Atoms("AlF", positions=[[0,0,0], [x, 0,0]]) for x in np.linspace(1.0,4.5,100)]
        pot = Potential(param_filename='./FIT/GAP.xml')
        dimer_curve = []
        for dim in dimers:
            dim.set_calculator(pot)
            dimer_curve.append(dim.get_potential_energy())
        plt.plot([dim.positions[1,0] for dim in dimers], np.array(dimer_curve)/2.0)
        plt.savefig("./FIT/AlF_interaction")



        """
        geo_file = 'geometry.in'
        with open(f'{FINAL_PATH_FULL}/{geo_file}', 'r') as f:
            lines = f.readlines()
        
        full = [x.split() for x in lines]
        full = np.asarray(full)
        coord = full[:, 1:-1].astype(float)
        atom = full[:, -1].astype(str)
       
        ext_xyz = os.path.join(FINAL_PATH_FULL, 'aims_mod.xyz')

        coord_and_force = np.c_[atom, coord, FORCES]
        coord_and_force = coord_and_force.tolist()

        gulp = FINAL_PATH_FULL + '/' +  FINAL_PATH_FULL.split('/')[-1] + '_eig.xyz'
        with open(gulp, 'r') as f:
            lines = f.readlines()
            TOTAL_ENERGY = str(lines[1].split()[2])
       
        with open(ext_xyz, 'w') as f:
            f.write(str(no_of_atoms))
            f.write('\n')
            #f.write(TOTAL_ENERGY)
            f.write(f'Properties=species:S:1:pos:R:3:forces:R:3 energy={AIMS_ENERGY[0]} pbc="F F F"')
            f.write('\n')
            for i in coord_and_force:
                new = [str(x) for x in i]
                new = '\t\t'.join(new) + '\n' 
                f.write(new) 


        with open('ext_movie.xyz', 'a') as f:
            f.write(str(no_of_atoms))
            f.write('\n')
            #f.write(TOTAL_ENERGY)
            f.write(f'Properties=species:S:1:pos:R:3:forces:R:3 energy={AIMS_ENERGY[0]} pbc="F F F"')
            f.write('\n')
            for i in coord_and_force:
                new = [str(x) for x in i]
                new = '\t\t'.join(new) + '\n'
                f.write(new)


        return None 
        """















