import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from itertools import combinations


binwidth = 0.05
sig2 = 0.001

name = sys.argv[1]

ipf= name + '.xyz'
if os.path.exists(ipf) != True:
    print(f"{ipf} doesn't exist")
    sys.exit()

with open(ipf, 'r') as f:
    lines = f.readlines()
    del lines[0:2]

array = [x.split() for x in lines]
array = np.asarray(array)
coord = array[:, 1:].astype(float)

ID = coord[:, 0]
ID_set = list(set(ID))

#pairs = [",".join(map(str, comb)) for comb in combinations(coord, 2)]
#pairs = [np.asarray(comb) for comb in combinations(coord, 2)]
npairs = 0
for numi, i in enumerate(coord):
    for numj, j in enumerate(coord):
        if numi != numj:
            npairs += 1

# Calculate the interatomic disntaces
all_dist = []
#for numi, i in enumerate(pairs):
#     dist = round(np.linalg.norm(i[0]-i[1]), 4)
#     all_dist.append(dist)

a=0
for numi, i in enumerate(coord):
    for numj, j in enumerate(coord):
        if numi != numj:
            distance = np.round(np.linalg.norm(i-j), 6)
            all_dist.append(distance)

# Prepare the bin
tmp = np.ceil(max(all_dist)) + 1
tmp = tmp/binwidth
nbins = int(round(tmp, 0) + 1)

num = 0.0
opdata = [0.0]
for i in range(nbins-1):
    num += binwidth
    opdata.append(round(num, 2))



# Binning the data
opdata_2 = {}
val = 1
for i in range(nbins-2):
    upper = opdata[i+2]
    lower = opdata[i+1]

    opdata_2[lower] = 1
    for j in range(npairs):
        dist = all_dist[j]
        if lower <= dist <= upper:
            opdata_2[lower] = opdata_2[lower] + 1



def gaussian(x, b, sigma2):
    pi = np.arccos(-1.0)
    sigma = np.sqrt(sigma2)
    prefix = 1.0/(sigma * np.sqrt(2.0 * pi))
    power = ((x-b)/sigma)**2
    power = power * (-0.5)
    prefix = 1.0
    gx = prefix * np.exp(power)
    return gx 

# Gaussian smearing
opdata_3 = []
for i in range(nbins):
    g = 0.0
    for j in range(npairs):
       tmp = 0
       x = opdata[i]
       b = round(all_dist[j], 10)
       tmp = gaussian(x,b,sig2)
       g = g + tmp
    opdata_3.append(g)

# Normalisation
csum = 0
for i in range(nbins):
    csum = csum + opdata_3[i]
opdata_4 = []
opdata_3 = np.array(opdata_3)
opdata_4 = opdata_3/csum
opdata_5 = opdata_3/len(ID)

print(type(opdata), type(opdata_5))
#opdata = opdata.tolist()
opdata_5 = opdata_5.tolist()

with open('output.csv', 'w') as f:
    f.write('r (A),  g(r) normalised by natoms\n')
    for i in range(nbins):
        f.write(f'{opdata[i]}, {opdata_5[]}\n')





# plotting using plotly
#pip install plotly

import plotly.express as px
import pandas as pd

dff = pd.read_csv('output.csv')
fig = px.line(dff, x=dff.columns[0], y=dff.columns[1], title=None)
fig.show()


