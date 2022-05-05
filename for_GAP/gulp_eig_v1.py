import os, sys
import time
import subprocess
import re
import shutil
import numpy as np
from colored import fg, bg, attr

'''
0.0v : Testing version (fully working) - need to be modulised

1.0v (upcoming) : composed of classes and function - fully modulised
'''


'''
Run this code at the parent directory of 'top_structures'

1. It will generate 'gulp_eig' directory where IP calculation will be placed

2. Generating n number of directories and run IP calculation using the gulp code
    2.1. keywords are [ opti conp conj prop eigenvectors ]
    2.2. the gulp will generate output file with optimised structure, xyz file

3. call the eigenvectors and format it as arrays (3n degrees of freedom: 3n-6)

4. Sum optimised cartesian coordiate and {lambda}*eigenvector and 
    generate ?? number of xyz file 

    4.1. generate {movie.xyz} file that contains all xyz file 
    (all xyz is concatedated in the file)

'''



def get_files(path, ext):
    
    files = [ x for x in os.listdir(path) if ext in x ]
    files = [ (path + x) for x in files ]
    files.sort()
    return files

FROM = int(sys.argv[1]) #int(input("[From] which order of frequency would you like to take? : "))

if FROM == 0:
    pass
else:
    TO = int(sys.argv[2]) #int(input("[To] which order of frequency would you like to take? : ")) + 1


if FROM > 6:
    print()
    raise Exception("[!!WARNING!!] Sorry, there is only [6] total of frequency order\n")
else:
    pass


# Measure the runtime
start = time.process_time()

target = os.getcwd()
dir_top_structures = target + '/top_structures/'
files = get_files(dir_top_structures, '.xyz')

if 'gulp_eig' in os.listdir('./'):
    shutil.rmtree('gulp_eig')
    os.mkdir('gulp_eig')
else:
    os.mkdir('gulp_eig')



os.chdir('./gulp_eig')

gulp_error = []
caution_scaling = []
for x in files:
    cation = []
    anion_core = []
    anion_shel = []
    
    '''
    Prepare gulp.gin
    '''
    # read data 
    with open(x, 'r') as coord:
        for i, line in enumerate(coord):
            if i > 1:
                if 'Al' in line:
                    c = line.replace('Al   ', 'Al  core')
                    cation.append(c)
                    
                if 'F' in line:
                    a_core = line.replace('F   ', 'F   core')
                    a_shel = line.replace('F   ', 'F   shel')
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

    dest = x.split('/')[-1]
    dest = dest.split('.')[0]

    os.mkdir(dest)


    '''
    write gulp.gin
    '''
    with open(dest + '/gulp.gin', 'w') as f:
        f.write('opti conp conj prop eigenvectors\ncartesian\n')
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
output xyz {dest}_eig')             

    os.chdir(dest)                                                      ####
    
    subprocess.check_output(["gulp", "gulp"])                           # excute gulp

    gulp_output = os.path.join(target, 'gulp_eig', dest, 'gulp.gout')
   
    '''
    grep data 
    '''
    with open(gulp_output, 'r') as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
      
        From = []
        To = []
        Formula = []
        for numi, i in enumerate(lines):
            if 'Job Finished' in i:
                print(f'{fg(5)} {bg(15)} {dest} is DONE {attr(0)}')
            
            #if 'Formula =' in i:
            #    stoi = (re.findall('(\d+)', i))
            #    no_of_atoms = sum([int(x) for x in stoi])
                
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
        if FROM == 0:
            TO = deg_of_freedom
            freq = list(range(FROM, TO)) 
        freq = list(range(FROM, TO))

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
         
    '''
    editing gulp output xyz file with eigvector and generate xyz movie file
    '''
    gulp_new_xyz = f'{dest}_eig.xyz' 
    with open(gulp_new_xyz, 'r') as f:
        lines = f.readlines()[2:]
        
        coord = [x.split() for x in lines] 
        array = np.asarray(coord)           #[:, 1:]
        coord = array[:, 1:].astype(float)
        ID = array[:, 0].astype(str)
       
        for numi, i in enumerate(range(len(freq))):
            os.mkdir(str(freq[i]))
            print()
            print(f'A + [{numi+1} eigenvec]')
            for j in range(-100, 100, 1):

                mod_eigvec_array = eigvec_array[i] * (int(j)/1000)
                new_coord = coord + mod_eigvec_array 
                new_coord = np.around((new_coord), decimals = 9)
                 
                stack = np.c_[ID, new_coord]
                stack = stack.tolist()
                
                with open(f'{freq[i]}/{str(j)}.xyz', 'w') as f:
                    f.write(str(no_of_atoms) + '\n')
                    f.write(total_energy + '\n')

                with open(f'{freq[i]}/movie.xyz', 'a') as f:
                    f.write(str(no_of_atoms) + '\n')
                    f.write(total_energy + '\n')

                for k in stack:
                    new = '\t\t'.join(k) + '\n'
                   
                    with open(f'{freq[i]}/{str(j)}.xyz', 'a') as f: 
                        f.write(new)

                    with open(f'{freq[i]}/movie.xyz', 'a') as f:
                        f.write(new) 
                
            print() 
    print()

    os.chdir('../')                                                     ####

print(f"{fg(19)} {bg(15)} ##### JOB DONE ##### {attr(0)}\n")

collection = os.listdir('./')
collection.sort()

print(f"----- process time : {int((time.process_time() - start)/60)} mins {(time.process_time() - start) % 60} seconds, -----")



