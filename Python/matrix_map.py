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


# Mapping matrix: In constructing the matrix, we have Etrue(column) <-> Erec(row)
class Mapping_matrix:
    _instance = None

    def __init__( self, row_en_reco, col_en_true, fator_sig_keep, fator_sig_sqrt, fator_sig_linear, fator_mean ):
        self.row_en_reco = row_en_reco
        self.col_en_true = col_en_true

        if fator_sig_keep is None and fator_sig_sqrt is None and fator_sig_linear is None and fator_mean is None:
            self.fator_sig_keep = 0.0
            self.fator_sig_sqrt = 0.0
            self.fator_sig_linear = 0.25
            self.fator_mean = 0.45
        else:
            self.fator_sig_keep = fator_sig_keep
            self.fator_sig_sqrt = fator_sig_sqrt
            self.fator_sig_linear = fator_sig_linear
            self.fator_mean = fator_mean
        
        # Self of the class will be determined by _instance
        Mapping_matrix._instance = self

    @classmethod
    def input_data(cls, in_row_en_reco, in_col_en_true):
        setup_data = cls(in_row_en_reco, in_col_en_true, None, None, None, None)
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def change_parameter(cls, in_fator_sig_keep, in_fator_sig_sqrt, in_fator_sig_linear, in_fator_mean):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(row_en_reco, col_en_true) first. ")
        else:
            cls._instance.fator_sig_keep = in_fator_sig_keep
            cls._instance.fator_sig_sqrt = in_fator_sig_sqrt
            cls._instance.fator_sig_linear = in_fator_sig_linear
            cls._instance.fator_mean = in_fator_mean
        return cls._instance


    def mapping_by_sum(self):
        
        # Parameters
        b = self.fator_mean
        r_keep = self.fator_sig_keep
        r_sqrt = self.fator_sig_sqrt
        r_linear = self.fator_sig_linear

        # Energy: True and Reconstruction
        en_true = self.col_en_true
        en_reco = self.row_en_reco

        # Final vector result : Initializing
        vet_result_rate = np.zeros( ( len(en_reco), len(en_true) ) )

        # Construction of the matrix_mapping
        for i in range( len(en_reco) ):
            for j in range( len(en_true) ):

                mu = b * en_true[j]
                sigma = r_keep + r_sqrt*np.sqrt( en_true[j] ) + r_linear*en_true[j]

                if sigma == 0:
                    vet_result_rate[i,j] = 0
                else:
                    coef_rate = 1/( sigma*np.sqrt( 2*np.pi ) )
                    
                    fator_rate = ( en_reco[i] - mu )/sigma
                    potential_rate = np.exp( - 1/2*fator_rate**2 )

                    vet_result_rate[i,j] = coef_rate*potential_rate

        return vet_result_rate

