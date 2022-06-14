import os, sys
import time
import subprocess
import re
import shutil
import numpy as np
import aims


AIMS = aims.AIMS()      # instantiate

GAP_pre = os.path.join(os.getcwd(), 'ranked')
KLMCs = AIMS.get_list(GAP_pre)
os.chdir(GAP_pre)

for i in KLMCs:                                                  # top_structures/001.xyz ....
    
    RANK_label = i.split('/')[-1] #.split('.xyz')[0]                               # 001 002 003
    
    NEW_wd_path = i

    if 'aims.out' not in os.listdir(NEW_wd_path):
        print(i)
        print()
        AIMS.Prepare_con_sub_files(NEW_wd_path, RANK_label)
        AIMS.xyz_to_Geometry(NEW_wd_path, i)
        AIMS.Aims_submit(NEW_wd_path)

    else:
        print(i)
        print()
        AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, NO_OF_ATOMS = AIMS.Aims_grep_data(NEW_wd_path)
        AIMS.Aims_extended_xyz(NEW_wd_path, AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, NO_OF_ATOMS)
        print()

AIMS.Aims_GAP_FIT()
        
