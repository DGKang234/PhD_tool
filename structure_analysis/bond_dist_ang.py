import numpy as np
from scipy.spatial import KDTree

# Read in the structure data
with open('001_aims.xyz', 'r') as f:
    lines = f.readlines()

# Extract the atomic coordinates
coords = np.array([list(map(float, line.split()[1:])) for line in lines[2:]])

# Build a KDTree from the atomic coordinates for nearest neighbor search
tree = KDTree(coords)

# Define the cutoff distance for identifying neighboring atoms
cutoff = 1.9

# Calculate the nearest neighbors for each atom within the cutoff distance
neighbor_indices = tree.query_ball_point(coords, r=cutoff)
print(neighbor_indices)
# Calculate the bond distances and bond angles for each atom based on its nearest neighbors
bond_distances = []
bond_angles = []
for i, atom1 in enumerate(coords):
    if isinstance(neighbor_indices[i], list):
        distances_i = []  # Initialize a list of bond distances for atom i
        angles_i = []  # Initialize a list of bond angles for atom i
        for j, atom2_idx in enumerate(neighbor_indices[i]):
            if i != atom2_idx:
                atom2 = coords[atom2_idx]
                vec1 = atom1 - atom2
                distance = np.linalg.norm(vec1)
                distances_i.append(distance)  # Append the bond distance to the list for atom i
                for k, atom3_idx in enumerate(neighbor_indices[i][j+1:]):
                    if k+j+1 != i:
                        atom3 = coords[atom3_idx]
                        vec2 = atom1 - atom3
                        print(i+1, atom2_idx+1, atom3_idx+1)
                        print([i+1, atom2_idx+1], [i+1, atom3_idx+1])
                        print(atom1)
                        print(atom2)
                        print(atom3)
                        print()
                        #cos_angle = np.clip(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)), -1.0, 1.0)
                        cos_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                        angle = np.degrees(np.arccos(cos_angle))
                        angles_i.append(angle)  # Append the bond angle to the list for atom i
        bond_distances.append(distances_i)  # Append the list of bond distances for atom i to the overall list
        bond_angles.append(angles_i)  # Append the list of bond angles for atom i to the overall list

# Print the nearest neighbors, bond distances, and bond angles for each atom
for i, indices in enumerate(neighbor_indices):
    print(f"Atom {i+1} Nearest Neighbors: {[idx+1 for idx in indices if idx != i]}")
    print(f"Atom {i+1} Bond Distances: {bond_distances[i]}")
    print(f"Atom {i+1} Bond Angles: {bond_angles[i]}\n")

