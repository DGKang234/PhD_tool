
import os
import sys
import subprocess

def change_fname(path, ext, prog):
    new_list=[]
    files = [x for x in os.listdir(path) if ext in x]
    for i in files:
        files = i.split('-')[1]
        files = files.replace(ext, '')
        if prog == "aims" or "a":
            files = path + '/' + prog + '-' + files + ext
        elif prog == "klmc" or "k":
            files = path + '/' + prog + '-' + files + ext
        pass
        i = path + '/' + i
        os.rename(i, files)
        new_list.append(files)
    new_list.sort()
    #print(new_list)
    return files



path = input("submit the path of file which is above the 'top_structures' dir : ")
path = '/home/uccatka/Scratch/' + path + "/xyzFiles"
#path = path + "/xyzFiles" 

prog = input("where the .xyz file came from? (klmc or aims) : ")
prog = prog.lower()
if prog == "k":
    prog = "klmc"
elif prog == "a":
    prog = "aims"
pass

ext = 'aims.xyz'

from_ = int(input('from which rank do you want to calculate RDF? : '))
to_   = int(input('up to which rank do you want to calculate RDF? : '))

#change_fname(path, '.xyz', prog)

files = [x for x in os.listdir(path) if ext in x]
files.sort()
#print(files)

os.chdir(path)
print(os.getcwd())

for i in range(len(files)):
    if from_ <= i+1 <= to_:
        xyz = files[i]
        xyz = xyz.replace(ext, prog)
        #print(xyz)
        cmd = f"echo '{xyz}' | /home/uccatka/auto/RDF/RDF_exe"
        print(cmd) 
        subprocess.call(cmd, shell=True)
        os.listdir(path) 
        csv =  xyz + '.csv'
        output = 'output.csv'
        os.rename(output, csv)




