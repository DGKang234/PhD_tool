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
        radii           a numpy array containing the radii of the spherical shells used to compute g(r)
        reference_indices   indices of reference particles
    """

    # Boundary condition (we want to have particle which located in between inner and outer sphere)
    # e.g. https://en.wikipedia.org/wiki/Radial_distribution_function#/media/File:Rdf_schematic.svg
    # rMax will not cross any face of the cube
    bools1 = x > rMax
    bools2 = x < (S - rMax)
    bools3 = y > rMax
    bools4 = y < (S - rMax)
    bools5 = z > rMax
    bools6 = z < (S - rMax)

    # store the atom number which satisfy the condition
    interior_indices, = np.where(bools1 * bools2 * bools3 * bools4 * bools5 * bools6)
    num_interior_particles = len(interior_indices)

    # Check error
    if num_interior_particles < 1:
        raise  RuntimeError ("No particles found for which a sphere of radius rMax\
                will lie entirely within a cube of side length S.  Decrease rMax\
                or increase the size of the cube.")
    
    # array (list) of sphere (boundary)
    edges = np.arange(0., rMax + 1.1 * dr, dr)

    num_increments = len(edges) - 1

    # generate len(num_interior_particles) by len(num_increments) 0 array
    g = np.zeros([num_interior_particles, num_increments]) 
    radii = np.zeros(num_increments)
    
    # density = total number of particle / cubic volume
    numberDensity = len(x) / S**3

    # Compute pairwise correlation for each interior particle
    for p in range(num_interior_particles):
        index = interior_indices[p]
        
        print(f"{index}th atom : {x[index]}, {y[index]}, {z[index]}")
        d = np.sqrt((x[index] - x)**2 + (y[index] - y)**2 + (z[index] - z)**2)     # euclidean distance
                        
        d[index] = 2 * rMax                                                        # replace the 0 to 2*rMax        
        
        (result, bins) = np.histogram(d, bins=edges, normed=False)
        
        g[p,:] = result / numberDensity  # replace                                 # insert the row

 
    # Average g(r) for all interior particles and compute radii
    g_average = np.zeros(num_increments)
    for i in range(num_increments):
        radii[i] = (edges[i] + edges[i+1]) / 2.                                  # average of inner and outer radii
        rOuter = edges[i + 1]
        rInner = edges[i]
        
        # No(particles) in shell (np.mean(g[:, i])) / tot no(atoms) / vol(shell) / no density
        # shell volume = 4/3*np.pi(r_outer**3-r_inner**3)
        g_average[i] = np.mean(g[:, i]) / ( 4./3. * np.pi * (rOuter**3 - rInner**3))
        
    return (g_average, radii, interior_indices)

    
# Particle setup
domain_size = 25.0

# Calculation setup
dr = 0.1

### Random arrangement of particles ###
particle_radius = 0.1
rMax = domain_size / 5

x = coord_x
y = coord_y
z = coord_z

# Compute pair correlation
g_r, r, reference_indices = pairCorrelationFunction_3D(x, y, z, domain_size, rMax, dr)


# Visulaise
plt.figure()
#plt.rcParams["figure.figsize"] = (10,10)
plt.figure(figsize=(10,10))
plt.plot(r, g_r, color='black')
plt.title('α-AlF3 - Pair correlation function', fontsize=30)
plt.xlabel('r', fontsize=25)
plt.ylabel('g(r)', fontsize=25)
plt.tick_params(labelsize=20) 


plt.xlim( (0, rMax) )
plt.ylim( (0, 1.05 * g_r.max()) )
plt.savefig('alpha.png', dpi=500)
plt.show()
