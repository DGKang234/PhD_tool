

import os, sys
import re
import pandas as pd
import numpy as np
import subprocess

'''
This code will produce .csv file which conatains global optimisation (klmc) -> 
DFT (aims) -> SM (gulp) energies with it's energy ranking.
After the energies are collected the duplicated structurer will be eliminated using 
python ver (written by Tomas Lazauskas) of NAUTY (No AUTomorphisms, Yes?).

However, if you are using
'0_preprocessing_step.py', '1_XYZcollect.py', '2_essentials.py', '3_optimisedXYZ.py', and 'gulp_assess.py'
code for automation you don't needto change anything.

variable:
{output_group}: where the directory of DFT (aims) calculations are located
'''


def grep_out(loc, out = 'aims.out'):
    contents = [loc + x for x in os.listdir(loc) if out in x]
    contents = ''.join(contents)
    return contents

def get_files(A='./', B=''):
    files = [x for x in os.listdir(A) if B in x]
    return(files)
try:
    radius = sys.argv[1]
except IndexError:
    print()
    print("==========================================================================")
    print("you need to type an argument:{radius} for the hashkey (e.g. 2.46 for AlF3)")
    print("==========================================================================")
    print()
    sys.exit()


'''
collect stats (single point DFT energy, final DFT energy, klmc energy and ranking that correspond to SM, DFT energy)
'''

output_group = './ranked/'
sp_marker = '| Total energy                  :'
final_marker = 'Hartree-Fock s.c.f. calculation      :' #'| Total energy of the DFT / Hartree-Fock s.c.f. calculation      :     '
klmc_marker = 'SCF Done'
gulp_marker = 'Final energy ='


dir_list = [output_group + x + '/' for x in os.listdir(output_group) if os.path.isdir(output_group + x)]
dir_list.sort()

out_full_path = list(map(grep_out, dir_list))

collection_sp_E = []
collection_final_E = []

for num, i in enumerate(out_full_path):
    print(i)
    with open(i, 'r') as f:
        lines = f.readlines()
        sp_from_each_file = ['-' + x.split('-')[2].split(' ')[0] for x in lines if sp_marker in x]
        final_from_each_file = ['-' + x.split('-')[2].split(' ')[0] for x in lines if final_marker in x]
        #final_from_each_file = [float(x.split(':')[1].split('eV')[0]) for x in lines if final_marker in x] 
        print(final_from_each_file)
        collection_sp_E.append(sp_from_each_file[0])
        collection_final_E.append(final_from_each_file[0])
        print()


df = pd.DataFrame(columns = ['IP_rank', 'SP_E', 'Final_E'])

ensemble_dir = [x.split('/')[2] for x in out_full_path]
df['IP_rank'] = ensemble_dir 
df['SP_E'] = collection_sp_E
df['SP_E'] = df['SP_E'].astype('float')
df['Final_E'] = collection_final_E
df['Final_E'] = df['Final_E'].astype('float')
df['delta_(a)'] = df['Final_E'] - df['Final_E'].min()
#df['aims_R'] = df['Final_E'].rank().astype('int')
df['aims_R'] = df.Final_E.rank(method='dense').astype(int)

df = df[['aims_R', 'SP_E', 'Final_E', 'delta_(a)']]
#pd.set_option("display.max_rows", None, "display.max_columns", None)

xyz = get_files('./xyzFiles', '.xyz')  #get_xyz('./xyzFiles')
xyz = sorted(xyz, key=lambda x: x.split('_')[0]) #xyz.sort()

klmc_xyz = [x.split('/')[2] + '.xyz' for x in out_full_path]
klmc_full_path = list(map(grep_out, dir_list, klmc_xyz))

collection_klmc_E = []
for i in klmc_full_path:
    with open(i, 'r') as f:
        lines = f.readlines()
        sme_from_each_file = [x.split()[2] for x in lines if klmc_marker in x]
        #[x.split('            ')[1].split('\n')[0] for x in lines if klmc_marker in x]
        collection_klmc_E.append(sme_from_each_file[0])

df['klmc_E'] = [float(x) for x in collection_klmc_E] 
df['delta_(k)'] = df['klmc_E'] - df['klmc_E'].min()
df['klmc_R'] = df.klmc_E.rank(method='dense').astype(int)

df = df[['aims_R', 'SP_E', 'Final_E', 'delta_(a)', 'klmc_R', 'klmc_E', 'delta_(k)']]

#print(df)
df.to_csv('./scratch.csv')


# ==================================================================================


'''
Collect gulp optimised aims info
'''

