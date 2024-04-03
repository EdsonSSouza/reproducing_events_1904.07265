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
    _instance = None

    def __init__(self, eps_mut, phi_mut) -> None:
        if eps_mut is None and phi_mut is None:
            self.eps_mut = 0.0
            self.phi_mut = 0.0
        else:
            self.eps_mut = eps_mut
            self.phi_mut = phi_mut
        # Self of the class will be determined by _instance
        Matrix_Tmut._instance = self
    @classmethod
    def input_data( cls ):
        setup_data = cls( None, None )
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def change_parameter( cls, eps_mut, phi_mut ):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data( ) first. ")
        else:
            cls._instance.eps_mut = eps_mut
            cls._instance.phi_mut = phi_mut
        return cls._instance

    def get_Tmut( self ):
        in_const = 27
        Nu_Flavor = 3

        Tmut = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )

        for i in range(Nu_Flavor):
            Tmut[i][i] = 1.0
        Tmut[1][2] = - in_const * self.eps_mut * np.exp( 1j * self.phi_mut )
        #Tmut[1][0] = - in_const * self.eps_mut * np.exp( 1j * self.phi_mut )

        return Tmut



if __name__ == "__main__":
    Tmut = Matrix_Tmut.input_data().change_parameter( 1e-3, 0.5*np.pi ).get_Tmut()
    print(Tmut)

