###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				18th Fev 2024	                  #####
###########################################################

import os
import numpy as np
import pandas as pd


# Name of the file to be imported
def read_arq(name_arq):
    table = pd.read_csv( name_arq, delimiter='\t', header=None ) 
    return [ table.iloc[row_i][1]     for row_i in range( len(table) ) ]     # Row [i] and second column ([1]) -> [i][1]


"""     

    Tau neutrino event files: 
        source image in https://arxiv.org/pdf/1904.07265.pdf - (Fig. 2)    

"""
# Path to the Mathematic directory: Input Files
directory_path = "/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/Mathematica"

# WoutS :  Without Smearing  (True  - plot dashed)                           # Name of the data files (Input): WS (With Smearing) | WoutS (Without Smearing)
# WS    :  With Smearing     (Reco. - plot continued)                     
name_WoutS_ModeNu_minus = "Mat_WoutS_In_ModeNu_Tau_minus.txt"                       # Neutrino Mode         -   Mode_Nu
name_WoutS_ModeNu_plus  = "Mat_WoutS_In_ModeNu_Tau_plus.txt"     
name_WS_ModeNu_minus    = "Mat_WS_In_ModeNu_Tau_minus.txt"
name_WS_ModeNu_plus     = "Mat_WS_In_ModeNu_Tau_plus.txt"     

name_WoutS_ModeAnti_minus = "Mat_WoutS_In_ModeAntiNu_Tau_minus.txt"                 # AntiNeutrino Mode     -   Mode_Anti
name_WoutS_ModeAnti_plus  = "Mat_WoutS_In_ModeAntiNu_Tau_plus.txt"     
name_WS_ModeAnti_minus    = "Mat_WS_In_ModeAntiNu_Tau_minus.txt"
name_WS_ModeAnti_plus     = "Mat_WS_In_ModeAntiNu_Tau_plus.txt"  
 
name_WoutS_ModeHE_minus = "Mat_WoutS_In_ModeHE_Tau_minus.txt"                       # High Energy Mode      -   Mode_HE
name_WS_ModeHE_minus    = "Mat_WS_In_ModeHE_Tau_minus.txt"

name_BG_ModeNu   = "Mat_WS_In_ModeNu_BG.txt"                                        # BackGround            -   BG (only)
name_BG_ModeAnti = "Mat_WS_In_ModeAntiNu_BG.txt"
name_BG_ModeHE   = "Mat_WS_In_ModeHE_BG.txt"

name_Cp_ModeNu   = "Mat_WS_In_ModeNu_All.txt"                                       # Comparison (with BG)  -   Cp (All the main)
name_Cp_ModeAnti = "Mat_WS_In_ModeAntiNu_All.txt"
name_Cp_ModeHE   = "Mat_WS_In_ModeHE_All.txt"

# Join  :  Directory_path/name_file                                          # Directory (Join): dir_path/name_file(complete):
WoutS_ModeNu_minus = os.path.join(directory_path, name_WoutS_ModeNu_minus)          # Mode_Nu
WoutS_ModeNu_plus  = os.path.join(directory_path, name_WoutS_ModeNu_plus)
WS_ModeNu_minus    = os.path.join(directory_path, name_WS_ModeNu_minus)
WS_ModeNu_plus     = os.path.join(directory_path, name_WS_ModeNu_plus)
 
WoutS_ModeAnti_minus = os.path.join(directory_path, name_WoutS_ModeAnti_minus)      # Mode_AntiNu
WoutS_ModeAnti_plus  = os.path.join(directory_path, name_WoutS_ModeAnti_plus)
WS_ModeAnti_minus    = os.path.join(directory_path, name_WS_ModeAnti_minus)
WS_ModeAnti_plus     = os.path.join(directory_path, name_WS_ModeAnti_plus)

WoutS_ModeHE_minus = os.path.join(directory_path, name_WoutS_ModeHE_minus)          # Mode_HE
WS_ModeHE_minus    = os.path.join(directory_path, name_WS_ModeHE_minus)

BG_ModeNu   = os.path.join(directory_path, name_BG_ModeNu)                          # BG (only)
BG_ModeAnti = os.path.join(directory_path, name_BG_ModeAnti)
BG_ModeHE   = os.path.join(directory_path, name_BG_ModeHE)

Cp_ModeNu   = os.path.join(directory_path, name_Cp_ModeNu)                          # Cp (All the main)
Cp_ModeAnti = os.path.join(directory_path, name_Cp_ModeAnti)
Cp_ModeHE   = os.path.join(directory_path, name_Cp_ModeHE)


# Below we've separated everything that generates Neutrino (tau_minus) and Antineutrino (tau_plus):    
#   The build is: In(Input)_Mode(MNu/MAn/MHE)_type(true/reco)_particle(Nu/Anti)

    # Neutrino Part:                                                        (All the parties that generate Nu)
In_MNu_true_Nu = read_arq(WoutS_ModeNu_minus)                                       # Tau_minus :  Mode Nu   : true energy      ( WoutS_ModeNu_minus )
In_MNu_reco_Nu = read_arq(WS_ModeNu_minus)                                          # Tau_minus :  Mode Nu   : reco. energy     ( WS_ModeNu_minus )

