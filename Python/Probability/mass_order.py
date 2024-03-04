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
#   dm_l = m3^2 - m1^1    /   dm_s = m2^2 - m1^2 > 0
#   NO : m3 > m2 > m1   /   IO : m2 > m1 > m3
class Mass_order:
    def __init__(self, dm_s, dm_l):
        self.dm_s = dm_s    # eV^2
        self.dm_l = dm_l    # eV^2
    @classmethod
    def input_data( cls, in_dm_21, in_dm_31 ):
        return cls( in_dm_21, in_dm_31 )

    def get_ordering(self):

        mq = np.zeros( (3), dtype=complex )

        if self.dm_l > 0:    # Normal Ordering
            mq[0] = 0
            mq[1] = self.dm_s
            mq[2] = self.dm_l
        
        else:               # Inverted Ordering
            mq[0] = -self.dm_l
            mq[1] = self.dm_s - self.dm_l
            mq[2] = 0
        
        # Define matrix os Mass
        M_mass = np.zeros( (3,3), dtype=complex )
        
        for i in range( len(mq) ):
            M_mass[i][i] = mq[i]
        
        return M_mass



if __name__ == "__main__":
    mass_ordem = Mass_order.input_data( 7*1e-5, 3*1e-3 )
    mass_NO = mass_ordem.get_ordering()
    print(f"\n{mass_NO}\n")
       
