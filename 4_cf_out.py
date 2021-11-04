
import os
import sys
import pathlib

def get_directories(path):
    directories = [x for x in os.listdir(path)]
    directories = [(path + x) for x in directories]
    directories.sort()
    return directories

def get_ranking(path, ext):
    ranking = [x for x in os.listdir(path) if ext in x ]
    ranking = [ x for x in ranking]
    ranking.sort()
    return ranking

#print("which structures would you like to compare? : {full path (holding ranked, top_structures)} ")
#root = input()
root = os.getcwd()
path = root + '/ranked/'
dest = ''


files = get_directories(path)

for x in range(len(files)):

    os.chdir(files[x])
    rank = get_ranking(files[x], '.xyz')

    os.system("python /home/uccatka/software/CF-CLUSTERpy/CF_CLUSTERSpy_MAIN.py aims.xyz %s" % rank[0])

    #print("\n%s has compared with aims output " % rank[0])

    cwd = os.getcwd()
    #check = [x for x in os.listdir(cwd) if "CF.out" in x]
    #print(check)
   
    check = pathlib.Path("CF.out")
    if check.exists():

        with open("CF.out", 'r') as f:
            for line in f:
                line = line.rstrip()
                if "RMS CONFIG:" in line:
                    RMS = line.replace("RMS CONFIG:", '')
                if "Scaling Factor :" in line:
                    scaling = line.replace("Scaling Factor :", '')
                    print(RMS, scaling)


    else:
        print("CF.out not existi in %s" % files[x])
        pass

print("RMS CONFIG, Scaling Factor")







