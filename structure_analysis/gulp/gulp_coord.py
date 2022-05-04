import os
import sys
import re
from shutil import copy

aims = [ x for x in os.listdir('./') if '.xyz' in x ]
size = [ x.split('.')[0] for x in aims]
size = [ x.replace('n', '') for x in size]
size = [ x for x in size if x.isdigit() == True ]
#size = [ str('n')+x+str('.xyz') for x in size]

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text)]

size.sort(key=natural_keys)
print(size)

for n in size:
    os.mkdir(n)
    os.chdir(n)

    coord_range = [x/10 for x in range(0, 51)]
    dir_name = [x for x in range(0, 31)]


    for x in dir_name:
        x = str(x)
        os.mkdir(x)
        os.chdir(x)

        copy('../../n' + n + '.xyz', './')

        # preparing GULP file
        with open('n'+ n + '.xyz') as coord:
            anion = []
            cation = []
            for i, line in enumerate(coord):
                if i > 1: #and 'F' in line:
                    if 'F' in line:
                        a = line.replace('F   ', 'F   core ')
                        #b = line.replace('F   ', 'F   shel ')
                        #ab = a + b
                        #anion.append(ab)
                        anion.append(a)
                    if 'Al' in line:
                        c = line.replace('Al   ', 'Al   core ')
                        cation.append(c)

            anion = ''.join(anion)
            anion = anion.split('\n')
            anion = '\n'.join(anion)

            cation = ''.join(cation)
            cation = cation.split('\n')
            cation = '\n'.join(cation)

        xx = str(int(x)/10)
        with open('gulp.gin', 'w') as g:
            g.write('pot single distance\ncartesian\n')
            g.write(cation)
            g.write(anion)                                                      # CORE SHELL
            g.write(f'species\nAl core 3.00\nF  core -1.00\n \
                buck\nAl  core  F   core  3760.000831  0.222000   0.00000 0.0 10.0\n \
                buck4\nF   core  F   core  1127.7 0.2753 15.83 2.0 2.79 3.031 12.0\n \
                xtol opt 6.000\nftol opt 5.000\ngtol opt 8.000\n \
                switch_min rfo gnorm 0.01\nmaxcyc 2000\ncutd {xx}\n\noutput xyz {x}')
                # spring\n F 20.77
        print(f'gulp.gin is generated to run GULP (single, pot, distance)')
        print(os.getcwd() + '\n')
        os.system('gulp gulp')

        os.chdir('../')                                          #######
    os.chdir('../')
