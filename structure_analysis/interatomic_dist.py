import numpy as np
def load_xyz(xyz_file):

    with open(xyz_file, 'r') as f:
        lines = f.readlines()

        c1_n = int(lines[0])                                       # number of atoms
        del lines[0]                                               # del num of atoms
        del lines[0]                                               # del energy

        coord = [x.split() for x in lines]                         # split into atom species, x, y, z coordinate
        coord = np.asarray(coord)                                  # transform into numpy array
        
        Coord = []
        
        ## condition
        #for i in coord:
        #    if 'Br' not in i:
        #        Coord.append(i)
        
        Coord = np.array(Coord)
        ID = Coord[:, 0]                                            # atom species
        Coord = Coord[:, 1:].astype(float)                          # atom position
        print(Coord)
        dummy_atom = np.zeros((1,3), dtype=float)                   # empty array

        distances = []
        for numi, i in enumerate(Coord):
            for numj, j in enumerate(Coord):
                dist = round(np.linalg.norm(i-j), 2)
                if dist != 0 and dist < 3:
                    distances.append(dist)
                    print(numi, numj, i, j, dist)
    
    distances = list(set(distances))
    distances.sort()
    print("### Unique set of interatomic distances ###")
    print(distances)
                


xyz_file = input("which interatomic distnace of .xyz file would you like to calculate? : ")
load_xyz(xyz_file)
