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
from scipy.interpolate import RectBivariateSpline as RBS_interp2d


# Gaussian mapping "interpolation" for energy_reco x true_energy: We have En_reco(row) <-> En_true(column)
class Gaussian_interp2D:
    _instance = None

    def __init__(self, energy_reco, energy_true, factor_keep, factor_sqrt, factor_linear, factor_mean, normalized) -> None:
        self.en_reco = energy_reco
        self.en_true = energy_true
        
        if factor_keep is None and factor_sqrt is None and factor_linear is None and factor_mean is None and normalized is None:    
            self.fac_keep = 0.0
            self.fac_sqrt = 0.0
            self.fac_linear = 0.25
            self.fac_mean = 0.45
            self.normalized = 1  # Normalized gaussian
        else:
            self.fac_keep = factor_keep
            self.fac_sqrt = factor_sqrt
            self.fac_linear = factor_linear
            self.fac_mean = factor_mean
            self.normalized = normalized
        # Self of the class will be determined by _instance
        Gaussian_interp2D._instance = self    
    @classmethod
    def input_data( cls, in_energy_reco, in_energy_true ):
        setup_data = cls( in_energy_reco, in_energy_true, None, None, None, None, None )
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def change_parameter( cls, in_factor_keep, in_factor_sqrt, in_factor_linear, in_factor_mean, in_normalized ):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(row_en_reco, col_en_true) first. ")
        else:
            cls._instance.fac_keep = in_factor_keep
            cls._instance.fac_sqrt = in_factor_sqrt
            cls._instance.fac_linear = in_factor_linear
            cls._instance.fac_mean = in_factor_mean
            cls._instance.normalized = in_normalized
        return cls._instance
    
    # Function that returns interpolate  
    def get_function2D(self):
        matrix_interp = np.zeros( (self.en_reco.shape[0], self.en_true.shape[0]) )

        for reco_i in range( self.en_reco.shape[0] ):
            for true_j in range( self.en_true.shape[0] ):

                en_reco_i = self.en_reco[reco_i]
                en_true_j = self.en_true[true_j]

                # Threshold of energy_true: En_true > 3.35
                if en_true_j < 3.35:
                    matrix_interp[reco_i][true_j] = 0.0                                                             # Defining the Gaussian matrix
                else:
                    sigma_gau = self.fac_keep + \
                                self.fac_sqrt * np.sqrt( en_true_j ) + \
                                self.fac_linear * en_true_j                                                         # sigma = c0 + a0*sqrt(En_true) + b0*En_true      
                    mean_gau = self.fac_mean * en_true_j                                                            # mu_mean = b1*En_true

                    if self.normalized != 0 and self.normalized != 1:                                               # coef_normal of Gaussian
                        raise Exception(" Set normalization with 0 for non-normalized or 1 for normalized. ")
                    elif self.normalized == 1:
                        coef_normal = 1/( np.sqrt( 2*np.pi )*sigma_gau )                                            
                    else:
                        coef_normal = 1
                    #
                    coef_factor = ( en_reco_i - mean_gau )/sigma_gau                                                # coef_factor of Gaussian
                    #
                    expression_gau = coef_normal*np.exp( -0.5*coef_factor**2 )                                      # function_gaussian = coef_normal * exp(- 0.5*coef_factor**2 )
                    
                    if expression_gau < 1e-5:                                                                       # Defining the Gaussian matrix
                        matrix_interp[reco_i][true_j] = 0.0
                    else:
                        matrix_interp[reco_i][true_j] = expression_gau
        
        gaussian_interp2D = RBS_interp2d( self.en_reco, self.en_true, matrix_interp )                               # Making the interpolation

        return gaussian_interp2D


# Mapping matrix: We have En_reco(row) <-> En_true(column) in the case where we consider the "average of the bin"
class Mapping_matrix:
    _instance = None

    def __init__( self, row_en_reco, col_en_true, factor_keep, factor_sqrt, factor_linear, factor_mean ):
        self.row_en_reco = row_en_reco
        self.col_en_true = col_en_true

        if factor_keep is None and factor_sqrt is None and factor_linear is None and factor_mean is None:
            self.factor_keep = 0.0
            self.factor_sqrt = 0.0
            self.factor_linear = 0.25
            self.factor_mean = 0.45
        else:
            self.factor_keep = factor_keep
            self.factor_sqrt = factor_sqrt
            self.factor_linear = factor_linear
            self.factor_mean = factor_mean
        # Self of the class will be determined by _instance
        Mapping_matrix._instance = self
    @classmethod
    def input_data(cls, in_row_en_reco, in_col_en_true):
        setup_data = cls(in_row_en_reco, in_col_en_true, None, None, None, None)
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def change_parameter(cls, in_factor_keep, in_factor_sqrt, in_factor_linear, in_factor_mean):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(row_en_reco, col_en_true) first. ")
        else:
            cls._instance.factor_keep = in_factor_keep
            cls._instance.factor_sqrt = in_factor_sqrt
            cls._instance.factor_linear = in_factor_linear
            cls._instance.factor_mean = in_factor_mean
        return cls._instance

    # Function that maps En_reco(row) <-> En_true(column) "to the bin average"
    def get_mapping_mean(self):
        b = self.factor_mean                                                                     # Parameters 
        r_keep = self.factor_keep
        r_sqrt = self.factor_sqrt
        r_linear = self.factor_linear

        en_reco = self.row_en_reco                                                               # Energy: True and Reconstruction        
        en_true = self.col_en_true

        vet_result_rate = np.zeros( ( len(en_reco), len(en_true) ) )                             # Final vector result : Initializing

        for i in range( len(en_reco) ):                                                          # Construction of the matrix_mapping
            for j in range( len(en_true) ):

                mu = b * en_true[j]
                sigma = r_keep + r_sqrt*np.sqrt( en_true[j] ) + r_linear*en_true[j]

                # Threshold of energy_true: En_true > 3.35
                if en_true[j] < 3.35 and en_true[j] != 3.25:                                            # Lower limit 3.35 and outside the first bin_true not null
                    vet_result_rate[i,j] = 0
                    
                elif en_true[j] < 3.35 and en_true[j] == 3.25:                                          # Lower limit 3.35 and equal to 3.25: special rules for the first non-zero bin
                    en_bin_1st = 3.35
                    mu_1st = b * en_bin_1st
                    sig_1st = r_keep + r_sqrt*np.sqrt(en_bin_1st) + r_linear*en_bin_1st

                    coef_rate = 1/( np.sqrt( 2*np.pi ) * sig_1st )
                    
                    factor_rate = ( en_reco[i] - mu_1st )/sig_1st
                    potential_rate = np.exp( - 1/2*factor_rate**2 )

                    vet_result_rate[i,j] = coef_rate*potential_rate 
                   
                else:                                                                                   # Rest:
                    coef_rate = 1/( sigma*np.sqrt( 2*np.pi ) )
                    
                    factor_rate = ( en_reco[i] - mu )/sigma
                    potential_rate = np.exp( - 1/2*factor_rate**2 )

                    vet_result_rate[i,j] = coef_rate*potential_rate

        return vet_result_rate

