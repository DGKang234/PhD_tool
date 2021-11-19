import os, subprocess
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as mplcm

import itertools, re, glob
import time

pre_dup = input("Would you like to delete any duplicated aims structures? \
(type rank of aims (delimeter whitespace) : ")
if len(pre_dup) > 0:
    pre_dup = pre_dup.split(',')
    
else:
    pre_dup = []

radius = input("set hashkey radius (this can be vary depends on the size of clusters) : ")
#SIZE = input("What is the size of the cluster : ")
TOP_10 = input("Would you like to plot top 10 aims to klmc connection only ? (y or default n) : ")
yes = ['yes', 'y']
NUM_COLOURS = input("How many colour would you like to use? : (default 100) ")

start = time.time()

if len(str(NUM_COLOURS)) == 0:
    NUM_COLOURS = 100
else:
    NUM_COLOURS = int(NUM_COLOURS)

def get_dir(A='./'):
    global dir_
    try:
        dir_ =  [str(os.path.join(A, x)) for x in os.listdir(A) if os.path.isdir(os.path.join(A, x))]
        dir_.sort()
    except FileNotFoundError:
        print("Probably you are in wrong directory to run the code")
    return dir_

def get_files(A='./', B=''):
    global files
    files = [x for x in os.listdir(A) if B in x]
    return(files)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text)]

###########
# hashkey #
###########

def get_xyz(A='./', B='.xyz'):
    global xyz
    xyz = [x for x in os.listdir(A) if B in x]
    return xyz

#radius = input("set hashkey radius : ")
get_xyz('./xyzFiles')
xyz.sort()


pairing = [['./xyzFiles/' + xyz[i], './xyzFiles/' +  xyz[i+1]] for i in range(0, len(xyz), 2)]
hkg_path = '/home/uccatka/software/hkg/hkg.py'

print()
print("----aims----")
aims = []
for i in pairing:
    AIMS = subprocess.check_output(["python", hkg_path, i[0], radius])
    AIMS = str(AIMS)
    #AIMS = AIMS[2:-3]
    print(i[0], AIMS)
    aims.append(AIMS)
print()

with open('aims_hashkey.txt', 'w') as f:
    for i in range(len(aims)):
        f.write(aims[i]+'\n')



'''
print("----klmc----")
klmc = []
for j in pairing:
    KLMC = subprocess.check_output(["python", hkg_path, j[0], radius])
    KLMC = str(KLMC)
    KLMC = KLMC[2:-3]
    print(j[0], KLMC)
    klmc.append(KLMC)
print()
'''



aims.append(pre_dup)
print("print aims")
aims = aims[:-1]
print(aims)
print(len(aims))
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


    for num_el, el in enumerate(aims):
        for num_a, a in enumerate(aims):
            if el == a:                 # if hashkey is identical
                if num_el != num_a:     # elimininate the case that recognise the same 
                                        # ranked structure as duplicated case e.g. 1 = 1, 2 = 2 
                    Pairs.append([num_a+1, num_el+1])   # paired as tuple
                    unique_pair = list(set((a,b) if a <= b else (b, a) for a, b in Pairs))
                    # sort as (lesser rank, higher rank) 
unique_pair.sort(key=lambda x:x[0])

result = []
l = unique_pair
if len(l) > 1:
  tmp = [l[0]]
  for i in range(1,len(l)):
    if l[i][0] == l[i-1][1] or l[i][1] == l[i-1][0] or l[i][1] == l[i-1][1] or l[i][0] == l[i-1][0]:
      tmp.append(l[i])
    else:
      result.append(tmp)
      tmp = [l[i]]
  result.append(tmp)
else:
  result = l


for elem in result:
    print(elem)
print()


#############
# bipartite #
#############
get_dir('./ranked')

files_ = [get_files(x, 'aims.out') for x in dir_]
files_ = list(itertools.chain(*files_))
files_ = list(set(files_))
files_.sort(key=natural_keys)

frame_df = pd.DataFrame(columns={'aims_R','klmc_R', 'aims_E'})
range_ = [x for x in os.listdir('./xyzFiles/')]
range_ = list(set(x.split('_')[0] for x in range_))

for i in range_:
    for j in files_:
        aim = os.path.join(f'./ranked/{i}/{j}')
        for name in glob.glob(aim):
            with open(name) as f:
                lines = f.readlines()
            for line in lines:
                if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation      :' in line:
                    aims_e = line.split('         ')[1]
                    aims_e = aims_e.split(' ')[0]

                    klmc_R = name.split('/')[2]
                    frame_df = frame_df.append({'klmc_R': int(klmc_R), 'aims_E':aims_e},
                     ignore_index=True)

frame_df = frame_df.sort_values(by=['aims_E'], ascending=False)
frame_df = frame_df.reset_index()
frame_df['aims_R'] = frame_df.index + 1
frame_df = frame_df.drop(columns=['index'])
frame_df = frame_df[['aims_E', 'aims_R', 'klmc_R']]
print("### After {aims} optimisation ###")
print(frame_df)
print()
frame_df.to_csv('for_bipartite.csv', index = False)

##########################
# unique structures only #
##########################

temp_df = frame_df

top_str = './xyzFiles/'
top_xyz = [ top_str + x for x in os.listdir(top_str) if 'klmc.xyz' in x]
top_xyz.sort()

