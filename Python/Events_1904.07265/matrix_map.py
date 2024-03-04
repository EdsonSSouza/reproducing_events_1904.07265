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


# Gaussian mapping "interpolation" for energy_reco x true_energy: We have En_rec(row) <-> En_true(column)
class Gaussian_interp2D:
    _instance = None

    def __init__(self, energy_reco, energy_true, factor_keep, factor_sqrt, factor_linear, factor_mean, pick_normal) -> None:
        self.en_reco = energy_reco
        self.en_true = energy_true
        
        if factor_keep is None and factor_sqrt is None and factor_linear is None and factor_mean is None and pick_normal is None:    
            self.fac_keep = 0.0
            self.fac_sqrt = 0.0
            self.fac_linear = 0.25
            self.fac_mean = 0.45
            self.pick_normal = 1
        else:
            self.fac_keep = factor_keep
            self.fac_sqrt = factor_sqrt
            self.fac_linear = factor_linear
            self.fac_mean = factor_mean
            self.pick_normal = pick_normal
        
        # Self of the class will be determined by _instance
        Gaussian_interp2D._instance = self
        
    @classmethod
    def input_data( cls, in_energy_reco, in_energy_true ):
        setup_data = cls( in_energy_reco, in_energy_true, None, None, None, None, None )
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def change_parameter( cls, in_factor_keep, in_factor_sqrt, in_factor_linear, in_factor_mean, in_pick_normal ):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(row_en_reco, col_en_true) first. ")
        else:
            cls._instance.fac_keep = in_factor_keep
            cls._instance.fac_sqrt = in_factor_sqrt
            cls._instance.fac_linear = in_factor_linear
            cls._instance.fac_mean = in_factor_mean
            cls._instance.pick_normal = in_pick_normal
        return cls._instance
    

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

                    
                    if self.pick_normal != 0 and self.pick_normal !=1:                                              # coef_normal of Gaussian
                        raise Exception(" Choose pick_normal with 0 for non-normalized or 1 for normalized. ")
                    elif self.pick_normal == 1:
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
        


# Mapping matrix: We have En_rec(row) <-> En_true(column) in the case where we consider the "average of the bin"
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

    # Function that maps En_reco(row) <-> En_true(column) to the bin average 
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

                if en_true[j] < 3.35:
                    vet_result_rate[i,j] = 0
                else:
                    coef_rate = 1/( sigma*np.sqrt( 2*np.pi ) )
                    
                    factor_rate = ( en_reco[i] - mu )/sigma
                    potential_rate = np.exp( - 1/2*factor_rate**2 )

                    vet_result_rate[i,j] = coef_rate*potential_rate

        return vet_result_rate




