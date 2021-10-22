import os
from shutil import copy
import sys
import glob
import shutil

#os.rename("~/originalFileName", "~/newFileName")
#shutil.move("~/newFileName", "~/Destination_dir")

def get_rank(input_dir):
    pref = input_dir.split('_')[1]
    return pref

def get_directories(path):
    directories = [x for x in os.listdir(path)]  # 'directories' = x which is in the 'path'
    directories = [(path + x) for x in directories]  # now directories = x that x is x + path
    return directories

t = input('please type the working directory : ')

from_ = int(input("from which KLMC rank of .xyz and aims optimised .xyz file do you want to collect ? : "))
to_ = int(input("upto which KLMC rank of .xyz and aims optimised .xyz file do you want to collect ? : "))

root = '/home/uccatka/auto/copy_this_for_new/'
path = '/home/uccatka/Scratch/' + t + '/ranked/'
dest = '/home/uccatka/Scratch/' + t +'/xyzFiles'

try:  
    os.mkdir(dest)
except OSError:  
    print ("The directory is already existed %s" % dest)
else:  
    print ("Successfully created the directory %s " % dest)

print('Do you want to proceed to collect all of the aims optimised .xyz files? y/n?')
permi = input()
if permi == 'n':
    print('The process has been cancelled')
    sys.exit()
else:
    pass

_dir = get_directories(path)
_dir.sort()
########################
# Make aims.xyz files  #
########################
convert = "aims_to_xyz.sh"
for i in range(len(_dir)):
    if from_ <= int(i)+1 <= to_:
        os.chdir(_dir[i])
        shutil.copy(root + convert, _dir[i])
        os.system("sh aims_to_xyz.sh geometry.in.next_step")
        os.chdir(path)

_dir = []
for i in os.listdir(path):                             
    os.chdir(path)
    if os.path.isdir(i) == True:            
        _dir.append(i)                              
_dir.sort()

for j in range(len(_dir)):    
    if from_ <= int(j)+1 <= to_:

        rank = _dir[j]
        print('/n')                             
        print(rank)        
        os.chdir(path + '/' + _dir[j])            
        
        P = os.getcwd()
        dummy = glob.glob(P + '/aims.xyz')    			# ~P/aims.xyz  
        dummy_1 = glob.glob(P + '/' + _dir[j] + '.xyz')    	# ~P/001.xyz (KLMC)

        fname = ''.join(dummy)                                    
        fname_1 = ''.join(dummy_1)    

        dummy_1 = fname.replace(P + '/', '')                      # 001/aims.xyz  
        dummy_11 = fname_1.replace(P + '/', '')			# 001/001.xyz
        
        out_cur = rank + '_' + dummy_1                        
        out_cur_1 = rank + '_' + 'klmc.xyz'
        print(out_cur)        
        print(out_cur_1)

        if len(out_cur) < 5:
            continue
        if len(out_cur_1) < 5:
            continue
             
        copy(fname, dest + '/' + out_cur)                    
        copy(fname_1, dest + '/' + out_cur_1)
 
        print ('The file ' + '[' + out_cur + ']' + 'has been moved to "xyzFiles" directory.')

        os.chdir('../')
print("\n###############################################")
print("##-----------Mission accomplished------------##")
print("###############################################")


