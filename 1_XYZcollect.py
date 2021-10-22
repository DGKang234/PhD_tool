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

##########################################################################################

#List all .xyz files in a specified directory + subdirectories

print('Please type the working directory')
target = input()

from_ = int(input('from which step do you want to calculate? : '))
to_   = int(input('up to which step do you want to calculate? : '))

path = '/home/uccatka/Scratch/' + target + '/top_structures/'
dest = '/home/uccatka/Scratch/' + target + '/ranked/'

files = get_files(path, '.xyz')
try:
    os.mkdir(dest)
except:
    pass

outfile = []
for i in range(len(files)):
    cur_file = files[i]
    rank = get_rank(files[i])
    #out = rank + '.xyz'

    outfile.append(rank)
outfile.sort()


for i in range(len(outfile)):

    if from_ <= i+1 <= to_:
        os.chdir(dest)

        rank = outfile[i].split('/')[-1]
        os.mkdir(rank)

        end = dest + rank + '/'

        #print(end)

        #print(outfile[i]+'.xyz')

        shutil.copy(outfile[i] + '.xyz', end)

        os.chdir(path)

        print('\n\nWorking direcotry --  0' + str(i+1) + ' -- DONE')



print("\n###############################################")
print("#------------Mission accomplished]------------#")
print("###############################################")
