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
import pandas as pd


# Name of the file to be imported
def read_file(name_arq):
    table = pd.read_csv( name_arq, delimiter='\t', header=None ) 
    vector_used = [ table.iloc[row_i][1]     for row_i in range( len(table) ) ] # Row [i] and second column ([1]) -> [i][1]
    
    return vector_used


"""     

    Tau neutrino event files: 
        source image in https://arxiv.org/pdf/1904.07265.pdf - (Fig. 2)    

"""
# Path to the Mathematic directory: Input Files
directory_path = "/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/Mathematica"

# WoutS : Without Smearing (True - plot dashed)                             # Name of the data files (Input): WS (With Smearing) | WoutS (Without Smearing)
# WS : With Smearing       (Reco. - plot continued)                       
name_WoutS_Nu_minus = "Mat_WoutS_In_ModeNu_Tau_minus.txt"                           # Neutrino Mode 
name_WoutS_Nu_plus  = "Mat_WoutS_In_ModeNu_Tau_plus.txt"     
name_WS_Nu_minus    = "Mat_WS_In_ModeNu_Tau_minus.txt"
name_WS_Nu_plus     = "Mat_WS_In_ModeNu_Tau_plus.txt"     

name_WoutS_AntiNu_minus = "Mat_WoutS_In_ModeAntiNu_Tau_minus.txt"                   # AntiNeutrino Mode 
name_WoutS_AntiNu_plus  = "Mat_WoutS_In_ModeAntiNu_Tau_plus.txt"     
name_WS_AntiNu_minus    = "Mat_WS_In_ModeAntiNu_Tau_minus.txt"
name_WS_AntiNu_plus     = "Mat_WS_In_ModeAntiNu_Tau_plus.txt"  
 
name_WoutS_HE_minus = "Mat_WoutS_In_ModeHE_Tau_minus.txt"                           # High Energy Mode
name_WS_HE_minus    = "Mat_WS_In_ModeHE_Tau_minus.txt"             

# Join: directory_path/name_file                                            # Directory (Join): dir_path/name_file:
WoutS_Nu_minus = os.path.join(directory_path, name_WoutS_Nu_minus)                  # Neutrino Mode
WoutS_Nu_plus  = os.path.join(directory_path, name_WoutS_Nu_plus)
WS_Nu_minus    = os.path.join(directory_path, name_WS_Nu_minus)
WS_Nu_plus     = os.path.join(directory_path, name_WS_Nu_plus)
 
WoutS_AntiNu_minus = os.path.join(directory_path, name_WoutS_AntiNu_minus)          # AntiNeutrino Mode
WoutS_AntiNu_plus  = os.path.join(directory_path, name_WoutS_AntiNu_plus)
WS_AntiNu_minus    = os.path.join(directory_path, name_WS_AntiNu_minus)
WS_AntiNu_plus     = os.path.join(directory_path, name_WS_AntiNu_plus)

WoutS_HE_minus = os.path.join(directory_path, name_WoutS_HE_minus)                  # High Energy Mode
WS_HE_minus    = os.path.join(directory_path, name_WS_HE_minus)

# Vectors (Events/bin) : Input (In) data from the table                     # Input:
    # Neutrino Mode:                                                        (Neutrino)
In_minus_Nu_true = read_file(WoutS_Nu_minus)                                     # Tau_minus :  neutrino of true energy      ( WoutS_Nu_minus )
In_plus_Nu_true  = read_file(WoutS_Nu_plus)                                      # Tau_plus  :  neutrino of true energy      ( WoutS_Nu_plus )
In_minus_Nu_reco = read_file(WS_Nu_minus)                                        # Tau_minus :  neutrino of reco. energy     ( WS_Nu_minus )
In_plus_Nu_reco  = read_file(WS_Nu_plus)                                         # Tau_plus  :  neutrino of reco. energy     ( WS_Nu_plus )

    # AntiNeutrino Mode:                                                    (AntiNeutrino)
In_minus_AntiNu_true = read_file(WoutS_AntiNu_minus)                             # Tau_minus :  neutrino of true energy      ( WoutS_AntiNu_minus )
In_plus_AntiNu_true  = read_file(WoutS_AntiNu_plus)                              # Tau_plus  :  neutrino of true energy      ( WoutS_AntiNu_plus )
In_minus_AntiNu_reco = read_file(WS_AntiNu_minus)                                # Tau_minus :  neutrino of reco. energy     ( WS_AntiNu_minus )
In_plus_AntiNu_reco  = read_file(WS_AntiNu_plus)                                 # Tau_plus  :  neutrino of reco. energy     ( WS_AntiNu_plus )

    # High Energy Mode:                                                     (High Energy)
In_minus_HE_true = read_file(WoutS_HE_minus)                                     # Tau_minus :  neutrino of true energy      ( WoutS_HE_minus )
In_minus_HE_reco = read_file(WS_HE_minus)                                        # Tau_minus :  neutrino of reco. energy     ( WS_HE_minus )