K_energy = []
for x in top_xyz:
    with open(x, 'r') as f:
        for num, line in enumerate(f):
            if num == 0:
                k_energy = f.readline()     
                k_energy = k_energy.split()[2] 
                K_energy.append(k_energy)

temp_df = temp_df.sort_values(by=['klmc_R'], ascending=True)
temp_df['klmc_E'] = np.array(K_energy)
temp_df = temp_df.sort_values(by=['aims_R'], ascending=True)
temp_df = temp_df[['aims_R', 'aims_E', 'klmc_R', 'klmc_E']]


dummy = []
if len(result) == 1:
    dummy.append(elem[1])
else:
    for elem in result:
        for a, b in elem:
            dummy.append(b)


del_list = []
for index, row in temp_df.iterrows():
    for e in dummy:
        if e == row['aims_R']:
            try:
                del_list.append(e)
                temp_df.drop(index, inplace = True)
            except Exception:
                pass

for i in del_list:
    try:
        temp_df.drop(index, inplace = True)
    except Exception:
        pass

temp_df.reset_index(drop=True, inplace=True)
temp_df.to_csv('unique_energy.csv', index = False)
#print("### duplicated {aims} rank ###")
#print(aims)
print("### Unique set ###")
print(len(list(set(del_list))), list(set(del_list)))
print()
print(temp_df)

######################
# Call the .csv file #
######################
# Generated from 'get_energy.py' (alias: rank (thomas))
data = './for_bipartite.csv'

####################
# Helper Functions #
####################
def addconnection(i,j,c):
  return [((-1,1),(i,j),c)]

def drawnodes(s,i):
  global ax
  if(i==1):    # right-hand side
    color='g'
    posx=1
  elif (i==2):
    color='b'  # left-hand side
    posx=-1

  posy=0
  for n in s:
    plt.gca().add_patch(plt.Rectangle((posx,posy+0.85),width=0.02,height=0.3,fc=color))    # tick marks (patch)

    ###############################
    # position of label of marker #
    ###############################
    if posx==1:  
        if int(n) % 100 == 0:
            ax.annotate(n,xy=(posx+0.08,posy+1))     # label of tick marks
    elif posx==-1:         # location of left-hand side
        if int(n) % 100 == 0:
            #ax.annotate(n,xy=(posx-len(n)*0.043,posy+1))
            ax.annotate(n,xy=(posx-0.1, posy+1))
    posy+=1

####################################################

fig = plt.figure(figsize=(30, 16))      #15, 8))
ax = fig.add_subplot(111)
ax.axis("off")

######################
#  Actual rank data  #
######################
df = pd.read_csv(data)  #'aims_klmc.csv')
aims_rank = df['aims_R']
aims_max = np.array(aims_rank)
A = aims_rank

klmc_rank = df['klmc_R']
klmc_rank = np.array(klmc_rank)
K = klmc_rank

############
#  MARKER  #
############
klmc_order = range(1, len(klmc_rank)+1)
klmc_set=[]
for r in klmc_order:
    klmc= f'{r}'
    klmc_set.append(klmc)

aims_order = range(1, len(aims_rank)+1)
aims_set=[]
for r in aims_order:
    aims = f'{r}'
    aims_set.append(aims)

plt.axis([-1.5,1.5,-1,max(len(klmc_order),len(aims_order))+1])
frame=plt.gca()
frame.axes.get_xaxis().set_ticks([])
frame.axes.get_yaxis().set_ticks([])

drawnodes(klmc_set,1)
drawnodes(aims_set,2)

################################
# axis title position settings #
################################
ax.text(-1.3, 20, 'PBEsol\n rank', style='italic', fontsize = 15)
ax.text(1.2, 20, 'Shell model\n rank', style='italic', fontsize = 15)

#########################################
# concatenate aims rank and klmc rank #
#########################################
connections = []
for i, j in zip(A, K):
    a =  str(i) + ',' + str(j)
    connections.append(a)

b = ','.join(connections)
c = b.split(',')

klmc_ = []
aims_ = []
for count, i in enumerate(c):
    if (count % 2 != 0):    # even numbered elements are the klmc rank
        klmc_.append(i)
    else:
        aims_.append(i)  # odd numbered elements are the aims rank


#########################################
#            Drawing lines              #
#########################################

cm = plt.get_cmap('gist_rainbow')
cNorm  = colors.Normalize(vmin=0, vmax=NUM_COLOURS-1)
scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)

connections = []
for count, i in enumerate(range(1,len(aims_rank)+1)):
            elements = (-0.97, 0.99), (int(aims_[i-1]), int(klmc_[i-1]))
            # position of right-end of the line
            connections.append(elements)

for count, c in enumerate(connections):
    fig = plt.plot(c[0],c[1]) #,c[2])
    fig[0].set_color(cm(count//3*3.0/NUM_COLOURS))

    if TOP_10 in yes:
        if count == 9:
            print(f"plot bipartite up to {count}")
            break
    else:
        continue

file_name = os.getcwd().split('/')[-1]
#plt.show()
plt.savefig(f'{file_name}_RchangingAnalysis.pdf')

end = time.time()
print(f'\nTotal time: {end}')




