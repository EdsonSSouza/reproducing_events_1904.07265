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
from migrate import *
from read_vec import *
from histogram import *
from rules_reco import *
from graphic_bar import *
from graphic_fill import *
from graphic_part import *


""" 

    Begin "__main__" : calculate() 

"""
show_vec = 2

if show_vec == 1:
    energy_bin = np.arange( 0.25, 20.25, 0.5 )                                                             # Histogram_Bins : build from the middle (From 0.0 to 20.0 in 0.5)
    histogram  = Histogram.get_Uniform_SP(0, 40, 0.5)                                                      # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5

    map_matrix = Mapping_matrix.input_data( energy_bin ).get_mapping_mean()                                # Calling the mapping matrix

    # OBJ: Factor 0.5 originates from the integration interval
    # Neutrino Mode (Calculate):                                                                           # Neutrino (Calc.): Reconstruction
    cal_MNu_reco_Nu = 0.5*np.dot( map_matrix, In_MNu_true_Nu )                                                   # Mode_NU : Events/bin Neutrino
    fator_normal    = 1*sum(In_MNu_true_Nu)/sum(cal_MNu_reco_Nu)                                                 #
    cal_MNu_reco_Nu = [ round( fator_normal*vet , 2 )     for vet in cal_MNu_reco_Nu ]                           # normalized

    cal_MNu_reco_Anti = 0.5*np.dot( map_matrix, In_MNu_true_Anti )                                               # Mode_Nu : Events/bin Antineutrino 
    fator_normal      = 1*sum(In_MNu_true_Anti)/sum(cal_MNu_reco_Anti)                                           #
    cal_MNu_reco_Anti = [ round( fator_normal*vet , 2 )     for vet in cal_MNu_reco_Anti ]                       # normalized

    # AntiNeutrino Mode (Calculate):                                                                       # Atineutrino (Calc.): Reconstruction
    cal_MAn_reco_Nu = 0.5*np.dot( map_matrix, In_MAn_true_Nu )                                                   # Mode_An : Events/bin Neutrino 
    fator_normal    = 1*sum(In_MAn_true_Nu)/sum(cal_MAn_reco_Nu)                                                 #
    cal_MAn_reco_Nu = [ round( fator_normal*vet , 2 )     for vet in cal_MAn_reco_Nu ]                           # normalized

    cal_MAn_reco_Anti = 0.5*np.dot( map_matrix, In_MAn_true_Anti )                                               # Mode_An : Events/bin AntiNeutrino 
    fator_normal      = 1*sum(In_MAn_true_Anti)/sum(cal_MAn_reco_Anti)                                           #
    cal_MAn_reco_Anti = [ round( fator_normal*vet , 2 )     for vet in cal_MAn_reco_Anti ]                       # normalized

    # High Energy Mode (Calculate):                                                                        # High Energy (Calc.): Reconstruction
    cal_MHE_reco_Nu = 0.5*np.dot( map_matrix, In_MHE_true_Nu )                                                   # Mode_HE : Events/bin Neutrino
    fator_normal    = 1*sum(In_MHE_true_Nu)/sum(cal_MHE_reco_Nu)                                                 #
    cal_MHE_reco_Nu = [ round( fator_normal*vet , 2 )     for vet in cal_MHE_reco_Nu ]                           # normalized

