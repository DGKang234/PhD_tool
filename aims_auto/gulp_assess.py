import os
import subprocess
import shutil

def get_files(path, ext):
    global files
    files = [ x for x in os.listdir(path) if ext in x ]
    files = [ (path + x) for x in files ]
    files.sort()
    return files

def hkg(type_, xyz, rad):
    global hkg_out
    hkg_executable = '/home/uccatka/software/hkg/hkg.py' 
    hkg_out = subprocess.check_output(["python", hkg_executable, xyz, str(rad)])
    hkg_out = str(hkg_out)
    hkg_out = hkg_out[2:-3]
    print(type_, hkg_out)
    return hkg_out

target = os.getcwd()
target = target.replace('/scratch/scratch/uccatka', '/home/uccatka/Scratch')

dir_ranked = target + '/ranked/'
dir_xyzFiles = target + '/xyzFiles/'

get_files(dir_xyzFiles, 'aims.xyz')  # source

if 'gulp' in os.listdir('./'):
    shutil.rmtree('gulp')
    os.mkdir('gulp')
    os.chdir('gulp')
else:
    os.mkdir('gulp')

gulp_error = []
caution_scaling = []
for x in files:
    
    cation = []
    anion_core = []
    anion_shel = []

    with open(x, 'r') as coord:
        for i, line in enumerate(coord):
            if i > 1:
                if 'Al' in line:
                    c = line.replace(' Al  ', 'Al  core')
                    cation.append(c)
                
                if 'F' in line:
                    a_core = line.replace('  F  ', 'F   core')
                    a_shel = line.replace('  F  ', 'F   shel')
                    anion_core.append(a_core)
                    anion_shel.append(a_shel)

    anion_core = ''.join(anion_core)
    anion_core = anion_core.split('\n')
    anion_core = '\n'.join(anion_core)

    anion_shel = ''.join(anion_shel)
    anion_shel = anion_shel.split('\n')
    anion_shel = '\n'.join(anion_shel)

    cation = ''.join(cation)
    cation = cation.split('\n')
    cation = '\n'.join(cation)

    dest = x.split('/')[-1]
    dest = dest.split('_')[0]
    
    os.mkdir(dest)
    
    with open(dest + '/gulp.gin', 'w') as f:
        f.write('opti conp conj prop\ncartesian\n')
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
output xyz {dest}_gulp')             # 3760.000831  0.222000   0.00000 0.0 10.0\n/

    print(f'{dest} is read to run GULP')
    
    os.chdir(dest)
    
    source_xyz = os.path.join(dir_xyzFiles, x)
    shutil.copy(source_xyz, './')

    subprocess.check_output(["gulp", "gulp"])

    gulp_output = target + '/gulp/' + dest + '/gulp.gout'
    with open(gulp_output, 'r') as f:
        if 'Job Finished' in f.read():
            print(f'{dest} DONE')
        else:
            print(f'!!!! {dest} Error !!!!')
            gulp_error.append(x)

    ###############################
    #   hashkey from {aims.xyz}   #
    ############################### 
    
    if 'gulp.xyz' in os.listdir(f'{target}/gulp/{dest}'): 
        cf_cluster = '/home/uccatka/software/CF-CLUSTERpy/CF_CLUSTERSpy_MAIN.py'
        subprocess.check_output(['python', cf_cluster, dest + '_aims.xyz', dest + '.xyz'])
        
        '''
        hkg('DFT',  'CF_1.xyz', 2.46)
        aims_hkg = hkg_out

        hkg('IP ', 'CF_2.xyz', 2.46)
        gulp_hkg = hkg_out

        bowl = []
        bowl.append(aims_hkg)
        bowl.append(hkg_out)
   
        bowl = list(set(bowl))

        matching_X = []
        if len(bowl) == 1:
            print("The AlF3 potential can predict the structure")
            print()
        elif len(bowl) > 1:
            print("!!!! DFT structure cannot be found in IP landscape")
            print()
            matching_X.append(x)
        '''
        cf_output = target + '/gulp/' + dest + '/CF.out'
        with open(cf_output, 'r') as f:
            lines = f.readlines()
            scaling = [l for l in lines if 'Scaling Factor :' in l]
            scaling = ' '.join(scaling).split()[3]

            if float(scaling) > 0.96:
                print(dest, "scaling factor : " + scaling) 
            else:
                print(dest, " ###### CHECK the xyz #####")
                caution_scaling.append(dest)
                 
            RMS_config = [l for l in lines if 'RMS CONFIG:' in l]
            RMS_config = ' '.join(RMS_config).split()[2]
            print(dest, "RMS config :     " + RMS_config)
            print()
             
        os.chdir('../')
    else:
        os.chdir('../')
collection = os.listdir('./')
collection.sort()

'''
for x in collection:
    with open(x + '/CF_3.xyz', 'r') as f:
        lines = f.readlines()

        for l in lines:
            with open('mega.xyz', 'a') as f:
                f.write(l)


    print(f'{x} appended to mega.xyz') 
'''         


#print(f"!!!!! {x} DFT structure cannot be found in IP landscape !!!!!")
print(f"!!!!! {caution_scaling} check CF3.xyz !!!!!")


