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
Pre_cal_MNu_Nu   = [6.6293, 11.6628, 16.2877, 18.0543, 16.1527, 12.0874, 8.018, 5.0952, 3.345, 2.3603, 1.7819, 1.4049, 1.133, 0.9234, \
                    0.756, 0.6197, 0.5079, 0.4157, 0.3396, 0.2767, 0.2247, 0.1819, 0.1466, 0.1178, 0.0941, 0.0749, 0.0593, 0.0468, \
                    0.0367, 0.0286, 0.0222, 0.0171, 0.0131, 0.01, 0.0076, 0.0057, 0.0043, 0.0032, 0.0024, 0.0017]
Pre_cal_MNu_Anti = [0.3283, 0.5517, 0.7768, 0.9156, 0.9154, 0.7961, 0.622, 0.4517, 0.3135, 0.212, 0.1412, 0.093, 0.0606, 0.039, 0.0248, \
                    0.0155, 0.0095, 0.0057, 0.0033, 0.0019, 0.0011, 0.0006, 0.0003, 0.0002, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, \
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

Pre_cal_MAn_Nu   = [1.1363, 1.8503, 2.5799, 3.0665, 3.1507, 2.8765, 2.4167, 1.9335, 1.5134, 1.179, 0.9224, 0.7274, 0.5786, 0.4639, 0.3744, \
                    0.3038, 0.2475, 0.2022, 0.1654, 0.1353, 0.1107, 0.0904, 0.0737, 0.0599, 0.0485, 0.0391, 0.0315, 0.0252, 0.0201, 0.0159, \
                    0.0126, 0.0099, 0.0077, 0.006, 0.0046, 0.0035, 0.0027, 0.002, 0.0015, 0.0011]
Pre_cal_MAn_Anti = [2.5777, 4.5785, 6.4018, 7.0537, 6.2186, 4.5275, 2.867, 1.6987, 1.0208, 0.6581, 0.4594, 0.3398, 0.2595, 0.2012, 0.157, \
                    0.1226, 0.0957, 0.0744, 0.0577, 0.0445, 0.0342, 0.0261, 0.0198, 0.0149, 0.0111, 0.0083, 0.0061, 0.0044, 0.0032, 0.0023, \
                    0.0017, 0.0012, 0.0008, 0.0006, 0.0004, 0.0003, 0.0002, 0.0001, 0.0001, 0.0001]

Pre_cal_MHE_Nu   = [6.2183, 9.8979, 13.7441, 16.5707, 17.5637, 16.776, 14.872, 12.5627, 10.3, 8.284, 6.5711, 5.1546, 4.0041, 3.083, 2.3545, \
                    1.7847, 1.3436, 1.0054, 0.7483, 0.5544, 0.4091, 0.301, 0.221, 0.162, 0.1186, 0.0869, 0.0637, 0.0467, 0.0343, 0.0253, \
                    0.0186, 0.0138, 0.0102, 0.0076, 0.0056, 0.0042, 0.0031, 0.0023, 0.0017, 0.0012]

    # Matrix mapping pre-calculation: bin_true for bin_reco                 (sigma = 0.256, fac_mu = 0.436, normalization = On)
In_matrix_pre_40x01 = np.loadtxt('/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau/rules_pre_40x01.dat')      # Pre-cal: 40 x 01
In_matrix_pre_40x40 = np.loadtxt('/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau/rules_pre_40x40.dat')      # Pre-cal: 40 x 40
                              



if __name__ == "__main__":
    #print(In_MNu_BG)
    #print(In_MNu_Cp)
    #print(In_matrix_pre_40x01)
    #print(In_matrix_pre_40x40)
    print(In_MNu_reco_Nu)
    print(Pre_cal_MNu_Nu)
    hist = np.linspace(0.25,19.75, 40)

    vec = np.zeros(len(In_MNu_true_Nu))

    for i in range(len(In_MNu_true_Nu)):
        for j in range(len(In_MNu_true_Nu)):
            if hist[j] < 3.25:
                vec[i] += 0
            elif hist[j] > 3.25:
                vec[i] += In_matrix_pre_40x40[i][j]*In_MNu_true_Nu[j]
            else:
                vec[i] += In_matrix_pre_40x01[i]*In_MNu_true_Nu[j]
    fac=sum(In_MNu_true_Nu)/sum(vec)
    print( [ round(fac*i,4) for i in vec ] )

