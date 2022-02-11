from colored import fg, bg, attr
import sys, math
import numpy as np

import matplotlib.pyplot as plt



kd = lambda i,j : 1. if (i==j) else 0.

class structure_shape:

    def __init__(self, f):
        self.xyz_file = f

    def load_xyz(self):

        with open(self.xyz_file, encoding="utf8", errors='ignore') as f:
            lines = f.readlines()

            self.c1_n = int(lines[0])                                       # number of atoms
            del lines[0]                                                    # del num of atoms
            del lines[0]                                                    # del energy

            self.coord = [x.split() for x in lines]                         # split into atom species, x, y, z coordinate
            self.coord = np.asarray(self.coord)                             # transform into numpy array

            self.ID = self.coord[:, 0]                                      # atom species
            self.coord = self.coord[:, 1:].astype(float)                    # atom position

            dummy_atom = np.zeros((1,3), dtype=float)                       # empty array
            #self.coord = np.append(self.coord, dummy_atom, axis = 0)
            #self.coord = np.append(self.coord, dummy_atom, axis = 0)

            #print()
            #print("### original atomic position ###")
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

        self.com = self.coord.sum(axis=0)                                   # sum all cartesian coordinates
        self.com = self.com / float(an)                                     # divided into number of atoms (mass of every atom = 1)

        #print()
        #print("### Center of mass of the original atomic position ###")
        #print(self.com)

        return None


    def Transformation(self):
        global coord_x

        self.coord_x = np.subtract(self.coord[:, 0], self.com[0], out=self.coord[:, 0])    # subtract all of x coordinate with x coordinate of com. same for all y, z
        self.coord_y = np.subtract(self.coord[:, 1], self.com[1], out=self.coord[:, 1])
        self.coord_z = np.subtract(self.coord[:, 2], self.com[2], out=self.coord[:, 2])

        self.coord = list(zip(self.coord_x, self.coord_y, self.coord_z))                   # zip the subtracted coordinates into one list
        self.coord = np.array(self.coord)                                                  # transform into array

        #self.coord = np.delete(self.coord, -1, 0)
        #self.coord = np.delete(self.coord, -1, 0)

        dummy_atom = np.zeros((1,3), dtype=float)
        #self.coord = np.append(self.coord, dummy_atom, axis = 0)
        #self.coord = np.append(self.coord, dummy_atom, axis = 0)

        #print()
        #print("### Shift atomic positions to the COM (my coordinate system (0, 0, 0)) ###")
        #print(an)
        #print(self.coord)

        return None
    

############
############



def pairCorrelationFunction_3D(x, y, z, S, rMax, dr):
    """Compute the three-dimensional pair correlation function for a set of
    spherical particles contained in a cube with side length S.  This simple
    function finds reference particles such that a sphere of radius rMax drawn
    around the particle will fit entirely within the cube, eliminating the need
    to compensate for edge effects.  If no such particles exist, an error is
    returned.  Try a smaller rMax...or write some code to handle edge effects! ;)
    Arguments:
        x               an array of x positions of centers of particles
        y               an array of y positions of centers of particles
        z               an array of z positions of centers of particles
        S               length of each side of the cube in space
        rMax            outer diameter of largest spherical shell
        dr              increment for increasing radius of spherical shell
    Returns a tuple: (g, radii, interior_indices)
        g(r)            a numpy array containing the correlation function g(r)
        radii           a numpy array containing the radii of the
                        spherical shells used to compute g(r)
        reference_indices   indices of reference particles
    """
    from numpy import zeros, sqrt, where, pi, mean, arange, histogram

    # Find particles which are close enough to the cube center that a sphere of radius
    # rMax will not cross any face of the cube
    bools1 = x > rMax
    bools2 = x < (S - rMax)
    bools3 = y > rMax
    bools4 = y < (S - rMax)
    bools5 = z > rMax
    bools6 = z < (S - rMax)

    interior_indices, = where(bools1 * bools2 * bools3 * bools4 * bools5 * bools6)
    num_interior_particles = len(interior_indices)

    if num_interior_particles < 1:
        raise  RuntimeError ("No particles found for which a sphere of radius rMax\
                will lie entirely within a cube of side length S.  Decrease rMax\
                or increase the size of the cube.")

    edges = arange(0., rMax + 1.1 * dr, dr)
    num_increments = len(edges) - 1
    g = zeros([num_interior_particles, num_increments])
    radii = zeros(num_increments)
    numberDensity = len(x) / S**3         #####

    # Compute pairwise correlation for each interior particle
    for p in range(num_interior_particles):
        index = interior_indices[p]
        d = sqrt((x[index] - x)**2 + (y[index] - y)**2 + (z[index] - z)**2)
        d[index] = 2 * rMax

        (result, bins) = histogram(d, bins=edges, normed=False)
        g[p,:] = result / numberDensity   #####

    # Average g(r) for all interior particles and compute radii
    g_average = zeros(num_increments)
    for i in range(num_increments):
        radii[i] = (edges[i] + edges[i+1]) / 2.
        rOuter = edges[i + 1]
        rInner = edges[i]
        g_average[i] = mean(g[:, i]) / (4.0 / 3.0 * pi * (rOuter**3 - rInner**3))

    return (g_average, radii, interior_indices)
    # Number of particles in shell/total number of particles/volume of shell/number density
    # shell volume = 4/3*pi(r_outer**3-r_inner**3)


############
############


structure = '/Users/tonggihkang/Desktop/work/Material/AlF3/structures/NEW/bulk/alpha/alpha_opti.xyz'

theExample = structure_shape(structure)
theExample.load_xyz()
theExample.CenterofMass()
theExample.Transformation()
#print(theExample.coord_x)

# array of x, y, z coordinates
coord_x = theExample.coord_x
coord_y = theExample.coord_y
coord_z = theExample.coord_z    
    

domain_size = 25.0                      # size of the box
dr = 0.03                               # step size
particle_radius = 0.01                  # size of atom
rMax = domain_size / 5 * 2              # diameter of the last shell, thus calculate RDF up to this diameter

# Compute pair correlation
g_r, r, reference_indices = pairCorrelationFunction_3D(coord_x, coord_y, coord_z, domain_size, rMax, dr)


# Visulaise
plt.figure()
#plt.rcParams["figure.figsize"] = (10,10)
plt.figure(figsize=(15,10))

plt.plot(r, g_r, color='red')

# labels
plt.title('α-AlF₃ Radial distribution function', fontsize=30, x=0.5, y=1.05)
plt.xlabel('r / Å', fontsize=25)
plt.ylabel('g(r)', fontsize=25)
plt.tick_params(labelsize=20) 

# range of data
plt.xlim( (0, rMax) )
plt.ylim( (0, 1.05 * g_r.max()) )
name = structure.split('.')[0]
plt.savefig(f'{name}.png', dpi=200)
plt.show()



