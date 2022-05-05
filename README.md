# Tools for nanoclusters material research

#### Language: python 3.x
#### Software requirement: KLMC, GULP, FHI-aims
#### Dong gi Kang, tonggih.kang.18@ucl.ac.uk

----
# Parent directory (current path)

## bulk_modulus_fit.py
Fitting bulk modulus using calculated data
- Birch_Munaghan
- Murnaghan
- Birch
- Vinet

## hashkey_fileter.py
Using NAUTY code to filter out duplicated (polymorph) structure

## change_atom.py
Chaning cation and anion to another atom type
e.g. for data mining:  LaF3 --> AlF3 

## xyz_to_geo.sh
Convert xyz file to geometry.in file (FHI-aims input)

## dftE_rank_changing.py
Retreive the rank of the DFT optimised IP structures and the rank of the corresponding IP structures.
Save to 'aims_klmc.csv'

## RDFpy_notebook.py
Plotting RDF (radial distribution function) for bulk structures
N.B.  Originally written in Jupyter lab and it's merely copied and pasted to this file

----

# aims_auto

## 0_preprocessing_step.py
Chaning 'top_structures/B{FirstStep}-{IPrank}.xyz' to 'top_structure/{IPrank}.xyz' 

## 1_XYZcollect.py
Preparing for the FHI-aims calculations. Generating 'ranked' (parent working dir) and nested directory (named with {IPrank}).
Then, copy and paste the {IPrank}.xyz to the nested directory

## 2_essentials.py
Copy and paste 'control.in' (parameters for the FHI-aims code), and generating 'geometry.in' using 'xyz_to_aims.sh'.
Copy and paste 'trash.in' (job submission script for a HPC) then, submit the job
N.B. default setting is using free budgets (no gold)

## 3_optimisedXYZ.py
Check all output file (aims.out) in the nested working directories at 'ranked'.
Except unfinished calculation generate .xyz file from 'geometry.in.next_ste' then, copy-and-paste to the 'xyzFiles' at 
parent directory

## 4_cf_out.py
Using 'CF_clusterpy' to quantify expansion/contraction and root-mean-squared of atomic postion of before (IP struc) 
and after (DFT optimised struc)

## gulp_assess.py
Retreive 'aims.xyz' file from 'xyzFiles' to generate gulp input file at 'gulp'/{IPrank} and run calculations

## final_stats.py
Generating 'uniq_str_info.csv' file which contains 'IP energy, 'IP rank, 'delta IP energy', 'DFT rank', 'DFT optimised energy', 
'DFT single point energy', 'delta DFT energy'.

# copy_this_for_new
The directory where '1_XYZcollect.py', '2_essentials.py' copy the FHI-aims input file and job submission script.

---

# 2body_IP_fitting_grid

## IP_mod.py
Using the grid search method to fit (standard fit and relax fit) 2-body potentials using GULP.
User can customise the resolutions.

## IP_collecting_Datacsv.py
Collect the 2-body potential parameters and sum-of-squares from the fitting at 'Data_standard.csv; and 'Data_relax.csv'

## IP_visparam.py
Plot contour map to show 2-body potential paramters as a function of sum-of-square from 'Data_standard.csv' and 'Data_relax.csv'

----

# for_GAP

## gulp_eig_v1.py
[No modulised version (no classes, or functions)]
Run this code at the parent directory of 'top_structures'

1. It will generate 'gulp_eig' directory where IP calculation will be placed

2. Generating n number of directories and run IP calculation using the gulp code
    2.1. keywords are [ opti conp conj prop eigenvectors ]
    2.2. the gulp will generate output file with optimised structure, xyz file

3. call the eigenvectors and format it as arrays (3n degrees of freedom: 3n-6)

4. Sum optimised cartesian coordiate and {lambda} x eigenvector and
    generate ?? number of xyz file

    4.1. generate {movie.xyz} file that contains all xyz file
    (all xyz is concatedated in the file)

## gulp_eig_v2.py
[Modulised version]

## gulp_eig_executable.py
It performs same work as 'gulp_eig_v1.py'

### top_structures_forCopying
Test data set. To test the code copy this directory as 'top_structures'
The test result should be idential to the 'gulp_eig_answer'

----
## Tools
.ipynb files

----
Copyright © 2022 Dong gi Kang. All rights reserved. No warranty.

This code is provided for reference only. You may republish any of this code verbatim with author and URL info intact.
You need written permission from the author to make modifications to the code, include parts into your own work, etc.
This is the repository which contains all kinds of tools that I use for my PhD studies.