dir_list = ['./gulp/' + x + '/'  for x in os.listdir('./gulp') if os.path.isdir('./gulp/' + x)]
dir_list = sorted(dir_list, key = lambda x: x.split('/')[2])

n_number = df['klmc_E'].size
gulp_out = [str(x).replace(str(x), 'gulp.gout') for x in range(n_number)]    
out_full_path = list(map(grep_out, dir_list, gulp_out))
out_full_path.sort()

collection_gulp_E = []
for num, i in enumerate(out_full_path):
    print(i)
    with open(i, 'r') as f:
        lines = f.readlines()
        gulp_from_each_file = [x.split()[3] for x in lines if gulp_marker in x]   
        #[x.split('    ')[1].split(' ')[0] for x in lines if gulp_marker in x]
        collection_gulp_E.append(gulp_from_each_file[0])
        print(num+1, gulp_from_each_file)

df['re_gulp_E'] = [float(x) for x in collection_gulp_E]
df['re_gulp_R'] = df.re_gulp_E.rank(method='dense').astype(int)

df['re_gulp_E'] = df['re_gulp_E']*10000 #  .round(4)
df['re_gulp_E'] = df['re_gulp_E'].astype(int)
df['re_gulp_E'] = df['re_gulp_E']/10000

df['klmc_E'] = df['klmc_E']*10000 # .round(4)
df['klmc_E'] = df['klmc_E'].astype(int)
df['klmc_E'] = df['klmc_E']/10000

re_gulp = df['re_gulp_E'].tolist()
klmc_E = df['klmc_E'].tolist()

indexes = list(range(1, int(len(xyz)/2)+1))

print("################################")
#NEW_gulp = [x for x in re_gulp if x not in klmc_E]
#NEW_gulp = [np.nan if x in NEW_gulp else x for x in indexes]
NEW_gulp =  ["#" if x in klmc_E else np.nan for x in re_gulp]
df['missing_gulp'] = NEW_gulp
print("################################")

#print(df)
df.to_csv('./scratch_and_gulp.csv') 


# ==================================================================================

'''
Using hashkey to filter duplicate structures 
'''

#xyz = get_files('./xyzFiles', '.xyz')  #get_xyz('./xyzFiles')
#xyz = sorted(xyz) #xyz.sort()

pairing = [['./xyzFiles/' + xyz[i], './xyzFiles/' +  xyz[i+1]] for i in range(0, len(xyz), 2)]
hkg_path = '/home/uccatka/software/hkg/hkg.py'

print(pairing)

print()
print("----aims----")
aims = []
for num, i in enumerate(pairing):
    i.sort()
    AIMS = subprocess.check_output(["python", hkg_path, i[0], radius])
    AIMS = str(AIMS)[2: -3]
    aims.append(AIMS)
    #if num +1 // 10 == 0:
    print(i[0], AIMS)

print()

#print("----klmc----")
#klmc = []
#for j in pairing:
#    KLMC = subprocess.check_output(["python", hkg_path, j[0], radius])
#    KLMC = str(KLMC)[-2: -3]
#    print(j[0], KLMC)
#    klmc.append(KLMC)

aims_xyz = [i[0].split('/')[2].split('_')[0] for i in pairing]

#indexes = list(range(1, int(len(xyz)/2)+1))

duplicates = list(set([x for x in aims if aims.count(x) > 1]))
Pairs = []
if len(duplicates) == 0:
    print("There is no duplicated structures among the 'aims' set")

else:
    print(f"Lists of duplicated structures :")

    unique_pair = [(i+1, aims.index(aims[i])+1) for i in range(len(aims)) if not i == aims.index(aims[i])]
    
    #dummy = [i+1 for i in range(len(aims)) if not i == aims.index(aims[i])]
    #print("print dummy")
    #print(dummy)
    #print(len(dummy))
    print(unique_pair)

    dup_list = [i[0] for i in unique_pair]
    unique_indexes = [np.nan if x in dup_list else x for x in indexes]
    with open('rank.txt', 'w') as f:
        for num, i in enumerate(unique_indexes):
            f.write(str(aims_xyz[num]) + ' ' +  str(i) + '\n')
            print(f'{i}')

 
df['aims_unique'] = unique_indexes 
df.to_csv("scratch_and_gulp_hash.csv")
df = df.dropna()
df = df.drop(columns=['aims_unique'])
df = df.round({'delta_(a)': 8, 'delta_(k)': 8})



# ==================================================================================



print(df)
df.to_csv('./uniq_str_info.csv')





