###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				6th Mar 2024	                  #####
###########################################################

""" 
Description about this script:
    This script creates the rules that are used to transform bins_true into bins_reconstructed. 
    We organized it as follows:
        get_middle  : leads the middle of the bins_true in the middle of the bins_reco
        get_5to5    : leads the average of the 5 points in the bins_true to the average of the 5 points in the bins_reco
        get_5to5_pre: uses the pre-calculated get_5to5 rules to perform the transformation in the same way as get_5to5
"""

import numpy as np

# Import our libraries
from Init_00_tau.read_vec import *
from Init_00_tau.migrate  import Gaussian_interp2D


# Rules for converting bins_true into bins_reco using migrate (mapping)
class Rule_smear_Near:
    _instance = None
    def __init__(self, histogram, event_true:np.ndarray, factor_linear:float, factor_mean:float, normalized:float ) -> None:
        self.hist    = histogram
        self.ev_true = event_true
        if factor_linear is None and factor_mean is None and normalized is None:
            self.fac_linear = 0.25453                                                           # sigma  = 0.25453
            self.fac_mean   = 0.43522                                                           # fac_mu = 0.43522
            self.norm       = 1                                                                 # Normalized gaussian: On
        else:
            self.fac_linear = factor_linear
            self.fac_mean   = factor_mean
            self.norm       = normalized
    @classmethod
    def input_data( cls, histogram, event_true:np.ndarray ):
        setup_data    = cls( histogram, event_true, None, None, None )
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def input_change( cls, factor_linear:float, factor_mean:float, normalized:float ):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(row_energy) first. ")
        else:
            cls._instance.fac_linear = factor_linear
            cls._instance.fac_mean   = factor_mean
            cls._instance.norm       = normalized
        return cls._instance
    
    # The midpoint is the reference for both the true bins and the reconstruction
    def get_middle(self, Norm_type:float) -> np.ndarray:                                                                        # Midpoint
        energy = np.linspace(0, 20, 401)
        mapping_mid = Gaussian_interp2D.input_data(energy).input_change(0, 0, 0.258, 0.436, self.norm).get_function2D()         # Mapping Gaussian_2D

        bin = [ (bin.left + bin.right)/2     for bin in self.hist.bins ]

        ev_smear = np.zeros( len(self.ev_true) )                                                                                # Events_reco
        for i in range( len(self.ev_true) ):                                                                                    # Rules
            for j in range( len(self.ev_true) ):        
                if bin[j] != 3.25:
                    ev_smear[i] += mapping_mid( bin[i] , bin[j] ) * self.ev_true[j] * 0.5                                       # OBS. about 0.5: width of the bins 
                else:
                    ev_smear[i] += mapping_mid( bin[i] , 3.35 )   * self.ev_true[j] * 0.5
        alpha_norm = Norm_type #sum(self.ev_true)/sum(ev_smear)                                                                 # Normalization: true_per_reco
        return [ round( abs(alpha_norm * ev_i) , 10 )    for ev_i in ev_smear ]                                                 # Event_reco: final_normalized                                                 
    
    # 5 points in bin_true are used to build 5 points in bin_reco
    def get_5to5(self, Norm_type:float) -> np.ndarray:                                                                          # 5x5 points
        energy  = np.linspace(0, 20, 401)                                                                                       # Mapping Gaussian_2D
        map_gau = Gaussian_interp2D.input_data(energy).input_change(0, 0, self.fac_linear, self.fac_mean, self.norm).get_function2D()

        bin_width = (self.hist.bins[0].right - self.hist.bins[0].left)
        bin_left  =  [  bin.left                                for bin in self.hist.bins ]                                     # building the 5 points
        bin_midl  =  [  bin.left + bin_width/4                  for bin in self.hist.bins ]
        bin_midd  =  [ (bin.left + bin.right)/2                 for bin in self.hist.bins ]
        bin_midr  =  [ (bin.left + bin.right)/2 + bin_width/4   for bin in self.hist.bins ]
        bin_right =  [  bin.right                               for bin in self.hist.bins ]
        
        ev_smear = np.zeros( len(self.ev_true) )                                                                                # Events_reco
        for i in range( len(self.ev_true) ):                                                                                    # Rules
            for j in range( len(self.ev_true) ):       
                if bin_midd[j] > 3.5:
                    # OBS: 0.1 = 0.2 * 0.5, i.e, (normalition of the sum)*(width of the bins) 
                    ev_smear[i] +=  0.1*self.ev_true[j]*\
                                    sum(    0.2*(   map_gau(bin_left[i],bin_left[j])  + map_gau(bin_left[i],bin_midl[j])  + map_gau(bin_left[i],bin_midd[j])  +\
                                                    map_gau(bin_left[i],bin_midr[j])  + map_gau(bin_left[i],bin_right[j])    ) +\
                                                    #
                                            0.2*(   map_gau(bin_midl[i],bin_left[j])  + map_gau(bin_midl[i],bin_midl[j])  + map_gau(bin_midl[i],bin_midd[j])  +\
                                                    map_gau(bin_midl[i],bin_midr[j])  + map_gau(bin_midl[i],bin_right[j])    ) +\
                                                    #
                                            0.2*(   map_gau(bin_midd[i],bin_left[j])  + map_gau(bin_midd[i],bin_midl[j])  + map_gau(bin_midd[i],bin_midd[j])  +\
                                                    map_gau(bin_midd[i],bin_midr[j])  + map_gau(bin_midd[i],bin_right[j])    ) +\
                                                    #
                                            0.2*(   map_gau(bin_midr[i],bin_left[j])  + map_gau(bin_midr[i],bin_midl[j])  + map_gau(bin_midr[i],bin_midd[j])  +\
                                                    map_gau(bin_midr[i],bin_midr[j])  + map_gau(bin_midr[i],bin_right[j])    ) +\
                                                    #
                                            0.2*(   map_gau(bin_right[i],bin_left[j]) + map_gau(bin_right[i],bin_midl[j]) + map_gau(bin_right[i],bin_midd[j]) +\
                                                    map_gau(bin_right[i],bin_midr[j]) + map_gau(bin_right[i],bin_right[j])  )                                       )[0]    
                elif bin_midd[j] < 3.0:
                    ev_smear[i] += 0
                else:
                    ev_smear[i] +=  0.1*self.ev_true[j]*\
                                    sum(    1/3*(   map_gau(bin_left[i] , 3.35) + map_gau(bin_left[i] , 3.425) + map_gau(bin_left[i] , 3.5)     ) +\
                                            1/3*(   map_gau(bin_midl[i] , 3.35) + map_gau(bin_midl[i] , 3.425) + map_gau(bin_midl[i] , 3.5)     ) +\
                                            1/3*(   map_gau(bin_midd[i] , 3.35) + map_gau(bin_midd[i] , 3.425) + map_gau(bin_midd[i] , 3.5)     ) +\
                                            1/3*(   map_gau(bin_midr[i] , 3.35) + map_gau(bin_midr[i] , 3.425) + map_gau(bin_midr[i] , 3.5)     ) +\
                                            1/3*(   map_gau(bin_right[i], 3.35) + map_gau(bin_right[i], 3.425) + map_gau(bin_right[i], 3.5)     )     )[0]
        alpha_norm = Norm_type #sum(self.ev_true)/sum(ev_smear)                                                                 # Normalization: true_per_reco
        return [ round( abs(alpha_norm * ev_i) , 10 )   for ev_i in ev_smear ]                                                  # Event_reco: final_normalized
    
    # Pre-calculation: 5 points in bin_true are used to build 5 points in bin_reco
    def get_5to5_pre(self, Norm_type:float) -> np.ndarray:                                                                      # Pre-calculation: 5x5 points
        if self.fac_linear != 0.25453 or self.fac_mean != 0.43522 or self.norm != 1:                                            # Valid condition
            raise Exception(" This object is only valid for .input_change(0.25453, 0.43522, 1) ! ") 

        bin_midd  =  [ (bin.left + bin.right)/2                 for bin in self.hist.bins ]
        ev_smear = np.zeros( len(self.ev_true) )                                                                                # Events_reco
        for i in range( len(self.ev_true) ):                                                                                    # Rules
            for j in range( len(self.ev_true) ):       
                if bin_midd[j] > 3.5:
                    ev_smear[i] +=  In_matrix_pre_40x40[i][j] * self.ev_true[j] * 0.5                                           # OBS. about 0.5: width of the bins 
                elif bin_midd[j] < 3.0:
                    ev_smear[i] += 0
                else:
                    ev_smear[i] +=  In_matrix_pre_40x01[i]    * self.ev_true[j] * 0.5
        alpha_norm = Norm_type #sum(self.ev_true)/sum(ev_smear)                                                                 # Normalization: true_per_reco
        return [ round( abs(alpha_norm * ev_i) , 10 )   for ev_i in ev_smear ]                                                  # Event_reco: final_normalized

    


if __name__ == "__main__":
    a=1
        
