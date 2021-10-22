
import os
import sys
import shutil


def get_files(path, ext):
	files = [ x for x in os.listdir(path) if ext in x ]
	files = [ (path + x) for x in files ]
	return files


target = input("plase type target directory : ")
cation = input("What is the original cation in the .xyz files? : ")
CAT = input("To what cation do you want to change? : ")
anion = input("\n\nWhat is the original anion in the .xyz files? : ")
AN = input("To what anion do you want to change? : ")

path = '/home/uccatka/Scratch/9_2019/ZnO/from_KLMC/GA/' + target + '/top_structures/'
dest = '/home/uccatka/Scratch/9_2019/TiN/from_KLMC/GA/' + target + '/top_structures/'
dest_2 = '/home/uccatka/Scratch/9_2019/TiN/from_KLMC/GA/' + target + '/'

os.mkdir(dest_2)
os.mkdir(dest)
#move = os.chdir(path)

xyz = get_files(path, '.xyz')


for f in range(len(xyz)):
	shutil.copy(xyz[f], dest)
	print (str(f + 1) + ' number of file copied to' + str(dest.replace(dest, '')) + '/n')	# EDIT!

os.chdir(dest)

xyz_mod = get_files(dest, '.xyz')

for f in range(len(xyz_mod)):
	print(xyz_mod[f])
	with open(xyz_mod[f], 'r') as fin:
		edit = fin.read().replace(cation, CAT)
		edit = edit.replace(anion, AN)
		with open(xyz_mod[f], 'w') as fout:
				fout.write(edit)
print('\n ALL DONE  ')
	
	


 


