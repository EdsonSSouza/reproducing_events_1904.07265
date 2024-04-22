###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				27th Fev 2024	                  #####
###########################################################

import numpy as np

# Import our libraries
from .hamilton_mass import Hamilton_matrix


# We define the S-operator on a mass basis
class S_matrix:
    def __init__(self, sign_cp, energy, distance_L, matter_V, instancia_U_PMNS, instancia_M_order) -> None:
        self.sign_cp = sign_cp                                                                            # sign_cp: +1 for neutrinos and -1 for antineutrinos
        self.en      = energy
        self.dist_L  = distance_L                                                                         # dist_L: Distance Source-Detector
        self.pot_V   = matter_V                                                                           # pot_V (Matter potential) = sqrt(2)*Gf*Ne  (Ne -> electron density in matter)
        self.inst_U  = instancia_U_PMNS
        self.inst_M  = instancia_M_order
    @classmethod
    def input_data( cls, sign_cp, energy, distance_L, matter_V, instancia_U_PMNS, instancia_M_order):
        return cls( sign_cp, energy, distance_L, matter_V, instancia_U_PMNS, instancia_M_order )
    
    def get_S_bm(self):
        Nu_Flavor = 3                                                                                     # Number of flavor neutrinos

        Si_bm = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )

        auto_valor = np.zeros( (Nu_Flavor), dtype=complex )                                               # EigenValue
        Q_mod  = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )                                        # EigenVector
        M_prod = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )                                        # Product matrix

        # factor_V =  GeV_to_eV
        Hf_bm = Hamilton_matrix.input_data( self.sign_cp, self.en, 1e9*self.pot_V, self.inst_U, self.inst_M ).get_base_mass()

        try:
            auto_valor, Q_mod = np.linalg.eigh(Hf_bm)
        except Exception as e:
            auto_valor = None
            Q_mod = None
        
        # Convert L to eV
        self.dist_L*=1.97327e-10                                                                          # ev_to_km: 1.97327 = 1/5.06773 * 10^(1)

        # Calculate S-Matrix in propagation basis
        for i in range( Nu_Flavor ):
            phase = 5.0677302143 * self.dist_L * auto_valor[i]                                            # L em GeV
            Si_bm[i][i] = np.exp( - 1j*phase )                                                            # Si_bm : S of mass at the base of the masses
        
        # Transforming: Si_bm to Sf_bm 
        M_prod = np.dot( Si_bm, np.conjugate(Q_mod).T )                                                   # M_prod = Si_bm . Q^{dagger}
        # S of flavor in the pasta base
        Si_bm = np.dot( Q_mod, M_prod )                                                                   # Sf_bm = Q . M_prod = Q. Si_bm . Q^{dagger}
        Sf_bm = Si_bm
        return Sf_bm




if __name__ == "__main__":
    from mass_order import *
    from matrix_PMNS import *
    
    matrix_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, 1.204225*np.pi )
    matrix_mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )

    Sf_bm = S_matrix.input_data( +1, 0.01, 1300*5.0677302143*1e9, 2.848*0.5*7.63247*1e-14, matrix_PMNS, matrix_mass )
    print(f"\n{Sf_bm.get_S_bm()}\n") 

