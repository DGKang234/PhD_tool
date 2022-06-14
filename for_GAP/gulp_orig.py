import os, sys
import time
import subprocess
import re
import shutil
import numpy as np
from colored import fg, bg, attr



class GULP:
    def __init__(self, STEP, FROM, TO, SP):
        self.FROM = FROM
        self.TO = TO 
        self.STEP = STEP  
        self.SP = SP

    def trunc(values, decs=0):
        return np.trunc(values*10**decs)/(10**decs)    
    
    
    def Get_file_list(self, path, ext='.xyz'):
        files = [x for x in os.listdir(path) if ext in x]
        files = [(path + '/' + x) for x in files]
        files.sort()
        return files

   
       
    def Label_top_str(self, xyz):
        return xyz.split('-')[1].split('.xyz')[0]
     


    def Re_top_str(self, TOP_structures='top_structures', Extension='.xyz'):
        cwd = os.getcwd()
        path = f'{cwd}/{TOP_structures}/'
         
        xyz_orig = [x for x in os.listdir(path) if Extension in x]
        xyz_orig_ordered = sorted(xyz_orig, key=self.Label_top_str)
        
        Max = xyz_orig_ordered[-1]
        Max_len = len(Max)
    
        change = []
        for xyz in xyz_orig_ordered:
            label = str(self.Label_top_str(xyz)) 
            
            if Max_len == 4:
                if len(str(label)) == 1:
                    label = '000' + label
                elif len(str(label)) == 2:
                    a = '00' + label
                elif len(str(label)) == 3:
                    a = '0' + label

            if Max_len == 3:
                if len(str(label)) == 1:
                    a = '00' + label
                elif len(str(label)) == 2:
                    a = '0' + label

            if Max_len == 2:
                if len(str(label)) == 1:
                    a = '0' + label

            rank_xyz = xyz.split('-')[1]
            rank = rank_xyz.replace('.xyz', '')

            rename = str(label) + '.xyz'
            change.append(rename)                    
        
            os.rename(path + '/' + xyz, path + '/' + rename)



    def Convert_xyz_Gulp(self, f):
        cation = []
        anion_core = []
        anion_shel = []
        
        with open(f, 'r') as coord:
            for i, line in enumerate(coord):
                if i > 1:
                    if 'Al' in line:
                        c = line.replace('Al', 'Al  core')
                        cation.append(c)
                    
                    if 'F' in line:
                        a_core = line.replace('F', 'F   core')
                        a_shel = line.replace('F', 'F   shel')
                        anion_core.append(a_core)
                        anion_shel.append(a_shel)

        no_of_anion = len(anion_core)
        anion_core = ''.join(anion_core)
        anion_core = anion_core.split('\n')
        anion_core = '\n'.join(anion_core)

        anion_shel = ''.join(anion_shel)
        anion_shel = anion_shel.split('\n')
        anion_shel = '\n'.join(anion_shel)

        no_of_cation = len(cation)
        cation = ''.join(cation)
        cation = cation.split('\n')
        cation = '\n'.join(cation)

        no_of_atoms = no_of_anion + no_of_cation

        dest = f.split('/')[-1]
        dest = dest.split('.')[0]

        return cation, anion_core, anion_shel, dest, no_of_atoms



    def Write_Gulp(self, path, outXYZ, cation, anion_core, anion_shel, SP):
        if SP == 'y':
            keywords = 'opti shel conp eigenvectors'
        else:
            keywords = 'opti conp conj prop eigenvectors'

        with open(path + '/gulp.gin', 'w') as f:
            f.write(f'{keywords}\ncartesian\n')
            f.write(cation)
            f.write(anion_core)
            f.write(anion_shel)
            f.write(
            f'species\n\
Al core 3.00\n\
F  core 0.59\n\
F  shel -1.59\n\
buck\n\
Al  core  F   shel  3760.000831  0.222000   0.00000 0.0 10.0\n\
buck4\nF   shel  F   shel  1127.7 0.2753 15.83 2.0 2.79 3.031 12.0\n\
spring\nF     20.77\n\
xtol opt 6.000\n\
ftol opt 5.000\n\
gtol opt 8.000\n\
switch_min rfo gnorm 0.01\n\
maxcyc 2000\n\n\
output xyz {outXYZ}_eig\n')
            if SP == 'y':
                f.write(f'output drv {outXYZ}_F_out')




    def Run_Gulp(self, path_of_gulp, dest):
        subprocess.check_output(['/home/uccatka/software/gulp-5.1/Src/gulp', f'{dest}/gulp'])
        gulp_output_path = os.path.join(path_of_gulp, 'gulp.gout')            
        return gulp_output_path
    


    def Grep_Data(self, gulp_output_path, no_of_atoms, dest, SP):
        #                      #
        # From the [gulp.gout] #
        #                      #
        with open(gulp_output_path, 'r') as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]

            From = []
            To = []
            Formula = []
            for numi, i in enumerate(lines):
                if 'Job Finished' in i:
                    print(f'{fg(5)} {bg(15)} {dest} is DONE {attr(0)}')

                if 'Final energy =  ' in i:
                    total_energy = i.split()[3]
        
                if 'Frequency   ' in i:
                    From.append(numi+7)
                    To.append(numi-3)
        
                if 'Vibrational properties (for cluster)' in i:
                    To.append(numi-6)
            To = To[1:]

            #                       #
            # Retrieve eigenvectors #
            #                       #
            deg_of_freedom = len(From)
            if self.FROM == 100:
                self.FROM = 0
                self.TO = deg_of_freedom
                freq = list(range(self.FROM, self.TO))
               
            freq = list(range(self.FROM, self.TO))
            
            DUMMY = []
            for numj, j in enumerate(From):
                for numk, k in enumerate(lines):
                    if From[numj] <= numk <= To[numj]:
                        eigvec = k.split()[2]
                        DUMMY.append(float(eigvec))
            DUMMY = np.asarray(DUMMY)
    
            eigvec_array = np.reshape(DUMMY, (deg_of_freedom, no_of_atoms, 3))

        #                      #
        # printing eigenvector #
        #                      #
        no_of_eigval = eigvec_array.shape[0]
        for i in range(no_of_eigval):
            print()
            print(f'# {fg(2)} {int(i)+1}th eigen vector {attr(0)}')
            print(eigvec_array[i])

        #               #
        # atomic forces #
        #               #
        force_out = [x for x in os.listdir(dest) if 'drv' in x]
        marker = []
        forces = []
        if SP == 'y':
            if os.path.isdir(dest) == True:
                
                #with open(os.path.join(dest, 'gulp.gout'), 'r') as f:
                #    lines = f.read()
                #    if 'ERROR' in lines:
                #        return ABORT == True
                #        pass
                 
                if force_out[0] in os.listdir(dest): 
                    with open(dest + '/' + force_out[0], 'r') as f:
                        lines = f.readlines()
                        for numi, i in enumerate(lines):
                            if 'gradients cartesian eV/Ang' in i:
                                marker.append(numi + 1)
                                marker.append(numi + no_of_atoms + 1)       
                        
                        for numj, j in enumerate(lines):
                            if numj in range(marker[0], marker[1]):
                                force = [float(x) for x in j.split()[1:]]
                                forces.append(force) 
                                

            FORCES_GULP = np.asarray(forces)
            FORCES_GULP = np.round(FORCES_GULP, decimals=6)
            print()
            print(f'# {fg(2)} forces on each individual atoms {attr(0)}')
            print(FORCES_GULP)
            
            return total_energy, eigvec_array, freq, FORCES_GULP
        return total_energy, eigvec_array, freq


       
    def Modifying_xyz(self, path, gulp_new_xyz, eigvec_array, freq, no_of_atoms, total_energy):
        with open(gulp_new_xyz, 'r') as f:
            lines = f.readlines()[2:]

            #print('gulp_new_xyz ########################')
            #print(gulp_new_xyz) 

            coord = [x.split() for x in lines]
            array = np.asarray(coord)
            coord = array[:, 1:].astype(float)
            ID = array[:, 0].astype(str)

            for numi, i in enumerate(range(len(freq))):
                os.mkdir(f'{path}/{str(freq[i])}')
                print()
                print(f'optimised cartesian coordinates + [{numi+1} eigenvec]')

                if self.STEP == 0:
                    mod_eigvec_array = eigvec_array[i]
                    new_coord = coord + mod_eigvec_array
                    new_coord = np.around((new_coord), decimals = 9)

                    stack = np.c_[ID, new_coord]
                    stack = stack.tolist()

                    with open(f'{path}/{freq[i]}/mod_0.xyz', 'w') as f:
                        f.write(str(no_of_atoms) + '\n')
                        f.write(total_energy + '\n')
                    with open(f'{path}/{freq[i]}/movie.xyz', 'a') as f:
                        f.write(str(no_of_atoms) + '\n')
                        f.write(total_energy + '\n')
                    for k in stack:
                        new = '\t\t'.join(k) + '\n'
                        
                        with open(f'{path}/{freq[i]}/mod_0.xyz', 'a') as f:
                            f.write(new)
                        with open(f'{path}/{freq[i]}/movie.xyz', 'a') as f:
                            f.write(new)

                else:
                    for j in range(-200, 201, self.STEP):                      # Resolution of frequency
                        mod_eigvec_array = eigvec_array[i] * (int(j)/100)
                        new_coord = coord + mod_eigvec_array
                        new_coord = np.around((new_coord), decimals = 9)

                        stack = np.c_[ID, new_coord]
                        stack = stack.tolist()

                        with open(f'{path}/{freq[i]}/mod_{str(j)}.xyz', 'w') as f:
                            f.write(str(no_of_atoms) + '\n')
                            f.write(total_energy + '\n')

                        with open(f'{path}/{freq[i]}/movie.xyz', 'a') as f:
                            f.write(str(no_of_atoms) + '\n')
                            f.write(total_energy + '\n')

                        for k in stack:
                            new = '\t\t'.join(k) + '\n'

                            with open(f'{path}/{freq[i]}/mod_{str(j)}.xyz', 'a') as f:
                                f.write(new)

                            with open(f'{path}/{freq[i]}/movie.xyz', 'a') as f:
                                f.write(new)
                    print()
        print()
        
        return None
         

    def Ext_xyz_gulp(self, FINAL_PATH_FULL, no_of_atoms, eigvec_array, FORCES, ENERGY):
        
        index = int(FINAL_PATH_FULL.split('/')[-2])
        eigvec_array = eigvec_array[index]
        drv_name = FINAL_PATH_FULL.split('/')[-1] + '_F_out.drv'
        xyz_name = FINAL_PATH_FULL.split('/')[-1] + '_eig.xyz'

        with open(f'{FINAL_PATH_FULL}/{xyz_name}', 'r') as f:
            lines = f.readlines()[2:]

        array = [x.split() for x in lines]
        array = np.asarray(array)
        coord = array[:, 1:].astype(float)
        atom = array[:, 0].astype(str)
        
        coord_and_eigvec = coord + eigvec_array
        coord_and_force = np.c_[coord_and_eigvec, FORCES]
        coord_and_force = np.round(coord_and_force, decimals=6) 
        atom_coord_and_force = np.c_[atom, coord_and_eigvec, FORCES]
        atom_coord_and_force = atom_coord_and_force.tolist()

        ext_xyz = os.path.join(FINAL_PATH_FULL, 'ext_gulp.xyz')
        with open(ext_xyz, 'a') as f:
            f.write(str(no_of_atoms))
            f.write('\n')
            f.write(f'Properties=species:S:1:pos:R:3:forces:R:3 energy={ENERGY} pbc="F F F"')
            f.write('\n')
            for i in atom_coord_and_force:
                new = [str(x) for x in i]
                new = '    '.join(new) + '\n'
                f.write(new) 

        with open('ext_movie.xyz', 'a') as f:
            f.write(str(no_of_atoms))
            f.write('\n')
            f.write(f'Properties=species:S:1:pos:R:3:forces:R:3 energy={ENERGY} pbc="F F F"')
            f.write('\n')
            for i in atom_coord_and_force:
                new = [str(x) for x in i]
                new = '    '.join(new) + '\n'
                f.write(new)
         

        return None
        


        


