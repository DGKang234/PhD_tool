
import os
import sys
import numpy as np
from scipy.special import softmax


#cutoff_coord = float(sys.argv[1])

class BOLTZMANN:
    def __init__(self):
        #self.cutoff = cutoff 
        self.ranked_path = 'ranked'

    def GET_COORD_NO(self, rank_w_energy, cutoff):
        output_clusters = [os.path.join('ranked', str(x)) for x in rank_w_energy.keys()]
        output_clusters.sort()
        cluster_mean_coord_no = {}
        for i in output_clusters:
            geometry_file = os.path.join(i, 'geometry.in')
            geometry_next_file = os.path.join(i, 'geometry.in.next_step')
            if os.path.exists(geometry_next_file):
                with open(geometry_next_file, 'r') as f:
                    geo = [x for x in f.readlines() if 'atom' in x]
            elif os.path.exists(geometry_file):
                with open(geometry_file, 'r') as f:
                    geo = [x for x in f.readlines() if 'atom' in x]

            geo = [x.split() for x in geo]
            geo_array = np.array(geo)[:, 1:4].astype(float)
            atom_array = np.array(geo)[:, 4:].ravel()
            matching_indicies_cat = np.where(atom_array == 'Al')[0]
            matching_indicies_an = np.where(atom_array == 'F')[0]

            coord_no = 0
            for j in matching_indicies_cat:
                for k in matching_indicies_an:
                    dist = np.linalg.norm(geo_array[j] - geo_array[k])
                    if dist < cutoff:
                        coord_no += 1
            cluster_mean_coord_no[i] = coord_no/len(matching_indicies_cat)
        return cluster_mean_coord_no



    def GET_DFT_ENERGY(self):
        output_clusters = [os.path.join(self.ranked_path, x, 'aims.out') for x in os.listdir(self.ranked_path) \
        if x.isdigit() if os.path.exists(os.path.join(self.ranked_path, x, 'aims.out')) \
        if os.path.isdir(os.path.join(self.ranked_path, x))]

        output_clusters = sorted(output_clusters, key=lambda x: int(x.split('/')[1]))

        IP_order_rank_w_energy = {}
        for i in output_clusters[:300]:
            with open(i, 'r') as f:
                contents = f.readlines()[-200:]
                energy = float([x for x in contents if '| Total energy of the DFT / Hartree-Fock s.c.f. calculation      :' in x][0].split()[-2])
                IP_order_rank_w_energy[str(i.split('/')[-2])] = energy

        DFT_order_rank_w_energy = sorted(IP_order_rank_w_energy.items(), key=lambda item: item[1])
        DFT_order_rank_w_energy = dict(DFT_order_rank_w_energy)

        check_loc = [x for x in os.listdir('./') if x == 'boltzmann' if os.path.isdir(x)]
        if len(check_loc) == 0:
            os.mkdir('boltzmann')
        else: pass

        with open(f'boltzmann/aims_rank.txt', 'w') as f:
            for k, v in DFT_order_rank_w_energy.items():
                f.write(f"{k}, {v}")
        return DFT_order_rank_w_energy, IP_order_rank_w_energy



    def BOLTZMANN_WEIGHT(self, coord_dict, energy_dict, cutoff):

        # up to DFT rank 300
        COORD_values = list(coord_dict.values())[:300]
        E_values_eV = list(energy_dict.values())[:300] 

        # Convert energies from eV to Joules
        eV_to_J = 1.602176634e-19  # Conversion factor from eV to Joules
        E_values = [E * eV_to_J for E in E_values_eV]
        
        # Set the Boltzmann constant and temperature
        k_B = 1.380649e-23  # Boltzmann constant (in J/K)
        T = 300 
        #T = 273.15 + 110 # Temperature (in Kelvin)
        
        # Subtract the minimum energy from all energy values
        E_min = min(E_values)
        E_shifted = np.array(E_values) - E_min # delta E
        
        # Calculate the Boltzmann weights for each energy value (partition function)
        energies_divided_by_kT = -E_shifted / (k_B * T)
        exp_values = np.exp(energies_divided_by_kT) # Boltzmann function
        partition_function = np.sum(exp_values) # partition function (Z)
        
        #boltzmann_weights of coordination no = COORD_values * exp_values / Z 
        boltzmann_weights = COORD_values * exp_values / partition_function 
        mean_boltzmann_weights = np.sum(COORD_values * exp_values) / partition_function

        #print("Boltzmann weights:", boltzmann_weights)
        list_boltzmann_weights = [str(x) for x in boltzmann_weights.tolist()]

        check_loc = [x for x in os.listdir('./') if x == 'boltzmann' if os.path.isdir(x)]
        if len(check_loc) == 0:
            os.mkdir('boltzmann')
        else: pass

        with open(f'boltzmann/boltzmann_weights_{cutoff}.txt', 'w') as f:
            f.write(f'{cutoff}\n')
            f.write(str(mean_boltzmann_weights.tolist()) + '\n\n')
            f.write('boltzmann_weights')
            for i in list_boltzmann_weights:
                f.write('\n'+i)
        return boltzmann_weights, mean_boltzmann_weights


if __name__ == "__main__":
    BOLTZMANN = BOLTZMANN()
    rank_w_energy = BOLTZMANN.GET_DFT_ENERGY() # rank_w_energy[0] = DFT_order_rank_w_energy, ~[1] = IP_order
    for i in np.arange(1.7, 3.1, 0.1): # cutoff distance in every 0.1 Ang from 1.7 Ang to 3.0 Ang
        i = np.round(i, 1)
        print(i)
        cluster_mean_coord_no = BOLTZMANN.GET_COORD_NO(rank_w_energy[0], i)
        boltzmann_weights, mean_boltzmann_weights = BOLTZMANN.BOLTZMANN_WEIGHT(cluster_mean_coord_no, rank_w_energy[0], i)
        print(f"cutoff distance: {i} Ang")
        print(f"DFT energy order: {rank_w_energy[0]}")
        print(f"Average Al atom coordination number: {cluster_mean_coord_no}")
        print(f"Boltzmann weight: {boltzmann_weights}")
        print(f"Mean Boltzmann weight: {mean_boltzmann_weights}")
