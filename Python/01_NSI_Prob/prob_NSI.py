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
from matrix_NSI import *
from s_matrix_mass import *


# Probability_OS : Oscillation Standard
class Probability_NSI:
    def __init__(self, cp_sign, energy, L, instance_U_PMNS, instance_T_NSI, instance_M_order, density) -> None:
        self.cp_sign = cp_sign
        self.en = energy
        self.L = L
        self.inst_U = instance_U_PMNS
        self.inst_T = instance_T_NSI
        self.inst_M = instance_M_order
        self.dens = density     # número de eletrons por cm^3
    @classmethod
    def input_data( cls, cp_sign, energy, in_L, instance_U_PMNS, instance_T_NSI, instance_M_order, density ):
        return cls( cp_sign, energy, in_L, instance_U_PMNS, instance_T_NSI, instance_M_order, density )
    
    def get_osc_NSI( self ):
        Nu_Flavor = 3

        factor_V = 7.63247*1e-14    # np.sqrt(2).Gf.(1 mol/cm^3)   em   [eV]
        factor_Ne_Mantle = 0.5
        V_final = self.dens * factor_V * factor_Ne_Mantle

        factor_L = 5.0677302143*1e9   #Km_to_ev

        Sf_bm = S_matrix.input_data( self.cp_sign, self.en, factor_L*self.L, V_final, self.inst_U, self.inst_M ).get_S_bm()

        U0 = self.inst_U.get_U()
        cU0 = self.inst_U.get_cU()

        Up = np.dot( self.inst_T.get_Tmut() , U0 )
        cUp = np.conjugate( Up )
        Ud = U0
        cUd = cU0

        M_prod = np.zeros( (3,3), dtype=complex )

        # Sf_bf = U0.Sf_bm.U0^{dagger}
        if self.cp_sign > 0:
            M_prod = np.dot( Sf_bm, np.transpose(cUp) )
            Sf_bm = np.dot( Ud, M_prod )
            Sf_bf = Sf_bm
        else:
            M_prod = np.dot( Sf_bm, np.transpose(Up) )
            Sf_bm = np.dot( cUd, M_prod )
            Sf_bf = Sf_bm
        

        Prob_NSI = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )
        for i in range( Nu_Flavor ):
            for j in range( Nu_Flavor ):
                Prob_NSI[i][j] = Sf_bf[j][i]*np.conjugate( Sf_bf[j][i] )

        return Prob_NSI.real



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    matrix_PMNS = Matrix_Osc.input_data( 0.31, 0.0224, 0.582, -0.79444*np.pi )
    Tmut = Matrix_Tmut.input_data().change_parameter( 1*1e-3, 0.0*np.pi )
    matrix_mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )

    Prob_NSI = Probability_NSI.input_data( +1, 4.5, 3, matrix_PMNS, Tmut, matrix_mass, 2.84 )
    print(f"\n{ Prob_NSI.get_osc_NSI() }\n") 

    
    #energy = np.linspace(0.1, 5,100)
    #plt.plot(energy,Probability_NSI.input_data( +1, energy, 1300, matrix_PMNS, Tmut, matrix_mass, 2.84 ))

