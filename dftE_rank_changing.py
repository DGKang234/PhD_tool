import os
import pandas as pd
import itertools, re, glob
import time

start = time.time()
def get_dir(A='./'):
    global dir_
    dir_ =  [str(os.path.join(A, x)) for x in os.listdir(A) if os.path.isdir(os.path.join(A, x))]
    dir_.sort()
    return dir_

def get_files(A='./', B=''):
    global files
    files = [x for x in os.listdir(A) if B in x]
    return(files)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text)]



get_dir('./ranked')

files_ = [get_files(x, '.out') for x in dir_]
files_ = list(itertools.chain(*files_))
files_ = list(set(files_))
#files_.remove('a.out')
files_.sort(key=natural_keys)

#print(files_)
#print(dir_)

frame_df = pd.DataFrame(columns={'aims R','klmc R', 'aims E'})
for i in dir_:
    for j in files_:
        aim = os.path.join(f'{i}/{j}')
        for name in glob.glob(aim):
            with open(name) as f:
                lines = f.readlines()
            for line in lines:
                if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation      :' in line:
                    aims_e = line.split('         ')[1]
                    aims_e = aims_e.split(' ')[0]

                    klmc_R = name.split('/')[2]
                    print(klmc_R, aims_e)
                    frame_df = frame_df.append({'klmc R': int(klmc_R), 'aims E':aims_e}, ignore_index=True) 

frame_df = frame_df.sort_values(by=['aims E'], ascending=False)
frame_df = frame_df.reset_index()
frame_df['aims R'] = frame_df.index + 1
frame_df = frame_df.drop(columns=['index'])
frame_df = frame_df[['aims E', 'aims R', 'klmc R']]
print(frame_df) 
frame_df.to_csv('aims_klmc.csv', index = False)

end = time.time()
print(f'\nTotal time {end-start}')


