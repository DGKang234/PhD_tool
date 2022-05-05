import gulp_eig_v2 as gulp
import os
import time




start = time.process_time()

GULP = gulp.GULP() 
#FROM = int(input("[From] which order of frequency would you like to take? : "))
#TO = int(input("[To] which order of frequency would you like to take? : ")) + 1
GULP.Re_top_str()
files = GULP.Get_file_list(os.getcwd() + '/top_structures')
os.mkdir('gulp_eig')
os.chdir('gulp_eig')
for f in files:
    cation, anion_core, anion_shel, dest, no_of_atoms = GULP.Convert_xyz_Gulp(f)
    cwd = os.getcwd()
    os.mkdir(dest)
    GULP.Write_Gulp(dest, cation, anion_core, anion_shel)
    Gulp_output_path = GULP.Run_Gulp(cwd + '/' + dest, dest)
    total_energy, eigvec_array, freq = GULP.Grep_Data(Gulp_output_path, no_of_atoms, dest)
    
    GULP.Modifying_xyz(dest, cwd + '/' + dest + f'/{dest}_eig.xyz', eigvec_array, freq, no_of_atoms, total_energy) #f'{cwd}/{dest}/{dest}_eig.xyz', freq)


print(f"----- process time : {int((time.process_time() - start)/60)} mins {(time.process_time() - start) % 60} seconds, -----")



