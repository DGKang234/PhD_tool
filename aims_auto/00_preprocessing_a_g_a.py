
import os

target = os.getcwd()
target = target.replace('/scratch/scratch/uccatka', '/home/uccatka/Scratch')

path =  target + '/gulp_xyz/'

os.chdir(path)
x = [x for x in os.listdir('./') if '.xyz' in x]
y = sorted(x, key=lambda x : x.split('_')[0])

for i in y:    
    rank_xyz = i.split('_')[0]
    rename = rank_xyz + '.xyz'
    os.rename(i, rename)



