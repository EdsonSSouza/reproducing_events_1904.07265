###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				27th Fev 2024	                  #####
###########################################################

# Import our libraries
from mass_order import *
from matrix_PMNS import *


# We define Hamilton on a mass basis
class Hamilton_matrix:   
    def __init__( self, sign_cp, energy, matter_V, instancia_U_PMNS, instancia_M_order ) -> None:
        self.sign_cp = sign_cp                                                                            # sign_cp: +1 for neutrinos and -1 for antineutrinos
        self.energy  = energy
        self.pot_V   = matter_V                                                                           # pot_V (Matter potential) = sqrt(2)*Gf*Ne  (Ne -> electron density in matter)
        self.inst_U  = instancia_U_PMNS
        self.inst_M  = instancia_M_order
    @classmethod
    def input_data( cls, sign_cp, energy, matter_V, instancia_U_PMNS, instancia_M_order ):
        return cls( sign_cp, energy, matter_V, instancia_U_PMNS, instancia_M_order )
      
    def get_base_mass(self):                                                                              # Definite of the Hamiltoniana: mass base
        Nu_Flavor = 3                                                                                     # Number of flavor neutrinos
        energy_inv = 1/self.energy

        Hf_bm = np.zeros( (3,3), dtype=complex )

        U0 = self.inst_U.get_U()                                                                          # Unitary matrix PMNS
        cU0 = self.inst_U.get_cU()                                                                        # Conjugate of the matrix PMNS ( delta_cp -> - delta_cp )

        Hf_bm[0][0] = self.sign_cp * self.pot_V                                                           # Hf_bm[0][0] (base mass) = sing * V ( first row and column )

        M_prod = np.zeros( (3,3), dtype=complex )                                                         # M_prod: product matrix
        M_prod = np.dot( Hf_bm, U0 )                                                                      # M_prod = Hf_bm . U0 = sign*V . U0
        Hf_bm = np.dot( cU0.T, M_prod )                                                                   # Hf_bm = U0^{dagger} . M_prod = sign * U0^{dagger} . V . U0

        for i in range( Nu_Flavor ):                                                                      # Including the mass part
            Hf_bm[i][i] += 0.5 * energy_inv * self.inst_M.get_ordering()[i][i]                            # Hf_bm = 1/(2 En) * M + sign * U0^{dagger}.V.U0
        
        if self.sign_cp == -1:                                                                            # For Antineutrino: conjugate (delta_cp -> - delta_cp)
            for i in range( Nu_Flavor ):
                for j in range( Nu_Flavor ):
                    Hf_bm[i][j] = np.conjugate( Hf_bm[i][j] )        
        elif abs(self.sign_cp) != 1:
            raise Exception(" Define sign_cp = +1 for Neutrino and sign_cp = -1 for AntiNeutrino! ")
        return Hf_bm




if __name__ == "__main__":
    matrix_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, 1.204225*np.pi )
    matrix_mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )

    hamilton_matrix = Hamilton_matrix.input_data( +1, 0.01, 2.848*0.5*7.63247*1e-14*1e9, matrix_PMNS, matrix_mass )
    print(f"\n{hamilton_matrix.get_base_mass()}\n")        

