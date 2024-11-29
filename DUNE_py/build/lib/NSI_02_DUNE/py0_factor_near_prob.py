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

# Import our libraries
from Init_00_tau.histogram  import Histogram
from SM_01_Prob.mass_order  import Mass_order
from SM_01_Prob.matrix_PMNS import Matrix_Osc
from NSI_02_Prob.prob_NSI   import Probability_NSI

class Factor_Near_Prob:
    
    def __init__(self, sign_cp:int, histogram, instance_U_PMNS, instance_M_order) -> None:
        self.sign_cp = sign_cp                                                                            # sign_cp: +1 for neutrinos and -1 for antineutrinos
        self.his     = histogram
        self.inst_U  = instance_U_PMNS
        self.inst_M  = instance_M_order
    @classmethod
    def input_data( cls, sign_cp:int, histogram, instance_U_PMNS, instance_M_order ):
        return cls( sign_cp, histogram, instance_U_PMNS, instance_M_order )
    
    def get_near( self, delta_mut:float, phi_mut:float ) -> np.ndarray:
        energy = [ (bin.left+bin.right)/2 for bin in self.his.bins ]

        prob_Near = np.zeros(len(energy))
        for i in range(len(energy)):
            prob_Near[i] = Probability_NSI.input_data( self.sign_cp, energy[i], 0.574, self.inst_U, self.inst_M, 0 ).get_osc_NSI(delta_mut, phi_mut)[1][1]
        
        return prob_Near

if __name__ == "__main__":

    hist = Histogram.get_Uniform_WB(0, 20, 0.5)
    PMNS_BF = Matrix_Osc.input_data( 0.307, 0.02195, 0.561, 0.9833*np.pi )
    mass_BF = Mass_order.input_data( 7.49*1e-5, 2.534*1e-3 )
    
    factor = Factor_Near_Prob.input_data(+1, hist, PMNS_BF, mass_BF).get_near(1e-3,1)
    print(factor)
