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
from matrix_PMNS import *
from mass_order import *


# We define Hamilton on a mass basis
#   cp_sign: +1 for neutrinos, -1 for antineutrinos

class Hamilton_matrix:
    # V : Matter potential
    #   V = sqrt(2) * Gf * Ne   ( Ne -> electron density in matter )
    def __init__( self, cp_sign, energ, V, instancia_U_PMNS, instancia_M_order ) -> None:
        self.cp_sign = cp_sign
        self.energ = energ
        self.V = V
        self.instancia_U = instancia_U_PMNS
        self.instancia_M = instancia_M_order
    @classmethod
    def input_data( cls, in_cp_sign, in_energ, in_V, in_instancia_U_PMNS, in_instancia_M_order ):
        return cls( in_cp_sign, in_energ, in_V, in_instancia_U_PMNS, in_instancia_M_order )
    
    
    # Definite of Hamiltoniana : 
    #   H_f(base mass) == |U|^{dagger}.H_f.U  
    #   H_f(base mass) = 1/2 * 1/En * |M|(3x3) + sign * |U|^{dagger}.V.U 
    def base_mass(self):
        # Number of flavor neutrinos
        Nu_Flavor = 3

        Hf_bm = np.zeros( (3,3), dtype=complex )

        U0 = self.instancia_U.get_U()         # Unitary matrix PMNS
        cU0 = self.instancia_U.get_cU()       # Conjugate of the unitary matrix PMNS ( delta_cp -> - delta_cp )

        M_prod = np.zeros( (3,3), dtype=complex )

        # H_f (base mass) = sing * V
        Hf_bm[0][0] = self.cp_sign*self.V

        M_prod = np.dot( Hf_bm, U0 )            # M_prod = Hf_bm . U0 = sign * V . U0
        Hf_bm = np.dot( cU0.T, M_prod )         # Hf_bm = U0^{dagger} . M_prod = sign * U0^{dagger} . V . U0

        # Including the mass part
        for i in range( (Nu_Flavor) ):
            Hf_bm[i][i] += 0.5 * 1/self.energ * self.instancia_M.get_ordering()[i][i]
        
        # Neutrino or Antineutrino
        if abs(self.cp_sign) != 1:
            raise Exception(" This cp_sign value does not exist. Set cp_sign = +1 for Neutrino / cp_sign = -1 for AntiNeutrino. ")
        
        elif self.cp_sign < 0:
            for i in range( len(Nu_Flavor) ):
                for j in range( len(Nu_Flavor) ):
                    Hf_bm[i][j] = np.conjugate( Hf_bm[i][j] )
        
        return Hf_bm



if __name__ == "__main__":
    matrix_PMNS = Matrix_Osc.input_data( 0.31, 0.0224, 0.582, -2.5 )
    matrix_mass = Mass_order.input_data( 7*1e-5, 3*1e-3 )

    hamilton_matrix = Hamilton_matrix.input_data( +1, 2, 2, matrix_PMNS, matrix_mass )
    print(f"\n{hamilton_matrix.base_mass()}\n")        
