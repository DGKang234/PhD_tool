import os, sys
import time
import subprocess
import re
import shutil
import numpy as np
from colored import fg, bg, attr



class GULP:
    def __init__(self, STEP, FROM, TO, SP):
        self.FROM = FROM #int(sys.argv[1]) #int(input("[From] which order of frequency would you like to take? : "))
        self.TO = TO+1 #int(sys.argv[2]) + 1 #int(input("[To] which order of frequency would you like to take? : ")) + 1       
        self.STEP = STEP  
        self.SP = SP
    
    
    
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
            keywords = 'single eigenvectors'
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
output xyz {outXYZ}_eig')



    def Run_Gulp(self, path_of_gulp, dest):
        subprocess.check_output(['gulp', f'{dest}/gulp'])
        gulp_output_path = os.path.join(path_of_gulp, 'gulp.gout')            
        return gulp_output_path
    


    def Grep_Data(self, gulp_output_path, no_of_atoms, dest):
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

            #                   #
            # degree of freedom #
            #                   #
            deg_of_freedom = len(From)
            if self.FROM == 0:
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

        #                       #
        # printing eigen vector #
        #                       #
        no_of_eigval = eigvec_array.shape[0]
        for i in range(no_of_eigval):
            print()
            print(f'# {fg(2)} {int(i)+1}th eigen vector {attr(0)}')
            print(eigvec_array[i])

        return total_energy, eigvec_array, freq


       
    def Modifying_xyz(self, path, gulp_new_xyz, eigvec_array, freq, no_of_atoms, total_energy):
        with open(gulp_new_xyz, 'r') as f:
            lines = f.readlines()[2:]
            
            coord = [x.split() for x in lines]
            array = np.asarray(coord)
            coord = array[:, 1:].astype(float)
            ID = array[:, 0].astype(str)

            for numi, i in enumerate(range(len(freq))):
                os.mkdir(f'{path}/{str(freq[i])}')
                print()
                print(f'A + [{numi+1} eigenvec]')
                for j in range(-100, 100, self.STEP):                      # Resolution of frequency

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
         


        


