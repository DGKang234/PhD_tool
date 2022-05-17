import gulp_eig_v2 as gulp
import aims as aims
import os, sys
import time
import shutil

'''
Brief explanation of what this code does:
    Calculate eigenvectors using GULP and add the eigenvectors to the cartesian 
    coordinate of optimised structure and prepare many xyz files.

HOW to use the code: 
     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
N.B. !!! the code requires [FIVE] argument. Read below for more info!!!
     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
To execute the code please type: 
[python gulp_eig_executable.py {[From] order of eigenvector component} {[To} order of eigenvector component} {Resolution of frequency} {[From] structure in IP rank} {[To] structure in IP rank}]

# UPDATE NOTE:
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
    
wd_name = 'gap_pre'
if wd_name  not in os.listdir('./'):
    os.mkdir(wd_name)
else:
    pass 


start = time.process_time()                                    

GULP = gulp.GULP(STEP, FROM, TO, SP='set')                      
AIMS = aims.AIMS()

try:
    GULP.Re_top_str()                                           
except IndexError:
    pass

files = GULP.Get_file_list(os.getcwd() + '/top_structures')     
os.chdir(wd_name)                                            

if 'ext_movie.xyz' in os.listdir('./'):
    os.remove('ext_movie.xyz')
else:
    pass




for f in files:                                                
    marker = int(f.split('/')[-1].split('.')[0])
    if FROM_rank <= marker <= TO_rank:
        #print("111111111111")
        cation, anion_core, anion_shel, DIR_IP_RANK, no_of_atoms = GULP.Convert_xyz_Gulp(f)    
        
        cwd = os.getcwd()                                                                      
        if DIR_IP_RANK not in os.listdir('./'):
            #print("22222222222222")
            os.mkdir(DIR_IP_RANK)    

            GULP_OUT_PATH = os.path.join(cwd, DIR_IP_RANK)
            GULP_OUT_PATH = GULP_OUT_PATH.split('/')[-1] + '/' + GULP_OUT_PATH.split('/')[-1]
            
            GULP.Write_Gulp(DIR_IP_RANK, GULP_OUT_PATH, cation, anion_core, anion_shel, 'n')              
            Gulp_output_path = GULP.Run_Gulp(cwd + '/' + DIR_IP_RANK, DIR_IP_RANK)                        
            total_energy, eigvec_array, freq = GULP.Grep_Data(Gulp_output_path, no_of_atoms, DIR_IP_RANK)  
       
            PATH = os.path.join(cwd, DIR_IP_RANK)
            
            GULP.Modifying_xyz(DIR_IP_RANK, PATH + f"/{DIR_IP_RANK}_eig.xyz", eigvec_array, freq, no_of_atoms, total_energy) 
            sub_wd = [x for x in os.listdir(f'{PATH}') if os.path.isdir(f'{PATH}/{x}')] 
        
        else:
            #print("222222222222-------2")
            PATH = os.path.join(cwd, DIR_IP_RANK)
            sub_wd = [x for x in os.listdir(PATH) if os.path.isdir(f'{PATH}/{x}')]


        for i in sub_wd:
            #print("333333333333")
            SECOND_LAST_PATH_FULL = os.path.join(PATH, i)
            
            mod_list = [x for x in os.listdir(SECOND_LAST_PATH_FULL) 
                    if not os.path.isdir(os.path.join(SECOND_LAST_PATH_FULL, x)) and 'movie.xyz' not in x] 

            mod_list = sorted(mod_list, key = lambda x: int(x.split('_')[1].split('.')[0]))
           
            mod_dir_list = [x for x in os.listdir(SECOND_LAST_PATH_FULL) 
            if os.path.isdir(os.path.join(SECOND_LAST_PATH_FULL, x))]
            
            mod_list_PATH = [os.path.join(SECOND_LAST_PATH_FULL, x) for x in mod_list] 

            for j in mod_list_PATH:
                #print("444444444444")
                print()
                print(f"Working on the {j.split('gap_pre')[1]}")
                print()
                
                cat, an_core, an_shel, MOD_XYZ_LABEL, no_of_atoms = GULP.Convert_xyz_Gulp(j)
                FINAL_PATH_FULL = os.path.join(SECOND_LAST_PATH_FULL, 'sp_' + MOD_XYZ_LABEL)
                spliter = FINAL_PATH_FULL.split('/')[-4] + '/'
                GULP_OUT_PATH = FINAL_PATH_FULL.split(spliter)[1] + '/' + FINAL_PATH_FULL.split('/')[-1]
              
                if len(mod_dir_list) == 0:
                    #print("555555555555")
                    os.mkdir(FINAL_PATH_FULL)
                    GULP.Write_Gulp(FINAL_PATH_FULL, GULP_OUT_PATH, cat, an_core, an_shel, 'y')
                    gulp_output_path = GULP.Run_Gulp(FINAL_PATH_FULL, FINAL_PATH_FULL)
                    tot_energy, eigv_array, fre = GULP.Grep_Data(Gulp_output_path, no_of_atoms, 
                    FINAL_PATH_FULL) 

                #
                # aims
                # 
                if 'aims.out' not in os.listdir(FINAL_PATH_FULL):
                    #print("666666666666")
                    AIMS.Prepare_con_sub_files(FINAL_PATH_FULL, MOD_XYZ_LABEL)
                    AIMS.xyz_to_Geometry(FINAL_PATH_FULL)
                    AIMS.Aims_submit(FINAL_PATH_FULL)

                else:
                    print("666666666666-------2")
                    AIMS.Aims_grep_data(FINAL_PATH_FULL)
                    AIMS_ENERGY, FORCES, no_of_atoms = AIMS.Aims_grep_data(FINAL_PATH_FULL)
                    AIMS.Aims_extended_xyz(FINAL_PATH_FULL, no_of_atoms, FORCES, AIMS_ENERGY)
   
                         
                    


                print()
                print()
                print('FINAL_PATH_FULL:' + FINAL_PATH_FULL)
                print('SECOND_LAST_PATH_FULL: ' + SECOND_LAST_PATH_FULL)
                print('MOD_XYZ_LABEL: ' + MOD_XYZ_LABEL)
                print('GULP_OUT_PATH: ' + GULP_OUT_PATH)
                print('DIR_IP_RANK: ' + DIR_IP_RANK)
                print('i (sub_wd): ' + i) #' '.join(sub_wd))
                print('j (mod_list_PATH): ' + j)#' '.join(mod_list_PATH))

if 'aims.out' in os.listdir(FINAL_PATH_FULL):
    with open('/home/uccatka/auto/for_GAP/Al_atom/aims.out', 'r') as f:
        lines = f.readlines()
        for i in lines:
            if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation' in i:
                Al_atom_energy = i.split()[11]
    with open('ext_movie.xyz', 'a') as f:
        f.write('1\n')
        f.write(f'Properties=species:S:1:pos:R:3:forces:R:3 energy={Al_atom_energy} pbc="F F F"\n') 
        f.write('Al 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000\n')


    with open('/home/uccatka/auto/for_GAP/F_atom/aims.out', 'r') as f:
        lines = f.readlines()
        for i in lines:
            if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation' in i:
                F_atom_energy = i.split()[11] 
    with open('ext_movie.xyz', 'a') as f:
        f.write('1\n')
        f.write(f'Properties=species:S:1:pos:R:3:forces:R:3 energy={F_atom_energy} pbc="F F F"\n')
        f.write('Al 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000')          
                

print(f"----- process time : {int((time.process_time() - start)/60)} mins {(time.process_time() - start) % 60} seconds -----")




