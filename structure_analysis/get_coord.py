import os, sys, re
from shutil import copy

def get_dir(A='./', B=''):
    global dir_
    dir_ = [x for x in os.listdir(A) if os.path.isdir(x) == True]
    dir_.sort()
    return dir_

def get_files(A='./', B=''):
    global files
    files = [x for x in os.listdir(A) if B in x]
    return files

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(x) for x in re.split(r'(\d+)', text)]

def readline_number_x(file, x, y):
    for index, line in enumerate(iter(file)):
        if x <= index + 1 <= x: return line
    return None

get_dir()

for count, x in enumerate(dir_):
    dir_ = [i for i in os.listdir(x) if os.path.isdir(x) == True] 
    dir_.sort(key=natural_keys)

    path = ['./'+ x +'/'+ i +'/gulp.gout' for i in dir_]
    
    print()
    for g in path:
        print(f'Downloading coordination number data from {g}')
        with open(g) as f:
            lines = f.readlines()

            for num, line_content in enumerate(lines, 1):
                if 'Cutoff for distances  =' in line_content:
                    start = num
                if 'General input information' in line_content:
                    last = num      

            for num, line_content in enumerate(lines, 1):
                if start <= num < last-3:
                    strings = [x for x in line_content.split() if x]
                    strings = list(filter(None, line_content.split()))
                    
                    if len(strings) > 1: 
                            print(strings)
                            if strings[1] == 'F':
                                break

                    with open('downloaded_coord.txt', 'a') as f:
                        from_ = g.split('/')
                        from_ = from_[1] + '/' + from_[2]
                        f.write(from_)
                        #strings = [x for x in strings if not 'Al' or 'F' or 'core' in x]
                        strings.insert(0, ' ')
                        f.write(' '.join(strings))
                        f.write('\n')
                        
           
           
           
            
