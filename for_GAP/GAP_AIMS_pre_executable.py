import os, sys
import time
import subprocess
import re
import shutil
import numpy as np
import aims


AIMS = aims.AIMS()      # instantiate

path_for_ranked = os.path.join(os.getcwd(), 'ranked')
list_of_ranked = AIMS.get_list(path_for_ranked)
os.chdir(path_for_ranked)                                                 # chdir to ~/ranked

for i in list_of_ranked:                                                  # top_structures/001.xyz ....
    RANK_label = i.split('/')[-1]                                         # 001 002 003
    NEW_wd_path = i

    if 'aims.out' not in os.listdir(NEW_wd_path):
        print("2")
        print(i)
        AIMS.Prepare_con_sub_files(NEW_wd_path, RANK_label)
        AIMS.xyz_to_Geometry(NEW_wd_path, i)
        AIMS.Aims_submit(NEW_wd_path)
        Breathing_dir = AIMS.Breathing(NEW_wd_path)
        for j in Breathing_dir:
            path_breathing = os.path.join(NEW_wd_path, j)
            AIMS.Prepare_con_sub_files(path_breathing, 'B'+RANK_label)
            AIMS.Aims_submit(path_breathing)
    else:
        print("2")
        print(i)
        if int(i.split('/')[-1]) < 11:
            if 'B_-1.0' not in os.listdir(i):
                print("3")
                Breathing_dir = AIMS.Breathing(NEW_wd_path)
                for j in Breathing_dir:
                    print("4")
                    path_breathing = os.path.join(NEW_wd_path, j)
                    AIMS.Prepare_con_sub_files(path_breathing, 'B'+RANK_label)
                    AIMS.Aims_submit(path_breathing)
            else:
                print("5")
                Breathing_dir = [x for x in os.listdir(i) if os.path.isdir(os.path.join(i, x))] #  i + '/' + x)]
                
                for j in Breathing_dir:
                    print("6")
                    print(j)
                    path_breathing = os.path.join(NEW_wd_path, j)
                    AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, NO_OF_ATOMS = AIMS.Aims_grep_data(path_breathing) 
                    AIMS.Aims_extended_xyz(path_breathing, AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, NO_OF_ATOMS)
                print("7") 
                AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, NO_OF_ATOMS = AIMS.Aims_grep_data(NEW_wd_path)
                AIMS.Aims_extended_xyz(NEW_wd_path, AIMS_FINAL_ENERGY, AIMS_ENERGY, FORCES, CART, ATOM, NO_OF_ATOMS)
                print()
#NOTE: breathing data is not append to the ext movie file

#AIMS.Aims_GAP_FIT()

