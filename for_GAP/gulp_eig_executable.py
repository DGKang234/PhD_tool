import gulp_eig_v2 as gulp
import os, sys
import time
import shutil

'''
Brief explanation of what this code does:
    Calculate eigenvectors using GULP and add the eigenvectors to the cartesian 
    coordinate of optimised structure and prepare many xyz files.

HOW to execute the code:
N.B. !!! the code requires [FOUR] argument !!!
type [python gulp_eig_executable.py {[From] order of eigenvector component} {[To} order of eigenvector component} {Resolution of frequency} {[From] structure in IP rank} {[To] structure in IP rank}

# UPDATE NOTE:
    * 0.0v (29 April 2022 - 29 April 2022): Testing version (fully working) - need to be modulised
    * 1.0v (4 May - 5 May): Composed of classes and function for modulisation - fully modulised 
        (using this in this executable)

    * 1.1v (working on) : -> Allowing to select which IP rank structure to calculate        (V) Tick marked function is implemented in this code
                          -> Allowing to customise lambda ( lambda * eigenvector)           (V)
                          -> Calling potential library instead of using written potential   ( )
'''


#Run this code at the parent directory of 'top_structures'
#
#1. It will generate 'gulp_eig' directory where IP calculation will be placed
#
#2. Generating n number of directories and run IP calculation using the gulp code
#    2.1. keywords are [ opti conp conj prop eigenvectors ]
#    2.2. the gulp will generate output file with optimised structure, xyz file
#
#3. call the eigenvectors and format it as arrays (3n degrees of freedom: 3n-6)
#
#4. Sum optimised cartesian coordiate and {lambda}*eigenvector and
#    generate 100 number of xyz file
#
#    4.1. generate {movie.xyz} file that contains all xyz file
#    (all xyz is concatedated in the file)
#
#
#N.B. This is executable code


FROM = int(sys.argv[1])
if FROM == 0:
    TO = 0
    STEP = int(sys.argv[2])
    FROM_rank = int(sys.argv[3])
    TO_rank = int(sys.argv[4])

    pass
else:
    TO = int(sys.argv[2])
    STEP = int(sys.argv[3])
    FROM_rank = int(sys.argv[4])
    TO_rank = int(sys.argv[5])


if 'gulp_eig' in os.listdir('./'):
    shutil.rmtree('gulp_eig')
    os.mkdir('gulp_eig')
else:
    os.mkdir('gulp_eig')


start = time.process_time()                 # Start measuring the runtime.

GULP = gulp.GULP(STEP, FROM, TO)                  # use the class (GULP) to create objects

try:
    GULP.Re_top_str()                       # convert "top_structure/B{FirstStep}-{rank}.xyz" to "top_structures/{rank}.xyz"
except IndexError:
    pass

files = GULP.Get_file_list(os.getcwd() + '/top_structures')     # get the full path of the xyz file in top_structures
os.chdir('gulp_eig')                                            # move to child path (parent working dir)

for f in files:
    marker = int(f.split('/')[-1].split('.')[0])
    if FROM_rank <= marker <= TO_rank: 
        cation, anion_core, anion_shel, dest, no_of_atoms = GULP.Convert_xyz_Gulp(f)    # retrieve info from xyz file 
        
        cwd = os.getcwd()                                                               # current working directory
        
        os.mkdir(dest)                                                                  # make working directory
        
        GULP.Write_Gulp(dest, cation, anion_core, anion_shel)                           # make gulp.in (gulp input file) at wd
        
        Gulp_output_path = GULP.Run_Gulp(cwd + '/' + dest, dest)                        # run gulp calc and get the output path
        
        total_energy, eigvec_array, freq = GULP.Grep_Data(Gulp_output_path, no_of_atoms, dest)  # retrieve essential data
        
        GULP.Modifying_xyz(dest, cwd + '/' + dest + f'/{dest}_eig.xyz',                 # optimised xyz + eigenvec
        eigvec_array, freq, no_of_atoms, total_energy) 

print(f"----- process time : {int((time.process_time() - start)/60)} mins {(time.process_time() - start) % 60} seconds, -----")



