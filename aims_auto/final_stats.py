
import os, sys
import pandas as pd
import numpy as np
import subprocess

def grep_out(loc, out = 'aims.out'):
    contents = [loc + x for x in os.listdir(loc) if out in x]
    contents = ''.join(contents)
    return contents

def get_files(A='./', B=''):
    files = [x for x in os.listdir(A) if B in x]
    return(files)

radius = sys.argv[1]
output_group = './ranked/'
sp_marker = '| Total energy                  :'
final_marker = '| Total energy of the DFT / Hartree-Fock s.c.f. calculation      :     '
klmc_marker = 'SCF Done'

dir_list = [output_group + x + '/' for x in os.listdir(output_group) if os.path.isdir(output_group + x)]
dir_list.sort()

out_full_path = list(map(grep_out, dir_list))

collection_sp_E = []
collection_final_E = []

for num, i in enumerate(out_full_path):
    with open(i, 'r') as f:
        lines = f.readlines()
        sp_from_each_file = [x.split('Ha      ')[1].split(' ')[0] for x in lines if sp_marker in x]
        final_from_each_file = [x.split(':         ')[1].split(' ')[0] for x in lines if final_marker in x]
        
        print(i) 
        collection_sp_E.append(sp_from_each_file[0])
        collection_final_E.append(final_from_each_file[0])
        

df = pd.DataFrame(columns = ['IP_rank', 'SP_E', 'Final_E'])

ensemble_dir = [x.split('/')[2] for x in out_full_path]
df['IP_rank'] = ensemble_dir 
df['SP_E'] = collection_sp_E
df['SP_E'] = df['SP_E'].astype('float')
df['Final_E'] = collection_final_E
df['Final_E'] = df['Final_E'].astype('float')
df['delta_(a)'] = df['Final_E'] - df['Final_E'].min()
df['aims_R'] = df['Final_E'].rank().astype('int')

df = df[['aims_R', 'SP_E', 'Final_E', 'delta_(a)']]
pd.set_option("display.max_rows", None, "display.max_columns", None)

klmc_xyz = [x.split('/')[2] + '.xyz' for x in out_full_path]
klmc_full_path = list(map(grep_out, dir_list, klmc_xyz))

collection_klmc_E = []
for i in klmc_full_path:
    with open(i, 'r') as f:
        lines = f.readlines()
        sme_from_each_file = [x.split('            ')[1].split('\n')[0] for x in lines if klmc_marker in x]
        collection_klmc_E.append(sme_from_each_file[0])
df['klmc_E'] = [float(x) for x in collection_klmc_E] 
df['delta_(k)'] = df['klmc_E'] - df['klmc_E'].min()
df['klmc_R'] = df['klmc_E'].rank().astype('int')

df = df[['aims_R', 'SP_E', 'Final_E', 'delta_(a)', 'klmc_R', 'klmc_E', 'delta_(k)']]
print(df)






'''
hashkey section
'''

xyz = get_files('./xyzFiles', '.xyz')  #get_xyz('./xyzFiles')
xyz = sorted(xyz) #xyz.sort()

pairing = [['./xyzFiles/' + xyz[i], './xyzFiles/' +  xyz[i+1]] for i in range(0, len(xyz), 2)]
hkg_path = '/home/uccatka/software/hkg/hkg.py'


print()
print("----aims----")
aims = []
for i in pairing:
    AIMS = subprocess.check_output(["python", hkg_path, i[0], radius])
    AIMS = str(AIMS)[2: -3]
    print(i[0], AIMS)
    aims.append(AIMS)
print()

#print("----klmc----")
#klmc = []
#for j in pairing:
#    KLMC = subprocess.check_output(["python", hkg_path, j[0], radius])
#    KLMC = str(KLMC)[-2: -3]
#    print(j[0], KLMC)
#    klmc.append(KLMC)

aims_xyz = [i[0].split('/')[2].split('_')[0] for i in pairing]

indexes = list(range(1, int(len(xyz)/2)+1))
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
 
df['aims_unique'] = unique_indexes 
df = df.dropna()
df = df.drop(columns=['aims_unique'])
df = df.round({'delta_(a)': 8, 'delta_(k)': 8})
print(df)
df.to_csv('./uniq_str_info.csv')


