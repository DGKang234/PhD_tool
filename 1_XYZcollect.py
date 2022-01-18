#!/usr/bin/python3

import os
import shutil
import sys
import fileinput

##########################################################################################

# Functions
def get_rank(xyz):
    pref = xyz.split('-')[0]
    pref = pref.replace('.xyz', '')
    return pref

def get_files(path, ext):
    files = [ x for x in os.listdir(path) if ext in x ]
    files = [ (path + x) for x in files ]
    return files

def func(elem):
    return int(elem.split('/')[-1].split('.xyz')[0])
##########################################################################################

#List all .xyz files in a specified directory + subdirectories

target = os.getcwd()
target = target.replace('/scratch/scratch/uccatka', '/home/uccatka/Scratch')

from_ = int(input('from which step do you want to calculate? : '))
to_   = int(input('up to which step do you want to calculate? : '))

path = target + '/top_structures/'   
dest = target + '/ranked/'          

files = get_files(path, '.xyz')
files = sorted(files, key=func)
try:
    os.mkdir(dest)
except:
    pass

outfile = []
for i in range(len(files)):
    cur_file = files[i]
    rank = get_rank(files[i])
    outfile.append(rank)


for num, i in enumerate(outfile): 
    if from_ <= num+1 <= to_:
        os.chdir(dest)

        rank = outfile[num].split('/')[-1]
        print(rank)

        os.mkdir(rank)
        
        end = dest + rank + '/'

        shutil.copy(outfile[num] + '.xyz', end)


print("\n###############################################")
print("#------------Mission accomplished]------------#")
print("###############################################")
