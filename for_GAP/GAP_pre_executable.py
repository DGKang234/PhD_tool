import gulp 
import aims as aims
import os, sys
import time
import shutil

'''
Brief explanation of what this code does:
    Calculate eigenvectors using GULP and add the eigenvalues to the cartesian coordinate of optimised 
    structure and prepare many xyz files.

HOW to use the code: 
     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
N.B. !!! the code requires [FIVE] argument. Read below for more info!!!
     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
     !!! Once you run the initial calculation single point FHI-aims calculation will be submitted  !!!
     !!! Once they finished please re-run the code! which will generate ext_movie in the {gap_pre} !!!
     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
To execute the code please type:
-> If you want to choose specific eigenvalues
[python /{path}/{to}/gap_pre_executable.py {[From]th eigenvalue component} {[To}th eigenvalue component} {Resolution (lambda) of frequency} {[From] IP rank structure in IP rank} {[To] IP rank structure in IP rank}]

-> If you want to run ALL eigenvalues
[python /{path}/{to}/gap_pre_executable.py {100} {Resulution (lambda)} of frequency} {[From] IP rank structure in IP rank} {[To] IP rank structure in IP rank}]

OUTPUT: 
[gap_pre] directory contains all outputs
    inside of [gap_pre] there will be the directories which are named with IP rank of the structure, [{IP rank}]
        -> insde of the [{IP rank}] the output from the gulp optimisation calculation. and [{order of eigenvalue}] directories
            -> insdie of the [{order of eigenvalue}] 
                - 200/{Resolution (lambda)} number of modified xyz files (sum({rank}_eig.xyz, eigenvector))
                - ------" " ------- number of directories
                    inside of the directories 
                    -output of the single point FHI-aims calculations
                
    


# VERSION NOTE:
    * 0.0v (29 April 2022 - 29 April 2022): Testing version (fully working) - need to be modulised
    * 1.0v (4 May - 5 May): Composed of classes and function for modulisation - fully modulised 
        (using this in this executable)

    * 1.1v (working on) : -> Allowing to select which IP rank structure to calculate        (V) 
                          -> Allowing to customise lambda ( lambda * eigenvector)           (V)
                          -> Calling potential library instead of using written potential   ( )

    * 2.0v (working on) : -> Calculate single point of the modified xyz files               (V)
                          -> Calculate the force of the individual atoms - FHI-aims         (V)
                          -> Make extended xyz files                                        (V)
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
if FROM == 100:
    TO = 0                      # ignore, it will be changed in def Grep_Data in GULP class
    STEP = int(sys.argv[2])
    FROM_rank = int(sys.argv[3])
    TO_rank = int(sys.argv[4])
    
    pass
else:
    TO = int(sys.argv[2])
    STEP = int(sys.argv[3])
    FROM_rank = int(sys.argv[4])
    TO_rank = int(sys.argv[5])
    
wd_name = 'gap_pre'
if wd_name  not in os.listdir('./'):
    os.mkdir(wd_name)
else:
    pass 

# Instantiate Classes
GULP = gulp.GULP(STEP, FROM, TO, SP='set')                      
AIMS = aims.AIMS()

# Re-naming the xyz files
try:
    GULP.Re_top_str()                                           
except IndexError:
    pass

# Get the list of xyz files (full path)
files = GULP.Get_file_list(os.getcwd() + '/top_structures')  

# Move upto 'gap_pre' 
os.chdir(wd_name)                                            

if 'ext_movie.xyz' in os.listdir('./'):
    os.remove('ext_movie.xyz')
else:
    pass

start = time.process_time()
dummy_1 = []
dummy_2 = []
for f in files:                                                
    rank = int(f.split('/')[-1].split('.')[0])
    if FROM_rank <= rank <= TO_rank:
        print("111111111111")
        cation, anion_core, anion_shel, DIR_IP_RANK, no_of_atoms = GULP.Convert_xyz_Gulp(f)    

        cwd = os.getcwd()                                                                      
        if DIR_IP_RANK not in os.listdir('./'):         # DIR_IP_RANK = 001, 002,...
            print("22222222222222")
            os.mkdir(DIR_IP_RANK)    
            GULP_OUT = os.path.join(cwd, DIR_IP_RANK)
            GULP_OUT_PATH = GULP_OUT.split('/')[-1] + '/' + GULP_OUT.split('/')[-1]
            
            GULP.Write_Gulp(DIR_IP_RANK, GULP_OUT_PATH, cation, anion_core, anion_shel, 'n') 
            Gulp_output_path = GULP.Run_Gulp(GULP_OUT, DIR_IP_RANK)
            total_energy, eigvec_array, freq = GULP.Grep_Data(Gulp_output_path, no_of_atoms, DIR_IP_RANK, 'n')
            
            #PATH = os.path.join(cwd, DIR_IP_RANK)
            GULP.Modifying_xyz(DIR_IP_RANK, GULP_OUT + f'/{DIR_IP_RANK}_eig.xyz', eigvec_array, freq, no_of_atoms, total_energy)
            GULP.Breathing_xyz(DIR_IP_RANK, GULP_OUT + f'/{DIR_IP_RANK}_eig.xyz', no_of_atoms, total_energy)
            sub_wd = [x for x in os.listdir(f'{GULP_OUT}') if os.path.isdir(f'{GULP_OUT}/{x}')]
            print(sub_wd)
            sub_wd = sorted(sub_wd, key=lambda x: isinstance(x, int))   #int)

        else:                                   # when the 001/002... directory is exsiting
            print("222222222222-------2")
            GULP_OUT = os.path.join(cwd, DIR_IP_RANK)
            sub_wd = [x for x in os.listdir(GULP_OUT) if os.path.isdir(f'{GULP_OUT}/{x}')]
            sub_wd = sorted(sub_wd, key=int)

        for i in sub_wd:                        # sub_wd = order of eigenvale (0, 1, 2 ...)
            print("333333333333")
            SECOND_LAST_PATH_FULL = os.path.join(GULP_OUT, i)
            mod_list = [x for x in os.listdir(SECOND_LAST_PATH_FULL) 
                            if not os.path.isdir(os.path.join(SECOND_LAST_PATH_FULL, x)) and 'movie.xyz' not in x] 
            #mod_list = sorted(mod_list, key = lambda x: int(x.split('_')[1].split('.')[0]))
            mod_list_PATH = [os.path.join(SECOND_LAST_PATH_FULL, x) for x in mod_list]
            mod_list_PATH = sorted(mod_list_PATH, key=lambda x: x.split('/')[-1].split('_')[1].split('.')[0]) # list of mod_{lambda}.xyz

            mod_dir_list = [x for x in os.listdir(SECOND_LAST_PATH_FULL) 
                                    if os.path.isdir(os.path.join(SECOND_LAST_PATH_FULL, x))]               # list of sp_mod_{labmda} dir
            
            for j in mod_list_PATH:     
                print("444444444444")
                print(f"Working on the {j.split('gap_pre')[1]}")
                print()
                cat, an_core, an_shel, MOD_XYZ_LABEL, no_of_atoms = GULP.Convert_xyz_Gulp(j)
                FINAL_PATH_FULL = os.path.join(SECOND_LAST_PATH_FULL, 'sp_' + MOD_XYZ_LABEL)
                spliter = FINAL_PATH_FULL.split('/')[-4] + '/'
                GULP_OUT_PATH = FINAL_PATH_FULL.split(spliter)[1] + '/' + FINAL_PATH_FULL.split('/')[-1]
 
                if len(mod_dir_list) == 0:
                    print("555555555555")
                    os.mkdir(FINAL_PATH_FULL)
                    GULP.Write_Gulp(FINAL_PATH_FULL, GULP_OUT_PATH, cat, an_core, an_shel, 'y')             # single-point calculation
                    gulp_output_path = GULP.Run_Gulp(FINAL_PATH_FULL, FINAL_PATH_FULL)          
                    gulp_out = FINAL_PATH_FULL + '/gulp.gout'

                    try:
                        tot_energy, eigv_array, fre, FORCES_GULP = GULP.Grep_Data(gulp_out, no_of_atoms, FINAL_PATH_FULL, SP='y')
                    except IndexError:
                        dummy_2.append(FINAL_PATH_FULL) 
                    except UnboundLocalError:
                        dummy_2.append(FINAL_PATH_FULL)
                    except ValueError:
                        dummy_2.append(FINAL_PATH_FULL)

                    try:
                        GULP.Ext_xyz_gulp(FINAL_PATH_FULL, no_of_atoms, eigv_array, FORCES_GULP, tot_energy)
                        dummy_1.append(FINAL_PATH_FULL)
                    except FileNotFoundError:
                        dummy_2.append(FINAL_PATH_FULL)
                    except UnboundLocalError: 
                        dummy_2.append(FINAL_PATH_FULL)

print()
print(len(dummy_1), dummy_1)
print()
print(len(dummy_2), dummy_2)
                
print()
print(f"----- process time : {(time.process_time() - start)} seconds -----")


