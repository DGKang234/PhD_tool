import os, subprocess
import pandas as pd


def get_xyz(A='./', B='.xyz'):
    global xyz
    xyz = [x for x in os.listdir(A) if B in x]
    return xyz


radius = input("set hashkey radius : ")
get_xyz('./xyzFiles')
xyz.sort()
print(xyz)

pairing = [['./xyzFiles/' + xyz[i], './xyzFiles/' +  xyz[i+1]] for i in range(0, len(xyz), 2)]
hkg_path = '/home/uccatka/software/hkg/hkg.py'

print()
print("----aims----")
aims = []
for i in pairing:
    AIMS = subprocess.check_output(["python", hkg_path, i[0], radius]) 
    print(i[0], AIMS)
    aims.append(AIMS)

print()    
print("----klmc----")
klmc = []
for j in pairing:
    KLMC = subprocess.check_output(["python", hkg_path, j[0], radius])
    print(j[0], KLMC)
    klmc.append(KLMC)

print()
for num, a in enumerate(aims):
    if a in klmc:
        loc_klmc = klmc.index(a) + 1
        print(f'aims {num+1} rank structure is same as klmc {loc_klmc} rank')
    else:
        print(f"{num+1} doesn't exist in KLMC set")


print()
duplicates = list(set([x for x in aims if aims.count(x) > 1]))
if len(duplicates) == 0:
    print("There is no duplicated structures among the 'aims' set")
else:
    print(f"Lists of duplicated structures :")
    for num_el, el in enumerate(aims):
        for num_a, a in enumerate(aims):
            if el == a:
                if num_el != num_a:  
                    print('duplicated {aims} structures : ' + str(num_el + 1) + ' == ' + str(num_a + 1) + ' ' + str(a))
print() 
