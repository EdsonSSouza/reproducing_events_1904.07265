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


# Matrix_PMNS
class Matrix_Osc:
    def __init__(self, sin2_th12, sin2_th13, sin2_th23, delta_cp) -> None:
        self.th12 = np.arcsin( np.sqrt(sin2_th12) )
        self.th13 = np.arcsin( np.sqrt(sin2_th13) )
        self.th23 = np.arcsin( np.sqrt(sin2_th23) )
        self.delta_CP = delta_cp
    @classmethod
    def input_data( cls, in_sin2_th12, in_sin2_th13, in_sin2_th23, in_delta_cp ): 
        return cls(in_sin2_th12, in_sin2_th13, in_sin2_th23, in_delta_cp)
    
    
    # Definition of unitary matrix
    def get_U(self):

        U = np.zeros( (3, 3), dtype=complex )

        U[0][0] = np.cos( self.th12 )*np.cos( self.th13 )
        U[0][1] = np.sin( self.th12 )*np.cos( self.th13 )
        U[0][2] = np.sin( self.th13 )*np.exp( -1j * self.delta_CP )

        U[1][0] = - np.sin( self.th12 )*np.cos( self.th23 ) - np.cos( self.th12 )*np.sin( self.th23 )*np.sin( self.th13 )*np.exp( +1j*self.delta_CP )
        U[1][1] = + np.cos( self.th12 )*np.cos( self.th23 ) - np.sin( self.th12 )*np.sin( self.th23 )*np.sin( self.th13 ) * np.exp( +1j*self.delta_CP )
        U[1][2] = + np.sin( self.th23 )*np.cos( self.th13 )

        U[2][0] = + np.sin( self.th12 )*np.sin( self.th23 ) - np.cos( self.th12 )*np.cos( self.th23 )*np.sin( self.th13 ) * np.exp( +1j*self.delta_CP )
        U[2][1] = - np.cos( self.th12 )*np.sin( self.th23 ) - np.sin( self.th12 )*np.cos( self.th23 )*np.sin( self.th13 ) * np.exp( +1j*self.delta_CP )
        U[2][2] = + np.cos( self.th23 )*np.cos( self.th13 )

        return U
    

    # Definition of the conjugate unitary matrix
    def get_cU(self):

        cU = np.zeros( (3, 3), dtype=complex )

        cU[0][0] = np.cos( self.th12 )*np.cos( self.th13 )
        cU[0][1] = np.sin( self.th12 )*np.cos( self.th13 )
        cU[0][2] = np.sin( self.th13 )*np.exp( +1j * self.delta_CP )

        cU[1][0] = - np.sin( self.th12 )*np.cos( self.th23 ) - np.cos( self.th12 )*np.sin( self.th23 )*np.sin( self.th13 )*np.exp( -1j*self.delta_CP )
        cU[1][1] = + np.cos( self.th12 )*np.cos( self.th23 ) - np.sin( self.th12 )*np.sin( self.th23 )*np.sin( self.th13 ) * np.exp( -1j*self.delta_CP )
        cU[1][2] = + np.sin( self.th23 )*np.cos( self.th13 )

        cU[2][0] = + np.sin( self.th12 )*np.sin( self.th23 ) - np.cos( self.th12 )*np.cos( self.th23 )*np.sin( self.th13 ) * np.exp( -1j*self.delta_CP )
        cU[2][1] = - np.cos( self.th12 )*np.sin( self.th23 ) - np.sin( self.th12 )*np.cos( self.th23 )*np.sin( self.th13 ) * np.exp( -1j*self.delta_CP )
        cU[2][2] = + np.cos( self.th23 )*np.cos( self.th13 )

        return cU



if __name__ == "__main__":
    mat_U = Matrix_Osc.input_data( 0.31, 0.0224, 0.582, -2.5 )
    mat_U = mat_U.get_U()
    mat_cU = Matrix_Osc.input_data( 0.31, 0.0224, 0.582, -2.5 )
    mat_cU = mat_cU.get_cU()
    print(f"\n{mat_U}\n")
    print(f"{mat_cU}\n")
