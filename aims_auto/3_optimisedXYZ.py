
import os
from shutil import copy
import sys
import glob
import shutil


def get_rank(input_dir):
    pref = input_dir.split('_')[1]
    return pref

def get_directories(path):
    directories = [x for x in os.listdir(path)]  # 'directories' = x which is in the 'path'
    directories = [(path + x) for x in directories]  # now directories = x that x is x + path
    return directories


from_ = int(input("from which KLMC rank of .xyz and aims optimised .xyz file do you want to collect ? : "))
to_ = int(input("upto which KLMC rank of .xyz and aims optimised .xyz file do you want to collect ? : "))

path = os.getcwd() + '/ranked/'     #'/home/uccatka/Scratch/work/' + t + '/ranked/'
dest = os.getcwd() + '/xyzFiles/'   #'/home/uccatka/Scratch/work/' + t +'/xyzFiles'

try:  
    os.mkdir(dest)
except OSError:  
    print ("The directory is already existed %s" % dest)
else:  
    print ("Successfully created the directory %s " % dest)

_dir = get_directories(path)
_dir.sort()

'''
Make {aims.xyz} files  
'''
convert = "aims_to_xyz.sh"

max_len = [x for x in os.listdir('./ranked') if x.isdigit and os.path.isdir('./ranked/'+x)]
max_len.sort()

ranked_dir_path = [path + x for x in max_len]
ranked_dir_path = [x.replace("/scratch/scratch/uccatka/", "/home/uccatka/Scratch/") for x in ranked_dir_path]

for i in ranked_dir_path:
    rank_ = i.split('/')[-1]
    if from_ <= int(rank_) <= to_:
        print(int(rank_), i)

        os.chdir(i)
        os.system("bash /home/uccatka/auto/aims_auto/aims_to_xyz.sh geometry.in.next_step")
        print('.xyz file of aims optimised structure is generated')
        
        dummy = glob.glob(i + '/aims.xyz')    			# ~P/aims.xyz  
        dummy_1 = glob.glob(i + '/' + i.split('/')[-1] + '.xyz')    	# ~P/001.xyz (KLMC)
        fname = ''.join(dummy)                                    
        fname_1 = ''.join(dummy_1)    
        
        rank = fname_1.split('/')[-2]
        dummy_1 = rank + '/' + fname.split('/')[-1]                      # 001/aims.xyz  
        dummy_11 = rank + '/' + fname_1.split('/')[-1]			# 001/001.xyz
        
        out_cur = dummy_1.replace('/', '_')                        
        out_cur_1 = rank + '_' + 'klmc.xyz'
    
        copy(fname, dest + '/' + out_cur)                    
        copy(fname_1, dest + '/' + out_cur_1)
    
        print ('The file ' + '[' + out_cur + ']' + ' and ' + '[' + out_cur_1 + ']' + ' has been moved to "xyzFiles" directory.')
        print()
         
        os.chdir('../')
print()
print("###############################################")
print("##-----------Mission accomplished------------##")
print("###############################################")


