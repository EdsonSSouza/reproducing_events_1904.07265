###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				12th Mar 2024	                  #####
###########################################################

import numpy as np


# Matrix NSI_mut
class Matrix_Tmut:
    def __init__(self, eps_mut, phi_mut) -> None:
        self.eps_mut = eps_mut
        self.phi_mut = phi_mut
    @classmethod
    def input_data( cls, eps_mut, phi_mut ):
        return cls( eps_mut, phi_mut )

    def get_Tmut( self ):
        Nu_Flavor = 3
        in_const  = 27
        
        Tmut = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )
        Tmut[np.diag_indices(Nu_Flavor)] = 1.0
        Tmut[1][2] = - in_const * self.eps_mut * np.exp( 1j * self.phi_mut )
        return Tmut




if __name__ == "__main__":
    Tmut = Matrix_Tmut.input_data(3e-2, 0.5*np.pi).get_Tmut()
    print(Tmut)

