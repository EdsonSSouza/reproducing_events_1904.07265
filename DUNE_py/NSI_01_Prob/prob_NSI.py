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
from SM_01_Prob.s_matrix_mass import S_matrix


# Probability_NSI :  Beyond Oscillation Standard
class Probability_NSI:
    def __init__(self, sign_cp, energy, distance_L, instance_U_PMNS, instance_T_NSI, instance_M_order, density) -> None:
        self.sign_cp = sign_cp                                                                            # sign_cp: +1 for neutrinos and -1 for antineutrinos
        self.en      = energy
        self.dist_L  = distance_L                                                                         # dist_L: Distance Source-Detector
        self.inst_U  = instance_U_PMNS
        self.inst_T  = instance_T_NSI
        self.inst_M  = instance_M_order
        self.dens    = density                                                                            # density: number of electrons per cm^3
    @classmethod
    def input_data( cls, sign_cp, energy, distance_L, instance_U_PMNS, instance_T_NSI, instance_M_order, density ):
        return cls( sign_cp, energy, distance_L, instance_U_PMNS, instance_T_NSI, instance_M_order, density )
    
    def get_osc_NSI( self ):
        Nu_Flavor = 3
        factor_V  = 7.63247*1e-14                                                                         # np.sqrt(2).Gf.(1 mol/cm^3)   em   [eV]
        factor_Ne_Mantle = 0.5                                                                            # factor Mantle: earth
        V_final  = self.dens * factor_V * factor_Ne_Mantle
        factor_L = 5.0677302143*1e9                                                                       # Km_to_ev
        
        Sf_bm = S_matrix.input_data( self.sign_cp, self.en, factor_L*self.dist_L, V_final, self.inst_U, self.inst_M ).get_S_bm()

        U0  = self.inst_U.get_U()
        cU0 = self.inst_U.get_cU()
        M_prod = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )

        Up = np.dot( self.inst_T.get_Tmut() , U0 )                                                        # Production PMNS matrix
        cUp = np.conjugate( Up )                                                                          # Conjugate of production PMNS matrix
        Ud, cUd = U0, cU0                                                                                 # Detection PMNS matrix

        if self.sign_cp > 0:                                                                              # For Neutrino
            M_prod = np.dot( Sf_bm, np.transpose(cUp) )                                                   # M_prod = Sf_bm . Up^{dagger}
            Sf_bm = np.dot( Ud, M_prod )                                                                  # Sf_bf = Ud . M_prod = Ud . Sf_bm . Up^{dagger}
            Sf_bf = Sf_bm
        else:                                                                                             # For Antineutrino
            M_prod = np.dot( Sf_bm, np.transpose(Up) )                                                    # M_prod = Sf_bm . Up^{T}
            Sf_bm = np.dot( cUd, M_prod )                                                                 # Sf_bf = Ud^{*} . M_prod = U0^{*} . Sf_bm . Up^{T}
            Sf_bf = Sf_bm
        
        Prob_NSI = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )                                       # Probability_NSI
        for i in range( Nu_Flavor ):
            for j in range( Nu_Flavor ):
                Prob_NSI[i][j] = Sf_bf[j][i]*np.conjugate( Sf_bf[j][i] )
        return Prob_NSI.real



if __name__ == "__main__":
    from matrix_NSI import Matrix_Tmut
    from SM_01_Prob.mass_order import Mass_order
    from SM_01_Prob.matrix_PMNS import Matrix_Osc

    matrix_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, 1.204225*np.pi )
    matrix_mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
    matrix_Tmut = Matrix_Tmut.input_data( 1*1e-3, 1.0*np.pi )

    Prob_NSI = Probability_NSI.input_data( +1, 0.01, 1300, matrix_PMNS, matrix_Tmut, matrix_mass, 2.848 )
    print(f"\n{ Prob_NSI.get_osc_NSI() }\n") 

