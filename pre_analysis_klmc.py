import time
import os
import re
import shutil
import glob
import pandas as pd
import numpy as np

start = time.time()
def get_dir(A='./', B=''):
    global dir_
    dir_ = [x for x in os.listdir(A) if os.path.isdir(x) == True]
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

if os.path.exists('./top_structures'):
    shutil.rmtree('top_structures')


get_uniq_xyz = input("Would you like to download the unique set of {.xyz} files? (default no) :")
get_uniq_xyz.lower()


get_dir()
dir_.sort(key=natural_keys)
#dir_.remove('dummy')
root = os.getcwd()
top = "/top_structures"
stat = "/statistics"
dest = "./statistics"

if os.path.exists(dest) == True:
    shutil.rmtree(dest)
    os.mkdir(dest)
else:
    os.mkdir(dest)

dir_.remove('statistics')

"""organise 'statistics' file into statistics directory"""
for d in dir_:
    from_ = os.path.join(root, d + top + stat)
    shutil.copy(from_, dest + '/' + d + '_statistics')

"""remove preprocessed.csv"""
get_files(dest, 'preprocessed.csv')
if len(files) > 0:
    for i in files:
        os.remove(i)
else:
    pass


get_files(dest, 'statistics')
files.sort(key=natural_keys)

print("\n\nThis is the overall output from the indiviudal calculation")
print("/// M /// 1st(ID) /// X /// min(n) /// LMrank_min(n) /// valid ///")
for f in files:
    stat_file = f
    label = stat_file.split('_')[0]             # 1 2 3 4 5 6 7 ...

    """statistics file"""
    a_file = open(dest + '/' + stat_file)       # statistics file.
    lines = a_file.readlines()
    lines = [item for item in lines if 'x' not in item]
    a_file.close()
    if len(lines[0]) < 18:
            del lines[0]    #delete the first line (number of stored data)
    new_file = open(dest + '/' + stat_file, "w+")
    for line in lines:
        new_file.write(line)
    new_file.close()

    """ call statistics file as DataFrame """
    column_label = ['rank', 'ID', 'energy', 'found']
    df = pd.read_fwf(dest + '/' + stat_file, names=column_label)
    df = df.reset_index(drop=True)

    """ round up to 7 decimal places of energy value """
    df['energy'] = df['energy'].astype(float)
    energy_ = list(df['energy'])
    energy_ = [int(x*1000000)/1000000 for x in energy_]
    df = df.assign(energy=energy_)
    df.to_csv(dest + '/' + label + "_V2.csv", index=False)

    """ Energy """
    sm_energy = df.iloc[:, 2].values

    """ freq """
    no_of_found = df.iloc[:, 3].values
    no_of_found_LM = np.argmin(no_of_found, axis=None, out=None)+1

    """ ID """
    df['ID'] = df['ID'].str.replace('B', '')
    ID = df.iloc[:, 1]
    ID = ID.astype(np.int)

    rank = int(df.index[-1]) + 1
    steps = sum(no_of_found)            # total no of steps

    """ print data """
    print(rank,  df['ID'].min(), max(ID), min(no_of_found), no_of_found_LM, steps)  #####


    """ preprocessing data for probability DOS """
    norm_no_of_found = no_of_found/steps
    gm_e = sm_energy.min()
    delta_e = sm_energy-gm_e
    pair = np.column_stack((norm_no_of_found, delta_e))
    df = pd.DataFrame({"norm_no_of_found" : norm_no_of_found, "delta_e" : delta_e})
    df.to_csv(dest + '/' + label+"_preprocessed.csv", index=False)


""" (append in a file)  Treat all independent KLMC calculation as a one calculation and give {statistics} """
get_files('statistics', 'V2.csv')
files.sort(key=natural_keys)

""" concatenating all .csv file into one """
df = pd.concat(map(pd.read_csv, glob.glob('statistics/*V2.csv')))
df['ID'] = df['ID'].str.replace('B', '')
df = df.sort_values(by=['energy', 'ID'])

energy = list(df['energy'])
energy = [int(x*100000)/100000 for x in energy]   #####
df.to_csv(dest + '/total.csv', index = False)

df_3 = df
df_3['found'] = df_3.groupby("energy")['found'].transform('sum')
df_3 = df.assign(energy=energy)                     ####
df_3 = df_3.drop_duplicates(subset=['energy'])        ####

