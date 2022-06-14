#pip install colored
from colored import fg, bg, attr
import sys, math
import numpy as np

kd = lambda i,j : 1. if (i==j) else 0.

class structure_shape:

    def __init__(self, f):
        self.xyz_file = f

    def load_xyz(self):

        with open(self.xyz_file, 'r') as f:
            lines = f.readlines()
            
            self.c1_n = int(lines[0])                                       # number of atoms
            del lines[0]                                                    # del num of atoms
            del lines[0]                                                    # del energy 
    
            self.coord = [x.split() for x in lines]                         # split into atom species, x, y, z coordinate
            self.coord = np.asarray(self.coord)                             # transform into numpy array
            
            self.ID = self.coord[:, 0]                                      # atom species
            self.coord = self.coord[:, 1:].astype(float)                    # atom position
            
            dummy_atom = np.zeros((1,3), dtype=float)                       # empty array
           
            print()
            print("### original atomic position ###") 
            print(self.coord)
        return None


    def CenterofMass(self, mode = 1):

        self.com = np.zeros((1,3))

        if mode == 1:
            an = self.c1_n + 0
        elif mode == 2:
            an = self.c1_n + 1
        elif mode == 3:
            an = self.c1_n + 2

        self.com = self.coord.sum(axis=0)                                   # sum all cartesian coordinates
        self.com = self.com / float(an)                                     # divided into number of atoms (mass of every atom = 1)
    
        print()         
        print("### Center of mass of the original atomic position ###")
        print(self.com)

        return None


    def Transformation(self): 

        self.coord_x = np.subtract(self.coord[:, 0], self.com[0], out=self.coord[:, 0])    # subtract all of x coordinate with x coordinate of com. same for all y, z
        self.coord_y = np.subtract(self.coord[:, 1], self.com[1], out=self.coord[:, 1])    
        self.coord_z = np.subtract(self.coord[:, 2], self.com[2], out=self.coord[:, 2])

        self.coord = list(zip(self.coord_x, self.coord_y, self.coord_z))                   # zip the subtracted coordinates into one list
        self.coord = np.array(self.coord)                                                  # transform into array
      
        dummy_atom = np.zeros((1,3), dtype=float)

        print()
        print("### Shift atomic positions to the COM (my coordinate system (0, 0, 0)) ###")
        #print(an)
        print(self.coord)
         
        return None


    def InertiaTensor(self):
        
        an = self.c1_n
        
        self.itensor = np.zeros((3,3), dtype=float)
       
        for i in range(an):
            r2 = self.coord[:i+1, 0]**2 + self.coord[:i+1, 1]**2 + self.coord[:i+1, 2]**2
            r2 = r2[-1]
             
            for j in range(3):
                for k in range(3):
                    
                    self.itensor.itemset((j,k), self.itensor.item((j, k)) + (r2 * kd(j,k) - self.coord[i][j] * self.coord[i][k]))
                    # kd is Kronecker delta
                    #print(self.itensor)

        self.eigVal, self.eigVec = np.linalg.eig(self.itensor)

        print()
        print(f"{fg(1)} {bg(15)} ### Inertia tensor ### {attr(0)}")
        print(self.itensor)

        print()
        print(f"{fg(1)} {bg(15)} ### Principal Axes of inertia ###{attr(0)}")
        print(self.eigVal)
        print() 
        print("### eigenvector ###")
        print(self.eigVec)
        return self.eigVal, self.eigVec

   
'''
    def DiagonalMatrix(self, mode = 1):

        self.eigenVal, self.eigenVec = np.linialg.eig(self.itensor)

        self.eigenVal_orig = np.copy(self.eigenVal)

        if mode == 1:
            an = self.c1_n + 0
        if mode == 2:
            an = self.c1_n + 1
        if mode == 3:
            an = self.c1_n + 2

        if mode == 1:
            self.eigenVal, self.eigenVec = self.eig_support_sort(self.eigenVal, self.eigenVec)

        if mode == 2:
            self.eigenVal_a = None
            self.eigenVec_a = None

            self.set_dummy_atom(mode)
            self.CenterofMass(mode)

            self.InertiaTensor(mode)

            self.eigenVal_a, self.eigenVec_a = np.linalg.eig(self.itensor)
            
            self.eigenVal_a, self_eigenVec_a = self.eig_support_sort(self.eigenVal_a, self.eigenVec_a)
        
        if mode = 3:
            self.eigenVal_a = None
            self.eigenVec_a = None

            self.set_dummy_atom(mode)
            self.CenterofMass(mode)
            self.Transformation(mode)
            self.InertiaTensor(mode)

            self.eigenVal_a, self.eigenVec_a = np.linalg.eig(self.itensor)

            self.eigenVal_a, self.eigenVEc_a = self.eig_support(self.eigenVal_a, self.eigenVec_a)
'''




if __name__ == '__main__':
    
    test = structure_shape(sys.argv[1])
    test.load_xyz()
    
    test.CenterofMass()

    test.Transformation()

    test.InertiaTensor()
   
