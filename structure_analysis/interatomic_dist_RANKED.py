import sys
import numpy as np
from colored import fg, bg, attr
import pandas as pd
import time
import os


def cat_an_interatomic_dist(xyz_file, cat, an):
    with open(xyz_file, 'r') as f:
        lines = f.readlines()

        c1_n = int(lines[0])                                       # number of atoms
        del lines[0]                                               # num of atoms
        del lines[0]                                               # energy

        coord = [x.split() for x in lines]                         # split into atom species, x, y, z coordinate
        coord = np.asarray(coord)                                  # transform into numpy array

        ID = coord[:, 0]
        ID_set = list(set(ID))
        
        #
        # condition: (cat - an distances)
        #
        cat_species = []
        an_species = []
        for i in coord:
            if an not in i:
                cat_species.append(i)
            else:
                an_species.append(i)
        
        cat_species = np.array(cat_species)[:, 1:].astype(float)
        an_species = np.array(an_species)[:, 1:].astype(float)

        hete_distances = []
        for i in cat_species:
            for j in an_species:
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0:
                    hete_distances.append(dist)
        hete_distances.sort()

        #
        # condition: (homogeneous species' interatomic distance)
        #
        cat_distances = []
        for i in cat_species:
            for j in cat_species:
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0:
                    cat_distances.append(dist)
        cat_distances.sort()
        
        an_distances = []
        for i in an_species:
            for j in an_species:
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0:
                    an_distances.append(dist)
        an_distances.sort()


        #
        # condition: ([All] heterogeneous and homogeneous species' interatomic distance)
        #
        all_distances = []
        coord_only = np.array(coord)[:, 1:].astype(float) 
        for i in coord_only:
            for j in coord_only:
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0:
                    all_distances.append(dist)
        all_distances.sort()


    shorts = []
    shorts.append(hete_distances[0])
    shorts.append(all_distances[0]) 
    shortest_dist = min(shorts)

    longs = []
    longs.append(hete_distances[-1])
    longs.append(all_distances[-1])
    longest_dist = max(longs)

    return shortest_dist, longest_dist, cat_distances, an_distances, cat, an 


# ==========================================================================

cat = sys.argv[1]
an = sys.argv[2]

pwd = os.getcwd()
pwd = pwd.replace('/scratch/scratch/uccatka', '/home/uccatka/Scratch') + '/xyzFiles/'

list_aims = [pwd + x for x in os.listdir('./xyzFiles') if 'klmc.xyz' in x] #os.path.isdir(pwd + x)]
list_aims = sorted(list_aims, key = lambda x: x.split('/')[-1].split('_')[0]) 

RANK = []
SHORT = []
LONG = []
for i in list_aims:
    shortest, longest, cat_distances, an_distances, cat, an = cat_an_interatomic_dist(i, cat, an)
    
    rank = i.split('/')[-1].split('_')[0]
    RANK.append(rank)
    SHORT.append(shortest)
    LONG.append(longest)
   
    print(f"{fg(1)} {bg(14)}{rank}{attr(0)}") 
    print(f"{fg(1)} {bg(15)}cat_species = {cat}{attr(0)}")
    print(f"{fg(1)} {bg(15)}B_speceis = {an}{attr(0)}")
    print()
    print(f"shortest dist between {cat} - {an}")
    print(shortest)
    print("longest interatomic dist")
    print(longest)
    print()
    print("shortest {cat}-{cat} and {an}-{an} distance:")
    print(f"{min(cat_distances)}, {min(an_distances)}")
    #print(cat_distances)
    #print(an_distances)
    print()
    print("longest {cat}-{cat} and {an}-{an} distance:") 
    print(f"{max(cat_distances)}, {max(an_distances)}")
    print()
    print()
    print()
     
pd.set_option("display.max_rows", None, "display.max_columns", None)
df = pd.DataFrame(columns = ['shortest', 'longest', 'IP_rank'])
df['shortest'] = SHORT
df['longest'] = LONG
df['IP_rank'] = RANK
df['IP_rank'] = df['IP_rank'].astype(int)
print(df)

df.to_csv('euc_dist.csv')



