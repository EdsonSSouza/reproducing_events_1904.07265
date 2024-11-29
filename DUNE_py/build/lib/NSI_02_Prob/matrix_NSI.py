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
    def __init__(self, delta_mut:float, phi_mut:float) -> None:
        self.delta_mut = delta_mut
        self.phi_mut   = phi_mut
    @classmethod
    def input_data( cls, delta_mut:float, phi_mut:float ):
        return cls( delta_mut, phi_mut )

    def get_Tmut( self ) -> np.ndarray:
        Nu_Flavor = 3
        in_const  = 27
        
        Tmut = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )
        Tmut[np.diag_indices(Nu_Flavor)] = 1.0
        eps_mut    =  in_const * self.delta_mut
        Tmut[1][2] = - eps_mut * np.exp( 1j * self.phi_mut )
        return Tmut




if __name__ == "__main__":
    Tmut = Matrix_Tmut.input_data(3e-2, 0.5*np.pi).get_Tmut()
    print(Tmut)

