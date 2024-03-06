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

# Import our libraries
from graphic_bar_unif import *
from histogram_unif import *
from matrix_map import *
from vector_read import *


"""     

    Tau neutrino event files: 
        source image in https://arxiv.org/pdf/1904.07265.pdf - (Fig. 2)    

"""
# Path to the Mathematic directory: Input Files
directory_path = "/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/Mathematica"

# WoutS : Without Smearing (True - plot dashed)                             # Name of the data files (Input): WS (With Smearing) | WoutS (Without Smearing)
# WS : With Smearing       (Reco. - plot continued)                       
name_WoutS_Nu_minus = "Mat_WoutS_In_ModeNu_Tau_minus.txt"                           # Neutrino Mode 
name_WoutS_Nu_plus = "Mat_WoutS_In_ModeNu_Tau_plus.txt"     
name_WS_Nu_minus = "Mat_WS_In_ModeNu_Tau_minus.txt"
name_WS_Nu_plus = "Mat_WS_In_ModeNu_Tau_plus.txt"     

name_WoutS_AntiNu_minus = "Mat_WoutS_In_ModeAntiNu_Tau_minus.txt"                   # AntiNeutrino Mode 
name_WoutS_AntiNu_plus = "Mat_WoutS_In_ModeAntiNu_Tau_plus.txt"     
name_WS_AntiNu_minus = "Mat_WS_In_ModeAntiNu_Tau_minus.txt"
name_WS_AntiNu_plus = "Mat_WS_In_ModeAntiNu_Tau_plus.txt"  
 
name_WoutS_HE_minus = "Mat_WoutS_In_ModeHE_Tau_minus.txt"                           # High Energy Mode
name_WS_HE_minus = "Mat_WS_In_ModeHE_Tau_minus.txt"             

# Join: directory_path/name_file                                            # Directory (Join): dir_path/name_file:
WoutS_Nu_minus = os.path.join(directory_path, name_WoutS_Nu_minus)                  # Neutrino Mode
WoutS_Nu_plus = os.path.join(directory_path, name_WoutS_Nu_plus)
WS_Nu_minus = os.path.join(directory_path, name_WS_Nu_minus)
WS_Nu_plus = os.path.join(directory_path, name_WS_Nu_plus)
 
WoutS_AntiNu_minus = os.path.join(directory_path, name_WoutS_AntiNu_minus)          # AntiNeutrino Mode
WoutS_AntiNu_plus = os.path.join(directory_path, name_WoutS_AntiNu_plus)
WS_AntiNu_minus = os.path.join(directory_path, name_WS_AntiNu_minus)
WS_AntiNu_plus = os.path.join(directory_path, name_WS_AntiNu_plus)

WoutS_HE_minus = os.path.join(directory_path, name_WoutS_HE_minus)                  # High Energy Mode
WS_HE_minus = os.path.join(directory_path, name_WS_HE_minus)

# Vectors (Events/bin) : Input (In) data from the table                     # Input:
    # Neutrino Mode:                                                        (Neutrino)
In_minus_Nu_true = read_arq(WoutS_Nu_minus)                                     # Tau_minus :  neutrino of true energy      ( WoutS_Nu_minus )
In_plus_Nu_true = read_arq(WoutS_Nu_plus)                                       # Tau_plus  :  neutrino of true energy      ( WoutS_Nu_plus )
In_minus_Nu_reco = read_arq(WS_Nu_minus)                                        # Tau_minus :  neutrino of reco. energy     ( WS_Nu_minus )
In_plus_Nu_reco = read_arq(WS_Nu_plus)                                          # Tau_plus  :  neutrino of reco. energy     ( WS_Nu_plus )

    # AntiNeutrino Mode:                                                    (AntiNeutrino)
In_minus_AntiNu_true = read_arq(WoutS_AntiNu_minus)                             # Tau_minus :  neutrino of true energy      ( WoutS_AntiNu_minus )
In_plus_AntiNu_true = read_arq(WoutS_AntiNu_plus)                               # Tau_plus  :  neutrino of true energy      ( WoutS_AntiNu_plus )
In_minus_AntiNu_reco = read_arq(WS_AntiNu_minus)                                # Tau_minus :  neutrino of reco. energy     ( WS_AntiNu_minus )
In_plus_AntiNu_reco = read_arq(WS_AntiNu_plus)                                  # Tau_plus  :  neutrino of reco. energy     ( WS_AntiNu_plus )

    # High Energy Mode:                                                     (High Energy)
In_minus_HE_true = read_arq(WoutS_HE_minus)                                     # Tau_minus :  neutrino of true energy      ( WoutS_HE_minus )
In_minus_HE_reco = read_arq(WS_HE_minus)                                        # Tau_minus :  neutrino of reco. energy     ( WS_HE_minus )


""" 

    Begin "__main__" : calculate() 

"""
energy_bin = np.arange( 0.25, 20.25, 0.5 )                                                              # Histogram_Bins : build from the middle (From 0.0 to 20.0 in 0.5 intervals)
histogram = Histogram.get_Uniform_SP(0, 40, 0.5)                                                        # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5

energy_true = energy_bin                                                                                # Energy: true e reco. built in the middle
energy_reco = energy_bin

