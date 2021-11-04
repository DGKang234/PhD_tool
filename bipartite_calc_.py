import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as mplcm

import itertools, re, glob
import time

TOP_10 = input("Would you like to plot top 10 aims to klmc connection only ? (y or default n) ")
yes = ['yes', 'y']
NUM_COLOURS = input("How many colour would you like to use? : (default 100) ")

start = time.time()

if len(str(NUM_COLOURS)) == 0:
    NUM_COLOURS = 100
else:
    NUM_COLOURS = int(NUM_COLOURS)

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

frame_df = pd.DataFrame(columns={'aims_R','klmc_R', 'aims_E'})
for i in dir_:
    for j in files_:
        aim = os.path.join(f'{i}/{j}')
        for name in glob.glob(aim):
            with open(name) as f:
                lines = f.readlines()
            for line in lines:
                if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation      :' in line:
                    aims_e = line.split('        ')[1]
                    aims_e = aims_e.split(' ')[0]

                    klmc_R = name.split('/')[2]
                    print(klmc_R, aims_e)
                    frame_df = frame_df.append({'klmc_R': int(klmc_R), 'aims_E':aims_e}, ignore_index=True)

frame_df = frame_df.sort_values(by=['aims_E'], ascending=False)
frame_df = frame_df.reset_index()
frame_df['aims_R'] = frame_df.index + 1
frame_df = frame_df.drop(columns=['index'])
frame_df = frame_df[['aims_E', 'aims_R', 'klmc_R']]
print(frame_df)
frame_df.to_csv('for_bipartite.csv', index = False)


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
    #plt.gca().add_patch(plt.Circle((posx,posy+1), 0.1, fc=color))

    ###############################
    # position of label of marker #
    ###############################
    if posx==1:  
        if int(n) % 10 == 0:
            ax.annotate(n,xy=(posx+0.08,posy+1))     # label of tick marks
    elif posx==-1:         # location of left-hand side
        if int(n) % 10 == 0:
            #ax.annotate(n,xy=(posx-len(n)*0.043,posy+1))
            ax.annotate(n,xy=(posx-0.1, posy+1))
    posy+=1

####################################################

fig = plt.figure(figsize=(15, 8))
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
ax.text(-1.3, 20, 'aims\n rank', style='italic', fontsize = 15)
ax.text(1.2, 20, 'klmc\n rank', style='italic', fontsize = 15)

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
    print(c)
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

