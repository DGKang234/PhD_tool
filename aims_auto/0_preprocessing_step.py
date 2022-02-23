
import os

def func(elem):
    return int(elem.split('-')[1].split('.xyz')[0])

target = os.getcwd() 
target = target.replace('/scratch/scratch/uccatka', '/home/uccatka/Scratch')

path =  target + '/top_structures/'
dest =  target + '/ranked/'

os.chdir(path)

x = [x for x in os.listdir('./') if '.xyz' in x]

y = sorted(x, key=func)
Max = y[-1] 
Max_len = len(str(Max.split('-')[1].split('.xyz')[0]))

change = []
for xyz in y:
    
    a = str(func(xyz))
    if Max_len == 4:
        if len(str(a)) == 1:
            a = '000' + a 
        elif len(str(a)) == 2:
            a = '00' + a
        elif len(str(a)) == 3:
            a = '0' + a

    if Max_len == 3:
        if len(str(a)) == 1:
            a = '00' + a
        elif len(str(a)) == 2:
            a = '0' + a

    if Max_len == 2:
        if len(str(a)) == 1:
            a = '0' + a

    rank_xyz = xyz.split('-')[1]
    rank = rank_xyz.replace('.xyz', '')

    rename = str(a) + '.xyz'
    change.append(rename)
    
    
    os.rename(xyz, rename)


