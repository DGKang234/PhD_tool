import os
import re
import time
from colored import fg, bg, attr
import subprocess
from InertiaTensor import *

start = time.time()



if __name__ == '__main__':
   
    def func(elem):
        return int(elem.split('_')[0])

    EXTENSION = 'klmc.xyz'
    path = './xyzFiles'

    task = [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x)) if EXTENSION in x ]
    task = sorted(task,key=func)
    
    for i in task:
        print()
        print()
        print(f"{fg('red')} {bg('blue')} {i} {attr(0)}")

        ii = i 
        i = path + '/' + i 
        main = structure_shape(i)
        
        main.load_xyz()
        
        main.CenterofMass()
        
        main.Transformation()
        
        eigVal, eigVec = main.InertiaTensor() 
         
        with open('eigval_inertiatensor.csv', 'a') as f:
            f.write(ii.split('.')[0])       # IP rank or file name
            f.write(', ' + str(', '.join([str(x) for x in sorted(eigVal)])))    # principle moment of inertia
            f.write('\n') 
        
         
    end = time.time()
    print(f'\nTotal time {end-start}')

