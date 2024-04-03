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
from hamilton_mass import *


class S_matrix:
    def __init__(self, cp_sign, energy, L, V, instancia_U_PMNS, instancia_M_order) -> None:
        self.cp_sign = cp_sign
        self.en = energy
        self.L = L
        self.V = V
        self.instancia_U = instancia_U_PMNS
        self.instancia_M = instancia_M_order
    @classmethod
    def input_data( cls, in_cp_sign, in_energy, in_L, in_V, in_instancia_U_PMNS, in_instancia_M_order):
        return cls( in_cp_sign, in_energy, in_L, in_V, in_instancia_U_PMNS, in_instancia_M_order )
    
    def get_S_bm(self):
        # Number of flavor neutrinos
        Nu_Flavor = 3

        Si_bm = np.zeros( (3,3), dtype=complex )

        auto_valor = np.zeros( (3), dtype=complex )
        Q_mod = np.zeros( (3,3), dtype=complex )

        M_prod = np.zeros( (3,3), dtype=complex )

        #factor_V =  # GeV_to_eV

        Hf_bm = Hamilton_matrix.input_data( self.cp_sign, self.en, 1e9*self.V, self.instancia_U, self.instancia_M ).get_base_mass()

        try:
            auto_valor, Q_mod = np.linalg.eigh(Hf_bm)
        except Exception as e:
            auto_valor = None
            Q_mod = None
        
        # Convert L to eV
        self.L*=1.97327e-10   # ev_to_km   # 1.97327... = 1/5.06773... * 10^(1)

        # Calculate S-Matrix in propagation basis
        for i in range( Nu_Flavor ):
            phase = 5.0677302143 * self.L * auto_valor[i]   # L em GeV
            Si_bm[i][i] = np.exp( - 1j*phase )              # Si_bm : S de massa na base das massas
        
        # Transformando: Si_bm to Sf_bm 
        M_prod = np.dot( Si_bm, np.conjugate(Q_mod).T )            # M_prod = Si_bm . Q^{dagger}
        # S de sabor na base das massas
        Si_bm = np.dot( Q_mod, M_prod )                     # Sf_bm = Q . M_prod = Q. Si_bm . Q^{dagger}
        Sf_bm = Si_bm

        #mat_auto = np.zeros( (3,3) , dtype=complex)
        #for i in range(3):
        #    mat_auto[i][i]=auto_valor[i]
        #
        #np.dot( np.dot(Q_mod,mat_auto), np.conjugate(Q_mod).T )-Hf_bm

        return Sf_bm



if __name__ == "__main__":
    matrix_PMNS = Matrix_Osc.input_data( 0.307, 0.021218, 0.55805, 1.5068*np.pi )
    matrix_mass = Mass_order.input_data( 7.53*1e-5, 2.4860*1e-3 )

    Sf_bm = S_matrix.input_data( +1, 2.1, 810*5.0677302143*1e9, 2.84*0.5*7.63247*1e-14, matrix_PMNS, matrix_mass )
    print(f"\n{Sf_bm.get_S_bm()}\n") 

