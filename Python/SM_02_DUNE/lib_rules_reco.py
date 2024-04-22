###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				6th Mar 2024	                  #####
###########################################################

import numpy as np

# Import our libraries
from lib_matrix_map import *


class Rule_smear:
    def __init__(self, histogram, event_true ) -> None:
        self.hist = histogram
        self.ev_true = event_true
    

    def get_middle(self):
        en_reco = np.linspace(0, 20, 401)
        en_true = np.linspace(0, 20, 401)
        mapping_mid = Gaussian_interp2D.input_data( en_reco, en_true ).get_function2D()

        bin_reco = [ (bin.left + bin.right)/2     for bin in self.hist.bins ]
        bin_true = [ (bin.left + bin.right)/2     for bin in self.hist.bins ]

        ev_smear = np.zeros( len(self.ev_true) )

        for i in range( len(self.ev_true) ):
            for j in range( len(self.ev_true) ):
                
                if bin_true[j] != 3.25:
                    ev_smear[i] += mapping_mid( bin_reco[i] , bin_true[j] ) * self.ev_true[j]
                else:
                    ev_smear[i] += mapping_mid( bin_reco[i] , 3.35 ) * self.ev_true[j]
        
        factor_norm = sum(self.ev_true)/sum(ev_smear)
        events_reco = [ round( factor_norm * ev_i , 4 )      for ev_i in ev_smear ]
    
        return events_reco
    

    def get_5for5(self):
        en_reco = np.linspace(0, 20, 401)
        en_true = np.linspace(0, 20, 401)
        map_gau = Gaussian_interp2D.input_data( en_reco, en_true ).change_parameter(0, 0, 0.255, 0.431, 1).get_function2D()

        bin_width = (self.hist.bins[0].right - self.hist.bins[0].left)
        bin_left  =  [  bin.left                                    for bin in self.hist.bins ]
        bin_midl  =  [  bin.left + bin_width/4                      for bin in self.hist.bins ]
        bin_midd  =  [ (bin.left + bin.right)/2                     for bin in self.hist.bins ]
        bin_midr  =  [ (bin.left + bin.right)/2 + bin_width/4       for bin in self.hist.bins ]
        bin_right =  [  bin.right                                   for bin in self.hist.bins ]

        ev_smear = np.zeros( len(self.ev_true) )

        for i in range( len(self.ev_true) ):
            for j in range( len(self.ev_true) ):
                
                if bin_midd[j] > 3.5:
                    ev_smear[i] +=  0.1*self.ev_true[j]*\
                                    sum(    1/10*(  1*map_gau(bin_left[i],bin_left[j])  + 2*map_gau(bin_left[i],bin_midl[j])  + 4*map_gau(bin_left[i],bin_midd[j])  +\
                                                    2*map_gau(bin_left[i],bin_midr[j])  + 1*map_gau(bin_left[i],bin_right[j])    ) +\
                                                    #
                                            2/10*(  1*map_gau(bin_midl[i],bin_left[j])  + 2*map_gau(bin_midl[i],bin_midl[j])  + 4*map_gau(bin_midl[i],bin_midd[j])  +\
                                                    2*map_gau(bin_midl[i],bin_midr[j])  + 1*map_gau(bin_midl[i],bin_right[j])    ) +\
                                                    #
                                            4/10*(  1*map_gau(bin_midd[i],bin_left[j])  + 2*map_gau(bin_midd[i],bin_midl[j])  + 4*map_gau(bin_midd[i],bin_midd[j])  +\
                                                    2*map_gau(bin_midd[i],bin_midr[j])  + 1*map_gau(bin_midd[i],bin_right[j])    ) +\
                                                    #
                                            2/10*(  1*map_gau(bin_midr[i],bin_left[j])  + 2*map_gau(bin_midr[i],bin_midl[j])  + 4*map_gau(bin_midr[i],bin_midd[j])  +\
                                                    2*map_gau(bin_midr[i],bin_midr[j])  + 1*map_gau(bin_midr[i],bin_right[j])    ) +\
                                                    #
                                            1/10*(  1*map_gau(bin_right[i],bin_left[j]) + 2*map_gau(bin_right[i],bin_midl[j]) + 4*map_gau(bin_right[i],bin_midd[j]) +\
                                                    2*map_gau(bin_right[i],bin_midr[j]) + 1*map_gau(bin_right[i],bin_right[j])  )                                       )
                
                elif bin_midd[j] < 3.0:
                    ev_smear[i] += 0
                
                else:
                    ev_smear[i] +=  0.1*self.ev_true[j]*\
                                    sum(    1/6*( 3*map_gau(bin_left[i] , 3.35) + 2*map_gau(bin_left[i] , 3.425) + 1*map_gau(bin_left[i] , 3.5) ) +\
                                            2/6*( 3*map_gau(bin_midl[i] , 3.35) + 2*map_gau(bin_midl[i] , 3.425) + 1*map_gau(bin_midl[i] , 3.5) ) +\
                                            4/6*( 3*map_gau(bin_midd[i] , 3.35) + 2*map_gau(bin_midd[i] , 3.425) + 1*map_gau(bin_midd[i] , 3.5) ) +\
                                            2/6*( 3*map_gau(bin_midr[i] , 3.35) + 2*map_gau(bin_midr[i] , 3.425) + 1*map_gau(bin_midr[i] , 3.5) ) +\
                                            1/6*( 3*map_gau(bin_right[i], 3.35) + 2*map_gau(bin_right[i], 3.425) + 1*map_gau(bin_right[i], 3.5) )     )
        

        factor_norm = sum(self.ev_true)/sum(ev_smear)
        events_reco = [ round( abs(factor_norm * ev_i) , 4 )      for ev_i in ev_smear ]
    
        return events_reco