########################################################
""" Track the {path} of the unique energy '.xyz' file """
########################################################
if get_uniq_xyz.startswith('y'):
    print() 
    print("Copying the {.xyz} files")

    df_2 = df
    df_2 = df_2.reset_index()
    df_2['rank'] = df_2.index + 1
    df_2 = df_2.drop(columns=['index'])
    
    ID = list(df_2['ID'])
    ENERGY = list(df_2['energy'])
    ENERGY = [int(x*100000)/100000 for x in ENERGY]
    ENERGY = [str(a) for a in ENERGY]
    
    get_dir()
    dir_.remove('statistics')
    dir_.sort(key=natural_keys)
    
    EE = []
    temp_df = pd.DataFrame(columns={'path', 'E'})
    for i in ID:
        for j in dir_:
            target = j + '/top_structures/B' + i
            aim = os.path.join(root, target)
            for name in glob.glob(aim + '-*'):
                with open(name) as fp:
                    for k, line in enumerate(fp):
                        if k == 1:                                  #  round up energy val. in .xyz file to 5 d.p.
                            E = float(line.split()[2])
                            E = str(int(E * 100000)/100000)
    
                            EE.append(E)
    
                            if any(E for x in ENERGY):
                                temp_df = temp_df.append({'path': name, 'E':E}, ignore_index=True)
    temp_df = temp_df.sort_values(by=['E', 'path'], ascending=False, ignore_index=True)
    temp_df.to_csv(dest + '/sub_temp_df.csv', index = False)
    temp_df = temp_df.drop_duplicates(subset=['E'], ignore_index=True)
    temp_df.to_csv(dest + '/temp_df.csv', index = False)
    
    Uniq = list(temp_df['path'])
    
    if os.path.exists('./top_structures'):
        shutil.rmtree('top_structures')
    
    if not os.path.exists('./top_structures'):
        os.mkdir('top_structures')
    
    for num, f in enumerate(Uniq):
        name = f.split('/')[-1]
        body = name.split('-')[0]
    
        dest_top = root + '/top_structures/'
        shutil.copy(f, dest_top)
    
        length = len(str(len(ID)))
        orig = dest_top + name
        change = dest_top + body
    
        if length == 2 and len(str(num+1)) < length:
            if len(str(num+1)) == 1:
                os.rename(orig, change + '-0' + str(num+1) + '.xyz')
            elif len(str(num+1)) == 2:
                os.rename(orig, change + '-' + str(num+1) + '.xyz')
    
        elif length == 3:
            if len(str(num+1)) == 1:
                os.rename(orig, change + '-00' + str(num+1) + '.xyz')
            elif len(str(num+1)) == 2:
                os.rename(orig, change + '-0' + str(num+1) + '.xyz')
            elif len(str(num+1)) == 3:
                os.rename(orig, change + '-' + str(num+1) + '.xyz')
    
        elif length == 4:
            if len(str(num+1)) == 1:
                os.rename(dest_top + name, dest_top + body + '-000' + str(num+1) + '.xyz')
            if len(str(num+1)) == 2:
                os.rename(dest_top + name, dest_top + body + '-00' + str(num+1) + '.xyz')
            if len(str(num+1)) == 3:
                os.rename(dest_top + name, dest_top + body + '-0' + str(num+1) + '.xyz')
            if len(str(num+1)) == 4:
                os.rename(dest_top + name, dest_top + body + '-' + str(num+1) + '.xyz')
        else:
            os.rename(dest_top + name, dest_top + body + '-' + str(num+1) + '.xyz')

else:
    pass


""" filter out unique energy value and sum same energy's frequency of finding"""

df['ID'] = df['ID'].replace(regex='B', value='').astype(int)
df = df.sort_values(by=['ID'], ascending=True, ignore_index=True)

df['ID_average'] = df.groupby("energy")["ID"].transform('mean').round(decimals=2)

df['energy'] = df['energy'].round(5)
df = df.drop_duplicates(subset=['energy'])
df = df.reset_index()

df = df.sort_values(by=['energy'], ascending=True, ignore_index=True)
df['rank'] = df.index + 1
df = df.drop(columns=['index'])

df['norm_n'] = df['found']/df['found'].sum()
df['norm_n'] = df['norm_n'].round(4)

df['del_E'] = df['energy'] - df['energy'].iloc[0]
df['del_E'] = df['del_E'].round(decimals = 4)

df['n_tsp/n_LM'] = df['found'].sum()/df['found']
df['n_tsp/n_LM'] = df['n_tsp/n_LM'].round(decimals = 2)

df = df[['rank', 'ID', 'ID_average', 'energy', 'found', 'norm_n', 'del_E', 'n_tsp/n_LM']]

print()
print("n number of calculations are treated as one chucky run")
print(df)
df.to_csv(dest + '/unique_total.csv', index = False)
print()


""" Check whether all runs found same number of LM """
total_no_LM = len(df)

get_files(dest, 'statistics')
files.sort(key=natural_keys)

"""statistics file"""
for stat_file in files:
    a_file = open(dest + '/' + stat_file)       # statistics file.
    lines = a_file.readlines()
    a_file.close()
    each_run_LM = len(lines)   
    run = stat_file.split('_')[0]
 
    checker = total_no_LM == each_run_LM
    if checker == True:
        qstat = str(subprocess.check_output(["qstat"]))
        qstat = qstat.split('\\n')

        job_name = os.getcwd()
        job_name = job_name.split('/')
        job_name = job_name[-2] + '/' + job_name[-1]

        for i in qstat:
            if job_name in i:
                job_id = i.split()[0]
                kill_job = subprocess.check_output(["qdel", job_id])
        print(f"{run} has found all LM")

    elif checker == False:
        print(f"{run} hasn't found all LM : " + str(each_run_LM))
    
end = time.time()
print(f'\nTotal time {end-start}')




