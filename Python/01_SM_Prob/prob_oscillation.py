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
from s_matrix_mass import *
from matrix_PMNS import *


# Define Experiment: L and density
class Pick_Exp:
    def __init__(self, L, density) -> None:
        self.L = L
        self.density = density


# Probability_OS : Oscillation Standard
class Probability_SM:
    def __init__(self, cp_sign, energy, L, instancia_U_PMNS, instancia_M_order, density) -> None:
        self.cp_sign = cp_sign
        self.en = energy
        self.L = L
        self.instancia_U = instancia_U_PMNS
        self.instancia_M = instancia_M_order
        self.dens = density     # número de eletrons por cm^3
    @classmethod
    def input_data( cls, in_cp_sign, in_energy, in_L, in_instancia_U_PMNS, in_instancia_M_order, in_density ):
        return cls( in_cp_sign, in_energy, in_L, in_instancia_U_PMNS, in_instancia_M_order, in_density )
    

    def get_osc_SM(self):

        factor_V = 7.63247*1e-14    # np.sqrt(2).Gf.(1 mol/cm^3)   em   [eV]
        factor_Ne_Mantle = 0.5
        V_final = self.dens * factor_V * factor_Ne_Mantle

        factor_L = 5.0677302143*1e9   #Km_to_ev

        Sf_bm = S_matrix.input_data( self.cp_sign, self.en, factor_L*self.L, V_final, self.instancia_U, self.instancia_M ).get_S_bm_SM()

        U0 = self.instancia_U.get_U()
        cU0 = self.instancia_U.get_cU()

        M_prod = np.zeros( (3,3), dtype=complex )

        # Sf_bf = U0.Sf_bm.U0^{dagger}
        if self.cp_sign > 0:
            M_prod = np.dot( Sf_bm, np.transpose(cU0) )
            Sf_bm = np.dot( U0, M_prod )
            Sf_bf = Sf_bm
        else:
            M_prod = np.dot( Sf_bm, np.transpose(U0) )
            Sf_bm = np.dot( cU0, M_prod )
            Sf_bf = Sf_bm
        

        Prob_SM = np.zeros( (3,3), dtype=complex )
        for i in range( 3 ):
            for j in range( 3 ):
                Prob_SM[i][j] = Sf_bf[j][i]*np.conjugate(Sf_bf[j][i])

        return Prob_SM.real




if __name__ == "__main__":
    matrix_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, -0.79444*np.pi )
    #matrix_mass = Mass_order.input_data( 7.53*1e-5, 2.48*1e-3 )
    matrix_mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )

    Prob_SM = Probability_SM.input_data( +1, 4.0, 1300, matrix_PMNS, matrix_mass, 2.84 )
    print(f"\n{ Prob_SM.get_osc_SM() }\n") 

