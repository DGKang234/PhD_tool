import sys
import numpy as np
import time


def cat_an_interatomic_dist(xyz_file):
    with open(xyz_file, 'r') as f:
        lines = f.readlines()
    
        c1_n = int(lines[0])                           # number of atoms
        del lines[0]                                   # del num of atoms
        del lines[0]                                   # del energy
        
        coord = [x.split() for x in lines]             # split into atom species, x, y, z coordinate
        coord = np.asarray(coord)                      # transform into numpy array
        
        ID = coord[:, 0]
        ID_set = list(set(ID))
        
        # condition
        A_species = []
        B_species = []
        for i in coord:
            if ID_set[0] not in i:
                A_species.append(i)
            else:
                B_species.append(i)
        
        A_species = np.array(A_species)[:, 1:].astype(float)
        B_species = np.array(B_species)[:, 1:].astype(float)
        
        distances = []
        every_dist = []
        for numi, i in enumerate(A_species):
            for numj, j in enumerate(B_species):
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0 and dist < 3:
                    distances.append(dist)
                if dist !=0:
                    every_dist.append(dist)

        for numi, i in enumerate(A_species):
            for numj, j in enumerate(A_species):
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0: #and dist < 5:
                    every_dist.append(dist)

        for numi, i in enumerate(B_species):
            for numj, j in enumerate(B_species):
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0: #and dist < 5:
                    every_dist.append(dist)
                    
    every_dist.sort()
    distances.sort() 
    shortest_dist = distances[0]
    longest_dist = distances[-1]
    average_dist = round(sum(distances)/len(distances), 4)
    
    return average_dist, every_dist, shortest_dist, longest_dist

try:
    xyz_file = sys.argv[1]
except IndexError: 
    print("================================================================= ")
    print("Please submit an argument (.xyz file) when you execute the code ")
    print("================================================================= ")
    sys.exit()

start = time.process_time()
average, every, shortest, longest = cat_an_interatomic_dist(xyz_file)
print(f"----- process time : {time.process_time() - start} seconds -----")
print()
print("Average dist")
print(average)
print()
print("shortest dist")
print(shortest)
print()
print("Longest dist")
print(longest)
print()
print('Every dist')
print(every)





