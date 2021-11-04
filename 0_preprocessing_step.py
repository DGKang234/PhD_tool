import os

print('Please type the working directory')
target = input()

path = '/home/uccatka/Scratch/' + target + '/top_structures/'
dest = '/home/uccatka/Scratch/' + target + '/ranked/'
os.chdir(path)

x = [x for x in os.listdir('./') if '.xyz' in x]

change = []
for xyz in x:
    code = xyz.split('-')[0]

    rank_xyz = xyz.split('-')[1]
    rank = rank_xyz.replace('.xyz', '')

    rename = rank + '.xyz'
    #rename = rank + '-' + code + '.xyz'
    #change.append(rename)
    os.rename(xyz, rename)
