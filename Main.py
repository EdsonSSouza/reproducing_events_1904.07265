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
import matplotlib.pyplot as plt

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

# WoutS : Without Smearing (True - plot dashed)   
# WS : With Smearing (Reconstruction - plot continued)
name_WoutS_Nu_minus = "Mat_WoutS_In_ModeNu_Tau_minus.txt"     
name_WS_Nu_minus = "Mat_WS_In_ModeNu_Tau_minus.txt"           

# Joint: directory_path/name_arq
WoutS_Nu_minus = os.path.join(directory_path, name_WoutS_Nu_minus)
WS_Nu_minus = os.path.join(directory_path, name_WS_Nu_minus)

# Vectors (Events/bin) : Input (In) data from the table 
In_minus_Nu_true = read_arq(WoutS_Nu_minus)          # Tau_minus:  neutrino of true energy            ( WoutS_Nu_minus )
In_minus_Nu_reco = read_arq(WS_Nu_minus)             # Tau_minus:  neutrino of reconstruction energy  ( WS_Nu_minus )


""" 

    Begin "__main__" : calculate() 

"""

if __name__ == "__main__":

    # Histogram_Bins : build from the middle (From 0.0 to 20.0 in 0.5 intervals)
    energy_bin = np.arange( 0.25, 20.25, 0.5 )
    histogram = Histogram.def_Uniform_SP(0, 40, 0.5)    

    # Calling the mapping matrix
    energy_true = energy_bin
    energy_reco = energy_bin
    map_matrix = Mapping_matrix.input_data( energy_reco, energy_true ).mapping_by_sum()

    # Vector_reconstruction
    cal_minus_Nu_reco = 0.5*np.dot( map_matrix, In_minus_Nu_true )
    fator_normal = 1 #* sum(In_minus_Nu_reco)/sum(cal_minus_Nu_reco)
    vet_minus_Nu_reco = [ fator_normal*round( vet , 2 )     for vet in cal_minus_Nu_reco ]       # Tau_minus: Events/bin Neutrino ( Reconstruction ) 


    graph = Graph_single_bar_UJ.input_data(histogram, In_minus_Nu_true, In_minus_Nu_reco, vet_minus_Nu_reco)
    graph.type_neutrino = -1
    graph.type_tau = -1
    graph.plot_bar()