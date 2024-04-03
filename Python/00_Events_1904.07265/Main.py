###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				18th Fev 2024	                  #####
###########################################################

import numpy as np

# Import our libraries
from matrix_map import *
from vector_read import *
from histogram_unif import *
from rules_bins_reco import *
from graphic_bar_unif import *


""" 

    Begin "__main__" : calculate() 

"""
show_vec = 2

if show_vec == 1:
    energy_bin = np.arange( 0.25, 20.25, 0.5 )                                                              # Histogram_Bins : build from the middle (From 0.0 to 20.0 in 0.5 intervals)
    histogram = Histogram.get_Uniform_SP(0, 40, 0.5)                                                        # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5

    energy_true = energy_bin                                                                                # Energy: true e reco. built in the middle
    energy_reco = energy_bin

    map_matrix = Mapping_matrix.input_data( energy_reco, energy_true )                                      # Calling the mapping matrix
    #map_matrix.change_parameter( 0, 0, 0.25, 0.435 )
    #map_matrix.change_parameter( 0.0, 0.0, 0.255, 0.431 )
    map_matrix = map_matrix.get_mapping_mean()

    # OBJ: Factor 0.5 originates from the integration interval
    # Neutrino Mode (Calculate):                                                                            # Neutrino (Calc.): Vector_Reco.
    cal_minus_Nu_reco = 0.5*np.dot( map_matrix, In_minus_Nu_true )                                                  # Tau_minus :  Events/bin Neutrino ( Reco. ) 
    fator_normal = 1*sum(In_minus_Nu_true)/sum(cal_minus_Nu_reco)                                                   #
    cal_minus_Nu_reco = [ round( fator_normal*vet , 2 )     for vet in cal_minus_Nu_reco ]                          # normalized

    cal_plus_Nu_reco = 0.5*np.dot( map_matrix, In_plus_Nu_true )                                                    # Tau_plus  :  Events/bin Neutrino ( Reco. ) 
    fator_normal = 1*sum(In_plus_Nu_true)/sum(cal_plus_Nu_reco)                                                     #
    cal_plus_Nu_reco = [ round( fator_normal*vet , 2 )     for vet in cal_plus_Nu_reco ]                            # normalized

    # AntiNeutrino Mode (Calculate):                                                                        # Atineutrino (Calc.): Vector_Reco.
    cal_minus_AntiNu_reco = 0.5*np.dot( map_matrix, In_minus_AntiNu_true )                                          # Tau_minus :  Events/bin AntiNeutrino ( Reco. ) 
    fator_normal = 1*sum(In_minus_AntiNu_true)/sum(cal_minus_AntiNu_reco)                                           #
    cal_minus_AntiNu_reco = [ round( fator_normal*vet , 2 )     for vet in cal_minus_AntiNu_reco ]                  # normalized

    cal_plus_AntiNu_reco = 0.5*np.dot( map_matrix, In_plus_AntiNu_true )                                            # Tau_plus  :  Events/bin AntiNeutrino ( Reco. ) 
    fator_normal = 1*sum(In_plus_AntiNu_true)/sum(cal_plus_AntiNu_reco)                                             #
    cal_plus_AntiNu_reco = [ round( fator_normal*vet , 2 )     for vet in cal_plus_AntiNu_reco ]                    # normalized

    # High Energy Mode (Calculate):                                                                         # High Energy (Calc.): Vector_Reco.
    cal_minus_HE_reco = 0.5*np.dot( map_matrix, In_minus_HE_true )                                                  # Tau_minus :  Events/bin High Energy ( Reco. ) 
    fator_normal = 1*sum(In_minus_HE_true)/sum(cal_minus_HE_reco)                                                   #
    cal_minus_HE_reco = [ round( fator_normal*vet , 2 )     for vet in cal_minus_HE_reco ]                          # normalized


if show_vec == 2:
    histogram = Histogram.get_Uniform_SP(0, 40, 0.5)                                                        # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5

    # Neutrino Mode (Calculate):                                                                            # Neutrino (Calc.): Vector_Reco.
    cal_minus_Nu_reco = Rule_smear( histogram, In_minus_Nu_true).get_5for5_change(0.255, 0.431, 1)                  # Tau_minus :  Events/bin Neutrino ( Reco. )                                                                                        
    cal_plus_Nu_reco  = Rule_smear( histogram, In_plus_Nu_true).get_5for5_change(0.255, 0.431, 1)                   # Tau_plus  :  Events/bin Neutrino ( Reco. )

    # AntiNeutrino Mode (Calculate):                                                                        # Atineutrino (Calc.): Vector_Reco.
    cal_minus_AntiNu_reco = Rule_smear( histogram, In_minus_AntiNu_true).get_5for5_change(0.255, 0.431, 1)          # Tau_minus :  Events/bin AntiNeutrino ( Reco. )
    cal_plus_AntiNu_reco  = Rule_smear( histogram, In_plus_AntiNu_true).get_5for5_change(0.255, 0.431, 1)           # Tau_plus  :  Events/bin AntiNeutrino ( Reco. ) 

    # High Energy Mode (Calculate):                                                                         # High Energy (Calc.): Vector_Reco.
    cal_minus_HE_reco = Rule_smear( histogram, In_minus_HE_true).get_5for5_change(0.255, 0.431, 1)                  # Tau_minus :  Events/bin High Energy ( Reco. ) 




if __name__ == "__main__":
    show_run = 1

    if show_run == 1:
        # Graph Display:

        # Neutrino Mode:                                                                                                                     # Neutrino Mode:
        plt_minus_Nu = Graph_single_bar_UJ.input_data( histogram, In_minus_Nu_true, In_minus_Nu_reco, cal_minus_Nu_reco )                           # tau_minus
        plt_minus_Nu.get_plot_bar()
        
        plt_plus_Nu = Graph_single_bar_UJ.input_data( histogram, In_plus_Nu_true, In_plus_Nu_reco, cal_plus_Nu_reco )                               # tau_plus
        plt_plus_Nu.input_change( +1, +1 )
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
        print( f"\n{In_minus_Nu_true}\n\n{In_plus_Nu_true}\n\n" )
        print( f"\n{In_minus_AntiNu_true}\n\n{In_plus_AntiNu_true}\n\n" )
        print( f"\n{In_minus_HE_true}\n" )
    

    elif show_run == 3:
        print( f"\n{cal_minus_Nu_reco}\n\n{cal_plus_Nu_reco}\n\n" )
        print( f"\n{cal_minus_AntiNu_reco}\n\n{cal_plus_AntiNu_reco}\n\n" )
        print( f"\n{cal_minus_HE_reco}\n" )

        print( 0.5*sum([In_plus_AntiNu_reco[i] - In_minus_AntiNu_reco[i] for i in range(len(In_plus_AntiNu_reco))]) )
        print(0.5*sum(In_minus_AntiNu_reco))
        print(0.5*sum(In_plus_AntiNu_reco))

