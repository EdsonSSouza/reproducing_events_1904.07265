###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				18th Mar 2024	                  #####
###########################################################

import numpy as np

# Import our libraries
#from histogram import *
#from rules_reco import *
from histogram import *
from rules_reco import *


def error_relativo(Input_vec_true, Input_vec_reco):
    numb = int(len(Input_vec_true))
    error_comp = 1e+10
    sigma_mean = 0
    sigma_linear = 0

    hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )

    vec_BFit = Input_vec_reco
    vec_err = np.zeros( numb )
    
    for sig_linear in np.linspace( 0.23, 0.33, 5 ):#101
        for sig_mean in np.linspace( 0.4, 0.5, 5 ):

            vec_reco = Rule_smear.input_data( hist, Input_vec_true ).input_change( sig_linear, sig_mean, 1 ).get_5to5( )

            for i in range( numb ):
                if vec_BFit[i] > 0.01:
                    vec_err[i] = abs( vec_BFit[i] - vec_reco[i] )/vec_BFit[i]
            
            error_rel = sum( vec_err )
            vec_err = np.zeros( numb )

            if error_rel < error_comp:
                error_comp = error_rel
                sigma_mean = sig_mean
                sigma_linear = sig_linear
        
        print( sig_linear/0.33*100 )
    return print(sigma_linear, sigma_mean, error_comp)


def error_different(Input_vec_true, Input_vec_reco):
    numb = int(len(Input_vec_true))
    error_rel = 0
    error_comp = 1e+10
    sigma_mean = 0
    sigma_linear = 0

    hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )

    vec_BFit = Input_vec_reco
    vec_err = np.zeros( numb )
    
    for sig_linear in np.linspace( 0.23, 0.33, 101 ):#101
        for sig_mean in np.linspace( 0.4, 0.5, 101 ):

            vec_reco = Rule_smear.input_data( hist, Input_vec_true ).input_change( sig_linear, sig_mean, 1 ).get_middle()

            for i in range( numb ):
                vec_err[i] = abs( vec_BFit[i] - vec_reco[i] )
            
            error_rel = sum( vec_err )
            vec_err = np.zeros( numb )

            if error_rel < error_comp:
                error_comp = error_rel
                sigma_mean = sig_mean
                sigma_linear = sig_linear
        
        print( sig_linear/0.33*100 )
    return print(sigma_linear, sigma_mean, error_comp)


def error_multiple(Input_vec_true, Input_vec_reco):
    numb = int(len(Input_vec_true))
    error_rel = 0
    error_comp = 1e+10
    sigma_mean = 0
    sigma_linear = 0

    hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )

    vec_BFit = Input_vec_reco
    vec_err = np.zeros( numb )
    
    for sig_linear in np.linspace( 0.23, 0.33, 11 ):#101
        for sig_mean in np.linspace( 0.4, 0.5, 11 ):

            vec_reco = Rule_smear.input_data( hist, Input_vec_true ).input_change( sig_linear, sig_mean, 1 ).get_5to5( )

            for i in range( numb ):
                vec_err[i] = abs( vec_BFit[i] - vec_reco[i] )*vec_BFit[i]
            
            error_rel = sum( vec_err )
            vec_err = np.zeros( numb )

            if error_rel < error_comp:
                error_comp = error_rel
                sigma_mean = sig_mean
                sigma_linear = sig_linear
        
        print( sig_linear/0.33*100 )
    return print(sigma_linear, sigma_mean, error_comp)




if __name__ == '__main__':

    show = 0
    
    if show == 0:
        n = len(In_MNu_true_Nu)
        
        In_all_true = np.zeros( n )
        In_all_reco = np.zeros( n )
        
        for i in range( n ):
            In_all_true[i] = In_MNu_true_Nu[i] + In_MAn_true_Nu[i] + In_MHE_true_Nu[i]
            In_all_reco[i] = In_MNu_reco_Nu[i] + In_MAn_reco_Nu[i] + In_MHE_reco_Nu[i]
        error_different(In_all_true, In_all_reco)

    if show == 1:
        error_different(In_MNu_true_Nu, In_MNu_reco_Nu)
        print("\n")
        error_different(In_MAn_true_Nu, In_MAn_reco_Nu)
        print("\n")
        error_different(In_MHE_true_Nu, In_MHE_reco_Nu)
    
    elif show == 2:
        error_different(In_MNu_true_Nu, In_MNu_reco_Nu)
        print("\n")
        error_multiple(In_MNu_true_Nu, In_MNu_reco_Nu) 
        print("\n")
        error_relativo(In_MNu_true_Nu, In_MNu_reco_Nu)
    
    elif show == 3:
        error_different(In_MAn_true_Nu, In_MAn_reco_Nu)
        print("\n")
        error_multiple(In_MAn_true_Nu, In_MAn_reco_Nu) 
        print("\n")
        error_relativo(In_MAn_true_Nu, In_MAn_reco_Nu)
    
    elif show == 4:
        error_different(In_MHE_true_Nu, In_MHE_reco_Nu)
        print("\n")
        error_multiple(In_MHE_true_Nu, In_MHE_reco_Nu) 
        print("\n")
        error_relativo(In_MHE_true_Nu, In_MHE_reco_Nu)
    
    elif show == 5:
        Input_vec_true = In_MNu_true_Nu
        Input_vec_reco = In_MNu_reco_Nu
        numb = int(len(Input_vec_reco))
        error_rel = 0
        sigma_mean = 0.431#0.45#0.435
        sigma_linear = 0.255#0.25#0.25

        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )

        vec_BFit = Input_vec_reco
        vec_err = np.zeros( numb )


        vec_reco = Rule_smear.input_data( hist, Input_vec_true ).get_5for5_change( sigma_linear, sigma_mean, 1 )

        for i in range( numb ):
            vec_err[i] = abs( vec_BFit[i] - vec_reco[i] )
                
        error_rel = sum( vec_err )
        vec_err = np.zeros( numb )

        print(vec_err, len(vec_err), numb)
        print( vec_BFit )
        print( vec_reco )    
        print(sigma_linear, sigma_mean, error_rel)
   