if show_vec == 2:
    histogram = Histogram.get_Uniform_SP(0, 40, 0.5)                                                       # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5

    # Neutrino Mode (Calculate):                                                                           # Neutrino (Calc.): Reconstruction
    cal_MNu_reco_Nu   = Rule_smear.input_data( histogram, In_MNu_true_Nu  ).get_5to5_pre(Norm5x5_MNu_Nu  )       # Mode_Nu : Events/bin Neutrino                                                                                      
    cal_MNu_reco_Anti = Rule_smear.input_data( histogram, In_MNu_true_Anti).get_5to5_pre(Norm5x5_MNu_Anti)       # Mode_Nu : Events/bin Antineutrino

    # AntiNeutrino Mode (Calculate):                                                                       # Atineutrino (Calc.): Reconstruction
    cal_MAn_reco_Nu   = Rule_smear.input_data( histogram, In_MAn_true_Nu  ).get_5to5_pre(Norm5x5_MAn_Nu  )       # Mode_An : Events/bin Neutrino
    cal_MAn_reco_Anti = Rule_smear.input_data( histogram, In_MAn_true_Anti).get_5to5_pre(Norm5x5_MAn_Anti)       # Mode_An : Events/bin Antineutrino

    # High Energy Mode (Calculate):                                                                        # High Energy (Calc.): Reconstruction
    cal_MHE_reco_Nu = Rule_smear.input_data( histogram, In_MHE_true_Nu ).get_5to5_pre(Norm5x5_MHE_Nu)            # Mode_HE : Events/bin Neutrino 




if __name__ == "__main__":
    show_run = 1

    if show_run == 1:
        # Graph Display:
        # Neutrino Mode:                                                                                                    # Neutrino Mode:
        plt_MNu_Nu   = Graph_each.input_data( +1, -1, histogram, In_MNu_true_Nu, In_MNu_reco_Nu, cal_MNu_reco_Nu )                 # tau_minus
        plt_MNu_Nu.get_plot_bar()  
        plt_MNu_Anti = Graph_each.input_data( +1, +1, histogram, In_MNu_true_Anti, In_MNu_reco_Anti, cal_MNu_reco_Anti )           # tau_plus
        plt_MNu_Anti.get_plot_bar()
        plt_MNu_all  = Graph_all.input_data(+1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti)   # All: tau_minus + tau_plus                            
        plt_MNu_all.input_change( In_MNu_reco_Nu, In_MNu_reco_Anti ).get_plot_bar()
        print()

        # AntiNeutrino Mode:                                                                                                # AntiNeutrino Mode: 
        plt_MAn_Nu   = Graph_each.input_data( -1, -1, histogram, In_MAn_true_Nu, In_MAn_reco_Nu, cal_MAn_reco_Nu )                 # tau_minus
        plt_MAn_Nu.get_plot_bar()
        plt_MAn_Anti = Graph_each.input_data( -1, +1, histogram, In_MAn_true_Anti, In_MAn_reco_Anti, cal_MAn_reco_Anti )           # tau_plus
        plt_MAn_Anti.get_plot_bar()
        plt_MAn_all  = Graph_all.input_data(-1, histogram, In_MAn_true_Nu, cal_MAn_reco_Nu, In_MAn_true_Anti, cal_MAn_reco_Anti)   # All: tau_minus + tau_plus
        plt_MAn_all.input_change(In_MAn_reco_Nu, In_MAn_reco_Anti).get_plot_bar()
        
        # High Energy Mode:                                                                                                 # High Energy Mode: 
        plt_MHE_Nu = Graph_HE.input_data( histogram, In_MHE_true_Nu, cal_MHE_reco_Nu )                                             # tau_minus
        plt_MHE_Nu.input_change(In_MHE_reco_Nu).get_plot_bar()

    elif show_run == 2:
        print( f"\n{In_MNu_true_Nu}\n\n{In_MNu_true_Anti}\n\n" )
        print( f"\n{In_MAn_true_Nu}\n\n{In_MAn_true_Anti}\n\n" )
        print( f"\n{In_MHE_true_Nu}\n" )
    
    elif show_run == 3:
        print( f"\n{cal_MNu_reco_Nu}\n\n{cal_MNu_reco_Anti}\n\n" )
        print( f"\n{cal_MAn_reco_Nu}\n\n{cal_MAn_reco_Anti}\n\n" )
        print( f"\n{cal_MHE_reco_Nu}\n" )

        print( 0.5*sum(In_MAn_reco_Nu)  )
        print( 0.5*sum(In_MAn_reco_Anti))
        print( 0.5*sum([In_MAn_reco_Anti[i] - In_MAn_reco_Nu[i] for i in range(len(In_MAn_reco_Anti))]) )

