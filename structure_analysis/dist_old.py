import numpy as np
import os

def cat_ani_dist(XYZ, size):

    temp1 = "temp_1"
    temp2 = "temp_2"
    temp3 = "temp_3"
    s1 = ' '

    with open(XYZ, 'r') as f:
        lines = f.readlines()
        l1 = lines[2 :]
        str1 = s1.join(l1)
        with open(temp1, 'w') as f:
            f.write(str1)

    with open(temp1, 'r') as f:
        print('Cartesian coordinates of atoms are:\n ')
        for line in f:
            l2 = line.split()[1: 4]
            s2 = '\t'
            str2 = s2.join(l2)
            print(str2)
            with open(temp2, 'a') as f:
                f.write (str2 + '\n')
            f.close()
        print('\n')

    array = np.loadtxt(temp2)
    cat = array[0:int(size)]
    ani = array[int(size):]
    print("\n")

    bond_dist=[]
    with open(temp3, 'w') as f:
        for c in cat:
            for a in ani:
                dist = np.sqrt(np.sum((c-a)**2))
                if dist < float(2.3):
                    f.write(str(dist)+'\n')
                    bond_dist.append(dist)

    bond_dist.sort(key=float)
    for i in bond_dist:
        print(i)

    with open(temp3, 'r') as f:
        array = np.loadtxt(temp3)
        average = np.average(array)
        print("\nThe average bond length is : " + str(average))
        print()
    os.remove(temp1)
    os.remove(temp2)
    os.remove(temp3)

name = input("name of the .xyz file ? : (type only the file name without '.xyz') ")
size = input("size of the nanocluster ? : ")
size = str(int(size)*1)                 # "int" to number of cation in a system
cwd = os.getcwd()
XYZ = cwd + '/' + str(name) + '.xyz'

cat_ani_dist(XYZ, size)