map_matrix = Mapping_matrix.input_data( energy_reco, energy_true )                                      # Calling the mapping matrix
#map_matrix.change_parameter( 0, 0, 0.25, 0.435 )
map_matrix = map_matrix.get_mapping_mean()

# OBJ: Factor 0.5 originates from the integration interval

# Neutrino Mode (Calculate):                                                                            # Neutrino (Calc.): Vector_Reco.
cal_minus_Nu_reco = 0.5*np.dot( map_matrix, In_minus_Nu_true )                                                  # Tau_minus :  Events/bin Neutrino ( Reco. ) 
fator_normal = 1*sum(In_minus_Nu_true)/sum(cal_minus_Nu_reco)                                                   #
cal_minus_Nu_reco = [ round( fator_normal*vet , 2 )     for vet in cal_minus_Nu_reco ]                          # normalized

cal_plus_Nu_reco = 0.5*np.dot( map_matrix, In_plus_Nu_true )                                                    # Tau_plus  :  Events/bin Neutrino ( Reco. ) 
fator_normal = 1*sum(In_plus_Nu_true)/sum(cal_plus_Nu_reco)                                                     #
cal_plus_Nu_reco = [ fator_normal*round( vet , 2 )     for vet in cal_plus_Nu_reco ]                            # normalized


# AntiNeutrino Mode (Calculate):                                                                        # Atineutrino (Calc.): Vector_Reco.
cal_minus_AntiNu_reco = 0.5*np.dot( map_matrix, In_minus_AntiNu_true )                                          # Tau_minus :  Events/bin AntiNeutrino ( Reco. ) 
fator_normal = 1*sum(In_minus_AntiNu_true)/sum(cal_minus_AntiNu_reco)                                           #
cal_minus_AntiNu_reco = [ fator_normal*round( vet , 2 )     for vet in cal_minus_AntiNu_reco ]                  # normalized

cal_plus_AntiNu_reco = 0.5*np.dot( map_matrix, In_plus_AntiNu_true )                                            # Tau_plus  :  Events/bin AntiNeutrino ( Reco. ) 
fator_normal = 1*sum(In_plus_AntiNu_true)/sum(cal_plus_AntiNu_reco)                                             #
cal_plus_AntiNu_reco = [ fator_normal*round( vet , 2 )     for vet in cal_plus_AntiNu_reco ]                    # normalized


# High Energy Mode (Calculate):                                                                         # High Energy (Calc.): Vector_Reco.
cal_minus_HE_reco = 0.5*np.dot( map_matrix, In_minus_HE_true )                                                  # Tau_minus :  Events/bin High Energy ( Reco. ) 
fator_normal = 1*sum(In_minus_HE_true)/sum(cal_minus_HE_reco)                                                   #
cal_minus_HE_reco = [ fator_normal*round( vet , 2 )     for vet in cal_minus_HE_reco ]                          # normalized



if __name__ == "__main__":
    
    show_run = 1

    if show_run == 1:
        
        # Graph Display:

        # Neutrino Mode:                                                                                                                     # Neutrino Mode:
        plt_minus_Nu = Graph_single_bar_UJ( histogram, In_minus_Nu_true, In_minus_Nu_reco, cal_minus_Nu_reco, +1, -1 )                              # tau_minus
        plt_minus_Nu.get_plot_bar()
        
        plt_plus_Nu = Graph_single_bar_UJ.input_data( histogram, In_plus_Nu_true, In_plus_Nu_reco, cal_plus_Nu_reco )                               # tau_plus
        plt_plus_Nu.graph_change( +1, +1 )
        plt_plus_Nu.get_plot_bar()
        
        plt_all_Nu = Graph_all_bar_UJ( histogram, In_minus_Nu_true, In_minus_Nu_reco, cal_minus_Nu_reco, \
                                      In_plus_Nu_true, In_plus_Nu_reco, cal_plus_Nu_reco, +1 )                                                      # All: tau_minus + tau_plus                            
        plt_all_Nu.get_plot_bar()

        
        # AntiNeutrino Mode:                                                                                                                 # AntiNeutrino Mode: 
        plt_minus_AntiNu = Graph_single_bar_UJ( histogram, In_minus_AntiNu_true, In_minus_AntiNu_reco, cal_minus_AntiNu_reco, -1, -1 )              # tau_minus
        plt_minus_AntiNu.get_plot_bar()
        
        plt_plus_AntiNu = Graph_single_bar_UJ( histogram, In_plus_AntiNu_true, In_plus_AntiNu_reco, cal_plus_AntiNu_reco , -1, +1 )                 # tau_plus
        plt_plus_AntiNu.get_plot_bar()
        
        plt_all_AntiNu = Graph_all_bar_UJ( histogram, In_minus_AntiNu_true, In_minus_AntiNu_reco, cal_minus_AntiNu_reco, \
                                          In_plus_AntiNu_true, In_plus_AntiNu_reco, cal_plus_AntiNu_reco, -1 )                                      # All: tau_minus + tau_plus
        plt_all_AntiNu.get_plot_bar()

        
        # High Energy Mode:                                                                                                                  # High Energy Mode: 
        plt_minus_HE = Graph_HE_bar_UJ( histogram, In_minus_HE_true, In_minus_HE_reco, cal_minus_HE_reco )                                          # tau_minus
        plt_minus_HE.get_plot_bar()
    


    elif show_run == 2:
        print( "show_run = 2" )
