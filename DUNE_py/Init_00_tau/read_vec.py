###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				18th Fev 2024	                  #####
###########################################################

"""     
Description about this script:
    This script imports all the data obtained and will always be used to export to other file.py  
    Tau neutrino event files: source image in https://arxiv.org/pdf/1904.07265.pdf - (Fig. 2)    
"""

import os
import numpy  as np
import pandas as pd


# Name of the file to be imported
def read_arq(name_arq):
    table = pd.read_csv( name_arq, delimiter='\t', header=None ) 
    return [ table.iloc[row_i][1]     for row_i in range( len(table) ) ]     # Row [i] and second column ([1]) -> [i][1]


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
In_MNu_reco_Nu = read_arq(WS_ModeNu_minus)                                          # Tau_minus :  Mode Nu   : reco. energy     ( WS_ModeNu_minus    )

In_MAn_true_Nu = read_arq(WoutS_ModeAnti_minus)                                     # Tau_minus :  Mode Anti : true energy      ( WoutS_ModeAnti_minus )
In_MAn_reco_Nu = read_arq(WS_ModeAnti_minus)                                        # Tau_minus :  Mode Anti : reco. energy     ( WS_AntiNu_minus      )

In_MHE_true_Nu = read_arq(WoutS_ModeHE_minus)                                       # Tau_minus :  Mode HE   : true energy      ( WoutS_ModeHE_minus )
In_MHE_reco_Nu = read_arq(WS_ModeHE_minus)                                          # Tau_minus :  Mode HE   : reco. energy     ( WS_ModeHE_minus    )

    # Antineutrino Part:                                                    (All the parties that generate Anti)
In_MNu_true_Anti = read_arq(WoutS_ModeNu_plus)                                      # Tau_plus  :  Mode Nu   : true energy      ( WoutS_ModeNu_plus )
In_MNu_reco_Anti = read_arq(WS_ModeNu_plus)                                         # Tau_plus  :  Mode Anti : reco. energy     ( WS_ModeNu_plus    )

In_MAn_true_Anti = read_arq(WoutS_ModeAnti_plus)                                    # Tau_plus  :  Mode Anti : true energy      ( WoutS_ModeAnti_plus )
In_MAn_reco_Anti = read_arq(WS_ModeAnti_plus)                                       # Tau_plus  :  Mode Anti : reco. energy     ( WS_ModeAnti_plus    )

    # BG and Comparison Part:                                               (All the Background and Comparison)
In_MNu_BG = read_arq(BG_ModeNu)                                                     # BG_ModeNu   : Background_Nu 
In_MNu_Cp = read_arq(Cp_ModeNu)                                                     # Cp_ModeNu   : Comparison_Nu

In_MAn_BG = read_arq(BG_ModeAnti)                                                   # BG_ModeAnti : Background_Anti
In_MAn_Cp = read_arq(Cp_ModeAnti)                                                   # Cp_ModeAnti : Comparison_Anti

In_MHE_BG = read_arq(BG_ModeHE)                                                     # BG_ModeHE   : Background_HE
In_MHE_Cp = read_arq(Cp_ModeHE)                                                     # Cp_ModeHE   : Comparison_HE


# Extra - Events and matrix built and used internally: with get5x5 ( sigma = 0.25453, fac_mu = 0.43522, normalization = On )
    # Normalization factors: The events_reco were corrected using the events_true by the normalizations
    # From 5 to 5
Norm5x5_MNu_Nu   = 1.0475126531525370                                               # For bins_get5x5: MNu_Nu 
Norm5x5_MAn_Nu   = 1.0463621343718934                                               # For bins_get5x5: MAn_Nu
Norm5x5_MHE_Nu   = 1.0461371326602456                                               # For bins_get5x5: MHE_Nu
Norm5x5_MNu_Anti = 1.0463685411283083                                               # For bins_get5x5: MNu_Anti
Norm5x5_MAn_Anti = 1.0477159098395560                                               # For bins_get5x5: MAn_Anti
    # From middle to middle: get by get_middle (in particular)
NormMid_MNu_Nu   = 1.0462942927844996                                               # For bins_middle: MNu_Nu 
NormMid_MAn_Nu   = 1.0469537708691026                                               # For bins_middle: MAn_Nu
NormMid_MHE_Nu   = 1.0469465527994053                                               # For bins_middle: MHE_Nu
NormMid_MNu_Anti = 1.0465659287110360                                               # For bins_middle: MNu_Anti
NormMid_MAn_Anti = 1.0461192819006024                                               # For bins_middle: MAn_Anti

###
################################# Linux #############################                       ( sigma = 0.25453, fac_mu = 0.43522, normalization = On )
###
path_linux = '/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau'
    # Calc_reco: Pre-calculation    and     Matrix mapping pre-calculation: bin_true for bin_reco
In_pre_MNu_Nu   = np.loadtxt( os.path.join(path_linux, 'pre_MNu_reco_Nu.dat'  ) )           # Pre-cal: MNu_Nu
In_pre_MNu_Anti = np.loadtxt( os.path.join(path_linux, 'pre_MNu_reco_Anti.dat') )           # Pre-cal: MNu_Anti
In_pre_MAn_Nu   = np.loadtxt( os.path.join(path_linux, 'pre_MAn_reco_Nu.dat'  ) )           # Pre-cal: MAn_Nu
In_pre_MAn_Anti = np.loadtxt( os.path.join(path_linux, 'pre_MAn_reco_Anti.dat') )           # Pre-cal: MAn_Anti
In_pre_MHE_Nu   = np.loadtxt( os.path.join(path_linux, 'pre_MHE_reco_Nu.dat'  ) )           # Pre-cal: MHE_Nu
    # Matrix mapping pre-calculation: bin_true for bin_reco
In_matrix_pre_40x01 = np.loadtxt( os.path.join(path_linux, 'pre_rules_40x01.dat') )         # Pre-cal: 40 x 01
In_matrix_pre_40x40 = np.loadtxt( os.path.join(path_linux, 'pre_rules_40x40.dat') )         # Pre-cal: 40 x 40

                              

















if __name__ == "__main__":
    #print(In_MNu_BG)
    #print(In_MNu_Cp)
    #print(In_matrix_pre_40x01)
    #print(In_matrix_pre_40x40)
    print(In_MNu_reco_Nu)
    print(In_pre_MNu_Nu)
    hist = np.linspace(0.25,19.75, 40)

    vec = np.zeros(len(In_MNu_true_Nu))

    for i in range(len(In_MNu_true_Nu)):
        for j in range(len(In_MNu_true_Nu)):
            if hist[j] < 3.25:
                vec[i] += 0
            elif hist[j] > 3.25:
                vec[i] += In_matrix_pre_40x40[i][j]*In_MNu_true_Nu[j]*0.5
            else:
                vec[i] += In_matrix_pre_40x01[i]*In_MNu_true_Nu[j]*0.5
    fac=sum(In_MNu_true_Nu)/sum(vec)
    print( [ round(fac*i,4) for i in vec ] )

