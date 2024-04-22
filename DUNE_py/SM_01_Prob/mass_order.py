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


# Mass Ordering : 
#   dm_l = m3^2 - m1^1  /   dm_s = m2^2 - m1^2 > 0          [ eV^2 ]
#   NO : m3 > m2 > m1   /   IO : m2 > m1 > m3               [ eV^2 ]
class Mass_order:
    def __init__(self, dm_s, dm_l):
        self.dm_s = dm_s * 1.0e-18                                           # [GeV^2]
        self.dm_l = dm_l * 1.0e-18                                           # [GeV^2]
    @classmethod
    def input_data( cls, dm2_21, dm2_31 ):
        return cls( dm2_21, dm2_31 )

    def get_ordering(self):
        Nu_Flavor = 3
        mq = np.zeros( (Nu_Flavor), dtype=complex )

        if self.dm_l * 1.0e+18 > 0:                                      # Normal Ordering
            mq[0] = 0                                                        # [ eV^2 ]
            mq[1] = self.dm_s * 1.0e+18                                      # [ eV^2 ]
            mq[2] = self.dm_l * 1.0e+18                                      # [ eV^2 ]
        else:                                                            # Inverted Ordering
            mq[0] = -self.dm_l * 1.0e+18                                     # [ eV^2 ]
            mq[1] = (self.dm_s - self.dm_l) * 1.0e+18                        # [ eV^2 ]
            mq[2] = 0                                                        # [ eV^2 ]
        
        M_mass = np.zeros( (Nu_Flavor, Nu_Flavor), dtype=complex )       # Define the mass matrix       
        for i in range( len(mq) ):
            M_mass[i][i] = mq[i]    
        return M_mass




if __name__ == "__main__":
    mass_ordem = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
    mass_NO = mass_ordem.get_ordering()
    print(f"\n{mass_NO}\n")
       