if __name__ == "__main__":
    import os
    from lib_vector_read import *
    from lib_histogram_uniform import *

    # Path to the Mathematic directory: Input Files
    directory_path = "/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/Mathematica"

    # WoutS : Without Smearing (True - plot dashed)                             # Name of the data files (Input): WS (With Smearing) | WoutS (Without Smearing)
    # WS : With Smearing       (Reco. - plot continued)                       
    name_WoutS_Nu_minus = "Mat_WoutS_In_ModeNu_Tau_minus.txt"                           # Neutrino Mode 
    name_WoutS_Nu_plus = "Mat_WoutS_In_ModeNu_Tau_plus.txt"
    name_WoutS_AntiNu_minus = "Mat_WoutS_In_ModeAntiNu_Tau_minus.txt"                   # AntiNeutrino Mode 
    name_WoutS_AntiNu_plus = "Mat_WoutS_In_ModeAntiNu_Tau_plus.txt"
    name_WoutS_HE_minus = "Mat_WoutS_In_ModeHE_Tau_minus.txt"                           # High Energy Mode

    # Join: directory_path/name_file                                            # Directory (Join): dir_path/name_file:
    WoutS_Nu_minus = os.path.join(directory_path, name_WoutS_Nu_minus)                  # Neutrino Mode
    WoutS_Nu_plus = os.path.join(directory_path, name_WoutS_Nu_plus)
    WoutS_AntiNu_minus = os.path.join(directory_path, name_WoutS_AntiNu_minus)          # AntiNeutrino Mode
    WoutS_AntiNu_plus = os.path.join(directory_path, name_WoutS_AntiNu_plus)
    WoutS_HE_minus = os.path.join(directory_path, name_WoutS_HE_minus)                  # High Energy Mode
    
    # Vectors (Events/bin) : Input (In) data from the table                     # Input:
        # Neutrino Mode:                                                        (Neutrino)
    In_minus_Nu_true = read_file(WoutS_Nu_minus)                                     # Tau_minus :  neutrino of true energy      ( WoutS_Nu_minus )
    In_plus_Nu_true = read_file(WoutS_Nu_plus)                                       # Tau_plus  :  neutrino of true energy      ( WoutS_Nu_plus )
        # AntiNeutrino Mode:                                                    (AntiNeutrino)
    In_minus_AntiNu_true = read_file(WoutS_AntiNu_minus)                             # Tau_minus :  neutrino of true energy      ( WoutS_AntiNu_minus )
    In_plus_AntiNu_true = read_file(WoutS_AntiNu_plus)                               # Tau_plus  :  neutrino of true energy      ( WoutS_AntiNu_plus )
        # High Energy Mode:                                                     (High Energy)
    In_minus_HE_true = read_file(WoutS_HE_minus)                                     # Tau_minus :  neutrino of true energy      ( WoutS_HE_minus )

    hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )
    
    event_minus_reco = Rule_smear( hist, In_minus_Nu_true ).get_5for5()
    event_plus_reco = Rule_smear( hist, In_plus_Nu_true ).get_5for5()

    print(f"\n{event_minus_reco}\n{event_plus_reco}\n")