In_MAn_true_Nu = read_arq(WoutS_ModeAnti_minus)                                     # Tau_minus :  Mode Anti : true energy      ( WoutS_ModeAnti_minus )
In_MAn_reco_Nu = read_arq(WS_ModeAnti_minus)                                        # Tau_minus :  Mode Anti : reco. energy     ( WS_AntiNu_minus )

In_MHE_true_Nu = read_arq(WoutS_ModeHE_minus)                                       # Tau_minus :  Mode HE   : true energy      ( WoutS_ModeHE_minus )
In_MHE_reco_Nu = read_arq(WS_ModeHE_minus)                                          # Tau_minus :  Mode HE   : reco. energy     ( WS_ModeHE_minus )


    # Antineutrino Part:                                                    (All the parties that generate Anti)
In_MNu_true_Anti = read_arq(WoutS_ModeNu_plus)                                      # Tau_plus  :  Mode Nu   : true energy      ( WoutS_ModeNu_plus )
In_MNu_reco_Anti = read_arq(WS_ModeNu_plus)                                         # Tau_plus  :  Mode Anti : reco. energy     ( WS_ModeNu_plus )

In_MAn_true_Anti = read_arq(WoutS_ModeAnti_plus)                                    # Tau_plus  :  Mode Anti : true energy      ( WoutS_ModeAnti_plus )
In_MAn_reco_Anti = read_arq(WS_ModeAnti_plus)                                       # Tau_plus  :  Mode Anti : reco. energy     ( WS_ModeAnti_plus )


    # BG and Comparison Part:                                               (All the Background and Comparison)
In_MNu_BG = read_arq(BG_ModeNu)                                                     # BG_ModeNu   : Background_Nu 
In_MNu_Cp = read_arq(Cp_ModeNu)                                                     # Cp_ModeNu   : Comparison_Nu

In_MAn_BG = read_arq(BG_ModeAnti)                                                   # BG_ModeAnti : Background_Anti
In_MAn_Cp = read_arq(Cp_ModeAnti)                                                   # Cp_ModeAnti : Comparison_Anti

In_MHE_BG = read_arq(BG_ModeHE)                                                     # BG_ModeHE   : Background_HE
In_MHE_Cp = read_arq(Cp_ModeHE)                                                     # Cp_ModeHE   : Comparison_HE


# Extra - Events and matrix built and used internally:
    # Calc_reco: Pre-calculation                                            (sigma = 0.256, fac_mu = 0.436, normalization = On)
Pre_cal_MNu_Nu   = [6.63, 11.66, 16.29, 18.05, 16.15, 12.09, 8.02, 5.1, 3.34, 2.36, 1.78, 1.4, 1.13, 0.92, 0.76, 0.62, 0.51, 0.42, \
                    0.34, 0.28, 0.22, 0.18, 0.15, 0.12, 0.09, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0]
Pre_cal_MNu_Anti = [0.33, 0.55, 0.78, 0.92, 0.92, 0.8, 0.62, 0.45, 0.31, 0.21, 0.14, 0.09, 0.06, 0.04, 0.02, 0.02, 0.01, 0.01, 0.0, \
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

Pre_cal_MAn_Nu   = [1.14, 1.85, 2.58, 3.07, 3.15, 2.88, 2.42, 1.93, 1.51, 1.18, 0.92, 0.73, 0.58, 0.46, 0.37, 0.3, 0.25, 0.2, 0.17, \
                    0.14, 0.11, 0.09, 0.07, 0.06, 0.05, 0.04, 0.03, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
Pre_cal_MAn_Anti = [2.58, 4.58, 6.4, 7.05, 6.22, 4.53, 2.87, 1.7, 1.02, 0.66, 0.46, 0.34, 0.26, 0.2, 0.16, 0.12, 0.1, 0.07, 0.06, \
                    0.04, 0.03, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

Pre_cal_MHE_Nu   = [6.22, 9.9, 13.74, 16.57, 17.56, 16.78, 14.87, 12.56, 10.3, 8.28, 6.57, 5.15, 4.0, 3.08, 2.35, 1.78, 1.34, 1.01, \
                    0.75, 0.55, 0.41, 0.3, 0.22, 0.16, 0.12, 0.09, 0.06, 0.05, 0.03, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0]
    # Matrix mapping pre-calculation: bin_true for bin_reco                 (sigma = 0.256, fac_mu = 0.436, normalization = On)
In_matrix_pre_40x01 = np.loadtxt('/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau/rules_pre_40x01.dat')      # Pre-cal: 40 x 01
In_matrix_pre_40x40 = np.loadtxt('/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau/rules_pre_40x40.dat')      # Pre-cal: 40 x 40
                              



if __name__ == "__main__":
    print(In_MNu_BG)
    print(In_MNu_Cp)
    print(In_matrix_pre_40x01)
    print(In_matrix_pre_40x40)

