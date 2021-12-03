import sys, math
import numpy as np


kd = lambda i,j : 1. if (i==j) else 0.
class structure_shape:

    def __init__(self, f):
        self.xyz_file = f

        #self.__DEGEN_TOL = 0.025
        #self.__DEGEN_DL  = 7.5
    
    def load_xyz(self):

        with open(self.xyz_file, 'r') as f:
            lines = f.readlines()
            
            self.c1_n = int(lines[0])                       # number of atoms
            del lines[0]
            del lines[0] 
            self.c1_config = np.zeros((self.c1_n+2, 4))

            self.coord = [x.split() for x in lines]
            self.coord = np.asarray(self.coord)
            
            self.ID = self.coord[:, 0]
            self.coord = self.coord[:, 1:].astype(float)
            
            dummy_atom = np.zeros((1,3), dtype=float)
            self.coord = np.append(self.coord, dummy_atom, axis = 0) 
            self.coord = np.append(self.coord, dummy_atom, axis = 0)
           
            print()
            print("### coord ###") 
            #print(self.coord) 
        return None

    def CenterofMass(self, mode = 1):

        self.com = np.zeros((1,3))

        if mode == 1:
            an = self.c1_n + 0
        elif mode == 2:
            an = self.c1_n + 1
        elif mode == 3:
            an = self.c1_n + 2

        self.com = self.coord.sum(axis=0)
        self.com = self.com / float(an)
    

        print()
        print("### COM ###")
        #print(an)
        #print(self.com)

        return None

    def Transformation(self, mode = 1):

        if mode == 1:
            an = self.c1_n + 0
        if mode == 2: 
            an = self.c1_n + 1
        if mode == 3:
            an = self.c1_n + 2

        self.coord_0th = np.subtract(self.coord[:, 0], self.com[0], out=self.coord[:, 0])
        self.coord_1st = np.subtract(self.coord[:, 1], self.com[1], out=self.coord[:, 1])
        self.coord_2nd = np.subtract(self.coord[:, 2], self.com[2], out=self.coord[:, 2])

        self.coord = list(zip(self.coord_0th, self.coord_1st, self.coord_2nd)) 
        self.coord = np.array(self.coord)
        self.coord = np.delete(self.coord, -1, 0)
        self.coord = np.delete(self.coord, -1, 0)

        dummy_atom = np.zeros((1,3), dtype=float)
        self.coord = np.append(self.coord, dummy_atom, axis = 0)
        self.coord = np.append(self.coord, dummy_atom, axis = 0)

        print()
        print("### shift COM to my coordinate system (0, 0, 0) ###")
        #print(an)
        #print(self.coord)
         
        return None


    def InertiaTensor(self, mode = 1):
        
        if mode == 1:
            an = self.c1_n + 0
        if mode == 2:
            an = self.c1_n + 1
        if mode == 3:
            an = self.c1_n + 2

        self.itensor = np.zeros((3,3), dtype=float)
        
        for i in range(an):
            r2 = self.coord[:i+1, 0]**2 + self.coord[:i+1, 1]**2 + self.coord[:i+1, 2]**2
            r2 = r2[-1]
             
            for j in range(3):
                for k in range(3):
                    
                    self.itensor.itemset((j,k), self.itensor.item((j, k)) + (r2 * kd(j,k) - self.coord[i][j] * self.coord[i][k]))
                    # kd is Kronecker delta
        
        eigVal, eigVec = np.linalg.eig(self.itensor)

        print()
        print("### inertia tensor ###")
        print(self.itensor)

        print()
        print("### eige value ###")
        print(eigVal)
        print() 
        print("### eigenvector ###")
        print(eigVec)
        return None

   
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
   
    test.CenterofMass()
     
    test.Transformation()