if __name__ == "__main__":
    import matplotlib.pyplot as plt

    en_reco = np.linspace(0, 20, 201)
    en_true = np.linspace(0, 20, 201)
    
    # Normalized
    gau_interp = Gaussian_interp2D.input_data(en_reco, en_true).get_function2D()
    Z_new = gau_interp(en_reco, en_true)
    
    # Non-Normalized
    Non_interp = Gaussian_interp2D.input_data(en_reco, en_true).change_parameter(0, 0, 0.25, 0.45, 0).get_function2D()
    Z_non_new = Non_interp(en_reco, en_true)
    

    
    """ 
        # Iniciando o plot
    """
 
    #
    ## Normalized: Gaussian
    #
    
    # Creates the figure with a customized proportion
    plt.figure(figsize=(12, 12))

    # Adjust the edges of the frame
    plt.gca().spines['top'].set_linewidth(4)            # Top edge
    plt.gca().spines['right'].set_linewidth(4)          # Right edge
    plt.gca().spines['bottom'].set_linewidth(4)         # Bottom edge
    plt.gca().spines['left'].set_linewidth(4)           # left edge

    # Getting the current axes and setting the scale markers / scale numbers
    ax = plt.gca()
    ax.tick_params(axis='x', direction='in', pad =10, length=25)                # For x-axis markers
    ax.tick_params(axis='y', direction='in', pad=10, length=25)                 # For y-axis markers
    ax.tick_params(axis='both', which='major', width=2.5, labelsize=22)         # For the main numbers: 'major' / 'minor' / 'both'

    # Specifying the values that will appear on the x and y axes
    plt.xticks([0, 3, 5, 10, 15, 20])                                           # Only the values 0, 3., 5, ... , 20 will be shown on the x-axis
    plt.yticks([0, 5, 10, 15, 20])                                              # Only the values 0, 5, 10, ... , 20 will be shown on the y-axis

    # Writing on the frame: text
    plt.text( 1.95, 6, r'$E_{\nu}^{\rm true} < E_{\tau}^{\rm threshold}$', color='white', fontsize=24, rotation=90 )
    plt.text( 11, 12.5, r'$E_{\nu}^{\rm reco.} = E_{\nu}^{\rm true}$', color='white', fontsize=24, rotation=45 )
    
    plt.xlabel( r'$E_{\nu}^{\rm true} \ [{\rm GeV}]$', fontsize=26 )
    plt.ylabel( r'$E_{\nu}^{\rm reco.} \ [{\rm GeV}]$', fontsize=26, labelpad=7 )
    plt.title( r'$P \left( E_{\nu}^{\rm reco.} | E_{\nu}^{\rm true} \right) : {\rm Gaussian \ function}$', fontsize=28, pad=15 )

    # Show the graph: Gaussian
    plt.imshow(Z_new, extent=(0, 20, 0, 20), origin='lower', cmap='viridis')
    cbar = plt.colorbar(shrink=0.81)                                                                                       # Control the size of the colorbar by setting shrink

    # Adds a label to the colorbar
    cbar.set_label( r'$(\ \sigma \ |\ \mu_{\rm mean}\ )=(\ 0.25\ | \ 0.45 \ ) \cdot E_{\nu}^{\rm true}$', fontsize=22, labelpad=10 ) 
    cbar.outline.set_linewidth(3)                                                                                          # Sets the width of the frame
    cbar.ax.tick_params(labelsize=18, direction='in', width=2.5, length=15)                                                # Define the size of the numbers
    cbar.ax.set_yticklabels([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])                                                           # Defines the specific values to be displayed

    x=en_true
    y=x
    plt.plot(x, y, color="black", linewidth=2.6)
    plt.plot([3.35,3.35],[0,20], color="white", linewidth=2.0, linestyle='dashed' )
    
    # Save with .pdf
    plt.savefig('../Image/Event_Gaussian_Norm.pdf', format='pdf')

    # Displaying the graph and pausing execution
    plt.pause(0.01)

    # Waiting for keyboard input to continue
    input("Enter to continue: ")
    plt.close()


    #
    ## Non-Normalized: Gaussian * (np.sqrt(2 pi) * sigma)
    #

    # Creates the figure with a customized proportion
    plt.figure(figsize=(12, 12))

    # Adjust the edges of the frame
    plt.gca().spines['top'].set_linewidth(4)            # Top edge
    plt.gca().spines['right'].set_linewidth(4)          # Right edge
    plt.gca().spines['bottom'].set_linewidth(4)         # Bottom edge
    plt.gca().spines['left'].set_linewidth(4)           # left edge

    # Getting the current axes and setting the scale markers / scale numbers
    ax = plt.gca()
    ax.tick_params(axis='x', direction='in', pad =10, length=25)                # For x-axis markers
    ax.tick_params(axis='y', direction='in', pad=10, length=25)                 # For y-axis markers
    ax.tick_params(axis='both', which='major', width=2.5, labelsize=22)         # For the main numbers: 'major' / 'minor' / 'both'

    # Specifying the values that will appear on the x and y axes
    plt.xticks([0, 3, 5, 10, 15, 20])                                           # Only the values 0, 3., 5, ... , 20 will be shown on the x-axis
    plt.yticks([0, 5, 10, 15, 20])                                              # Only the values 0, 5, 10, ... , 20 will be shown on the y-axis

    # Writing on the frame: text
    plt.text( 1.95, 6, r'$E_{\nu}^{\rm true} < E_{\tau}^{\rm threshold}$', color='white', fontsize=24, rotation=90 )
    plt.text( 11, 12.5, r'$E_{\nu}^{\rm reco.} = E_{\nu}^{\rm true}$', color='white', fontsize=24, rotation=45 )
    
    plt.xlabel( r'$E_{\nu}^{\rm true} \ [{\rm GeV}]$', fontsize=26 )
    plt.ylabel( r'$E_{\nu}^{\rm reco.} \ [{\rm GeV}]$', fontsize=26, labelpad=7 )
    plt.title( r'$P \left( E_{\nu}^{\rm reco.} | E_{\nu}^{\rm true} \right) : {\rm Non-Normalized}$', fontsize=28, pad=15 )

    # Show the graph: Non-Normalized
    plt.imshow(Z_non_new, extent=(0, 20, 0, 20), origin='lower', cmap='viridis')
    cbar = plt.colorbar(shrink=0.81)                                                                                       # Control the size of the colorbar by setting shrink

    # Adds a label to the colorbar
    cbar.set_label( r'$(\ \sigma \ |\ \mu_{\rm mean}\ )=(\ 0.25\ | \ 0.45 \ ) \cdot E_{\nu}^{\rm true}$', fontsize=22, labelpad=10 ) 
    cbar.outline.set_linewidth(3)                                                                                          # Sets the width of the frame
    cbar.ax.tick_params(labelsize=18, direction='in', width=2.5, length=15)                                                # Define the size of the numbers
    cbar.ax.set_yticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])                                                                # Defines the specific values to be displayed

    x=en_true
    y=x
    plt.plot(x, y, color="black", linewidth=2.6)
    plt.plot([3.35,3.35],[0,20], color="white", linewidth=2.0, linestyle='dashed' )

    # Save with .pdf
    plt.savefig('../Image/Event_Gaussian_Non_Norm.pdf', format='pdf')
    
    # Displaying the graph and pausing execution
    plt.pause(0.01)

    # Waiting for keyboard input to continue
    input("Enter to continue: ")
    plt.close()
