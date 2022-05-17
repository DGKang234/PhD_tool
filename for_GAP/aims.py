import os, sys
import time
import subprocess
import re
import shutil
import numpy as np
from colored import fg, bg, attr



class AIMS:
    def __init__(self):
        self.job_sub_V = 'trash.sh'

    def Prepare_con_sub_files(self, FINAL_PATH_FULL, MOD_XYZ_LABEL):
        control = 'control.in.single'
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
   
   
    
    def xyz_to_Geometry(self, FINAL_PATH_FULL):
        xyz = [FINAL_PATH_FULL + '/' + x for x in os.listdir(FINAL_PATH_FULL) if '.xyz' in x]
        with open(xyz[0], 'r') as f:
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
        print()
        print(command)
        print()
        os.system(command)
        return None



    def Aims_grep_data(self, FINAL_PATH_FULL):
        forces = [] 
        with open(f'{FINAL_PATH_FULL}/aims.out', 'r') as f:
            lines = f.readlines()

            no_of_atoms = 0
            marker = []
            AIMS_ENERGY = []
            for numi, i in enumerate(lines):
                if '| Number of atoms                   :' in i:
                    no_of_atoms += int(i.split()[-1])

                if 'Total atomic forces (unitary forces cleaned)' in i:
                    marker.append(numi + 1)
                    marker.append(numi + no_of_atoms + 1) 
                if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation' in i:
                    AIMS_ENERGY.append(i.split()[11])
                    
            for numj, j in enumerate(lines):
                if numj in range(marker[0], marker[1]):
                    force = [float(x) for x in j.split()[2:]]
                    forces.append(force)
       
        FORCES = np.asarray(forces)
        
        return AIMS_ENERGY, FORCES, no_of_atoms       # array



    def Aims_extended_xyz(self, FINAL_PATH_FULL, no_of_atoms, FORCES, AIMS_ENERGY):
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
















