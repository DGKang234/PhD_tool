import os
import numpy as np
import pandas as pd
from colored import fg, bg, attr

name = input("input file name? : ") 

pd.set_option('display.max_rows', None)


def gout_load_xyz(name):
    
    with open(name, 'r') as f:
        lines = f.readlines()
    
    for lnum, line in enumerate(lines):
        if 'cartesian coordinates of atoms :' in line:
            sline = lnum+6
        if 'Final Cartesian derivatives :' in line:
            eline = lnum-4
        if 'Species    Type' in line:
            cline = lnum+3
   
    charge = []
    for line in range(cline, cline+3):
        charge.append(float(lines[line].strip().split()[4]))
        chrage = list(charge)
    #print(charge)
    cartesian = []
    for line in range(sline, eline+1):
        cartesian.append(lines[line].strip())
   
    num_particle = cartesian[-1].split()[0]
    coord = [x.split() for x in cartesian]
    coord = np.array(coord)

    ID = list(coord[:, 1])
    CS = list(coord[:, 2])
    ID_CS = np.stack((ID, CS), axis=1)
    ID_CS = pd.DataFrame((ID_CS), columns=['ID', 'CS'])

    used = set()
    ID_list = [x for x in ID if x not in used and (used.add(x) or True)] 
    used = set()
    CS_list = [x for x in CS if x not in used and (used.add(x) or True)]
   
    #print(ID_list, CS_list, charge)
    q = []
    for index, row in ID_CS.iterrows():
        if ID_CS.at[index, 'ID'] == ID_list[0]:
            q.append(charge[0]) 
        elif (ID_CS.at[index, 'ID'] == ID_list[1] and  ID_CS.at[index, 'CS'] == CS_list[0]):
            q.append(charge[1])
        elif (ID_CS.at[index, 'ID'] == ID_list[1] and ID_CS.at[index, 'CS'] == CS_list[1]):
            q.append(charge[2])
  
    ID_CS['q'] = q
    ID_CS_q = ID_CS 
    #print(ID_CS_q)
    orig_coord = coord[:, 3:6].astype(np.float)

    return ID_CS_q,  num_particle, orig_coord
       

def CenterofMass(num_particle, orig_coord):
    com = np.zeros((1,3))
    com = orig_coord.sum(axis=0)                                            # sum all cartesian coordinates
    com = com / float(num_particle)                                         # divided into number of atoms (mass of every atom = 1)
    print(com)
    return com



def Transformation(ID_CS_q, com):
    coord_x = np.subtract(orig_coord[:, 0], com[0], out=orig_coord[:, 0])    # subtract all of x coordinate with x coordinate of com. same for all y, z
    coord_y = np.subtract(orig_coord[:, 1], com[1], out=orig_coord[:, 1])
    coord_z = np.subtract(orig_coord[:, 2], com[2], out=orig_coord[:, 2])
    coord = list(zip(coord_x, coord_y, coord_z))                             # zip the subtracted coordinates into one list
    coord = np.array(coord)                                                  # transform into array
    coord = pd.DataFrame(coord, columns=['x','y','z'])
    coord = pd.concat([coord, ID_CS_q], axis=1)
    coord = coord[['ID', 'CS', 'x', 'y', 'z', 'q']]
    #print(coord)
    return coord


def Dipole_moment(ID_CS_q, coord):
    O = np.zeros(3)
    coord['qx'] = (np.multiply(coord.iloc[:, [2]].values, coord.iloc[:,[5]].values))
    coord['qy'] = (np.multiply(coord.iloc[:, [3]].values, coord.iloc[:,[5]].values))
    coord['qz'] = (np.multiply(coord.iloc[:, [4]].values, coord.iloc[:,[5]].values))

    qx = coord['qx'].sum()
    qy = coord['qy'].sum()
    qz = coord['qz'].sum()

    Mu = np.sqrt(qx**2 + qy**2 + qz**2)    

    return Mu, coord
 
ID_CS_q, num_particle, orig_coord = gout_load_xyz(name)
com = CenterofMass(num_particle, orig_coord)
coord = Transformation(ID_CS_q, com)
Mu, coord =Dipole_moment(ID_CS_q, coord)

print(coord)
print()
print(f"{fg(1)} {bg(15)} Dipole moment unit need to be changed (it's in e Å) : {Mu} {attr(0)}") 
print()


