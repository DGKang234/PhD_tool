#!/usr/bin/python

import os
import os.path
from os import path
import shutil
import sys
import subprocess as sp

###########################################################
def get_directories(path):
    directories = [x for x in os.listdir(path)]
    directories = [(path + x) for x in directories]
    return directories

def get_files(path, ext):
    files = [ x for x in os.listdir(path) if ext in x ]
    files = [ (path + x) for x in files ]
    return files
###########################################################
#print('please type target working directory (after ~Scratch/')
target = os.getcwd() #input()

from_ = int(input('from which step do you want to calculate? : '))
to_   = int(input('up to which step do you want to calculate? : '))

root = '/home/uccatka/auto/copy_this_for_new/'
path = target + '/top_structures/'  #'/home/uccatka/Scratch/' + target + '/top_structures/'
dest = target + '/ranked/'          #'/home/uccatka/Scratch/' + target + '/ranked/'
###########################################################
#####       Check contents of the directories        ######
###########################################################
_dir = get_directories(dest)

###########################################################
##### Copy the essential files to acquired directory ######
###########################################################
_dir = get_directories(dest)

file_1 = 'control.in'
file_4 = 'a.out'
file_3 = 'trash_1.sh'


foo = 'trash_1.sh'
bar = 'trash.sh'

_dir.sort()
wd = os.getcwd()

for i in range(len(_dir)):
    dir_name = _dir[i].split('/')[-1]
    #print(int(dir_name))

    if from_ <= int(dir_name) <= to_:

        a = dest + dir_name
        print(a)
        control = os.path.exists(a + "/geometry.in")
        if control == False:
            shutil.copy(root + file_1, _dir[i])
            shutil.copy(root + file_3, _dir[i])
            print('copy "control.in", "trash_1.sh" to ~/' + dir_name + '  -- Done')

            with open(_dir[i] + '/' + foo, 'r') as f:
                edit_1 = f.read().replace("target_1", str(_dir[i].replace(root, target + '/')))
                edit_2 = edit_1.replace("target_2", str(_dir[i]).replace(dest, ''))
                with open(_dir[i] + '/' + bar, 'w') as f:
                    f.write(edit_2)

            os.remove(_dir[i] + '/' + foo)
            print('"trash_1.sh" is removed and "trash.sh" produced with right output file path ~/' + dir_name+ '  -- Done')

            xyz_1 = _dir[i] + '/'
            xyz_2 = get_files(xyz_1, '.xyz')
            args_ = str(xyz_2)[2:-2]
            print(args_)
            os.chdir(_dir[i] + '/')
            os.system(f"bash /home/uccatka/auto/xyz_to_aims.sh {args_}")

            os.chdir(wd)
            print('"geometry.in" has been produced for ' +  dir_name  + ' -- Done\n')

        else:
            print('Done')

_dir.sort()

wd = os.getcwd()
for l in range(len(_dir)):
    dir_name = _dir[l].split('/')[-1]

    if from_ <= int(dir_name) <= to_:
        loc = dest +  dir_name
        os.chdir(loc + '/')
        os.system("qsub trash.sh")

        os.chdir(wd)

        print("FHI-aims (DFT) %s is submitted -- GOOD LUCK" % (_dir[l]))
print("\n\n###############################################")
print("#------------Mission accomplished]------------#")
print("###############################################\n\n")
