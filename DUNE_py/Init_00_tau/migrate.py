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
#   Normalization: 0 Off / 1 On
class Gaussian_interp2D:
    _instance = None
    def __init__(self, energy, factor_keep, factor_sqrt, factor_linear, factor_mean, normalized) -> None:
        self.en = energy    
        if factor_keep is None and factor_sqrt is None and factor_linear is None and factor_mean is None and normalized is None:    
            self.fac_keep   = 0.0
            self.fac_sqrt   = 0.0
            self.fac_linear = 0.256                                 # sigma  = 0.256
            self.fac_mean   = 0.436                                 # fac_mu = 0.436
            self.normalized = 1                                     # Normalized gaussian: On
        else:
            self.fac_keep   = factor_keep
            self.fac_sqrt   = factor_sqrt
            self.fac_linear = factor_linear
            self.fac_mean   = factor_mean
            self.normalized = normalized
        # Self of the class will be determined by _instance
        Gaussian_interp2D._instance = self    
    @classmethod
    def input_data( cls, energy ):
        setup_data    = cls( energy, None, None, None, None, None )
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def input_change( cls, factor_keep, factor_sqrt, factor_linear, factor_mean, normalized ):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(row_energy) first. ")
        else:
            cls._instance.fac_keep   = factor_keep
            cls._instance.fac_sqrt   = factor_sqrt
            cls._instance.fac_linear = factor_linear
            cls._instance.fac_mean   = factor_mean
            cls._instance.normalized = normalized
        return cls._instance
      
    def get_function2D(self):                                                                                       # Function that returns "interpolate" in 2D
        matrix_interp = np.zeros( (self.en.shape[0], self.en.shape[0]) )
        for reco in range( self.en.shape[0] ):
            for true in range( self.en.shape[0] ):
                en_reco = self.en[reco]
                en_true = self.en[true]

                if en_true < 3.35:                                                                                  # Threshold of energy_true: En_true > 3.35
                    matrix_interp[reco][true] = 0.0                                                                 # Defining the Gaussian matrix
                else:
                    sigma_gau = self.fac_keep + \
                                self.fac_sqrt * np.sqrt( en_true ) + \
                                self.fac_linear * en_true                                                           # sigma = c0 + a0*sqrt(En_true) + b0*En_true      
                    mean_gau  = self.fac_mean * en_true                                                             # mu_mean = b1*En_true

                    if self.normalized == 1:                                                                        # coef_normal of Gaussian
                        coef_normal = 1/( np.sqrt( 2*np.pi )*sigma_gau )
                    elif self.normalized == 0:
                        coef_normal = 1
                    else:                                               
                        raise Exception(" Set normalization with 0 for non-normalized or 1 for normalized. ")
                    #
                    coef_factor = ( en_reco - mean_gau )/sigma_gau                                                  # coef_factor of Gaussian
                    #
                    expression_gau = coef_normal*np.exp( -0.5*coef_factor**2 )                                      # function_gaussian = coef_normal * exp(- 0.5*coef_factor**2 )
                    
                    if expression_gau < 1e-5:                                                                       # Defining the Gaussian matrix
                        matrix_interp[reco][true] = 0.0
                    else:
                        matrix_interp[reco][true] = expression_gau
        return RBS_interp2d( self.en, self.en, matrix_interp )                                                      # Making the interpolation


# Mapping matrix: We have En_reco(row) <-> En_true(column) in the case where we consider the "average of the bin"
class Mapping_matrix:
    _instance = None
    def __init__( self, energy, factor_keep, factor_sqrt, factor_linear, factor_mean ):
        self.en = energy
        if factor_keep is None and factor_sqrt is None and factor_linear is None and factor_mean is None:
            self.factor_keep   = 0.0
            self.factor_sqrt   = 0.0
            self.factor_linear = 0.256                                 # sigma  = 0.256
            self.factor_mean   = 0.436                                 # fac_mu = 0.436
        else:
            self.factor_keep   = factor_keep
            self.factor_sqrt   = factor_sqrt
            self.factor_linear = factor_linear
            self.factor_mean   = factor_mean
        # Self of the class will be determined by _instance
        Mapping_matrix._instance = self
    @classmethod
    def input_data(cls, energy):
        setup_data    = cls(energy, None, None, None, None)
        cls._instance = setup_data
        return cls._instance
    @classmethod
    def input_change(cls, factor_keep, factor_sqrt, factor_linear, factor_mean):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(energy) first. ")
        else:
            cls._instance.factor_keep   = factor_keep
            cls._instance.factor_sqrt   = factor_sqrt
            cls._instance.factor_linear = factor_linear
            cls._instance.factor_mean   = factor_mean
        return cls._instance

    def get_mapping_mean(self):                                                                         # Function that maps En_reco(row) <-> En_true(column) "to the bin average"
        b = self.factor_mean                                                                            # Parameters 
        r_keep = self.factor_keep
        r_sqrt = self.factor_sqrt
        r_linear = self.factor_linear

        en_reco = self.en                                                                               # Energy: True and Reconstruction        
        en_true = self.en

        vet_result_rate = np.zeros( ( len(en_reco), len(en_true) ) )                                    # Final vector result : Initializing
        for i in range( len(en_reco) ):                                                                 # Construction of the matrix_mapping
            for j in range( len(en_true) ):
                mu = b * en_true[j]
                sigma = r_keep + r_sqrt*np.sqrt( en_true[j] ) + r_linear*en_true[j]

                # Threshold of energy_true: En_true > 3.35
                if en_true[j] < 3.35 and en_true[j] != 3.25:                                            # Lower limit 3.35 and outside the first bin_true not null
                    vet_result_rate[i,j] = 0
                    
                elif en_true[j] < 3.35 and en_true[j] == 3.25:                                          # Lower limit 3.35 and equal to 3.25: special rules for the first non-zero bin
                    en_bin_1st = (3.35+3.5)*0.5
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



if __name__ == "__main__":
    import os
    import matplotlib.pyplot as plt

    show = 1

    if show == 1:
        energy = np.linspace(0, 20, 401)
        Func = Gaussian_interp2D.input_data(energy).get_function2D()
        print( Func(1.25, (3.35+3.5)*0.5) )
        print( Func(1.25, 3.35) )
        print( Func(1.25, 3.75) )
    
    elif show == 2:
        energy = np.linspace(0.25, 19.75, 40)
        Func = Mapping_matrix.input_data(energy).get_mapping_mean()
        print( energy )
        print()
        print( Func[3][7] )
        print( Func[3][8] )
    
    elif show == 3:
        #directory_here = os.getcwd()
        new_directory = '/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau'
        os.chdir( new_directory )

        energy = np.linspace(0, 20, 401)
        
        # Normalized
        gau_interp = Gaussian_interp2D.input_data(energy).input_change(0, 0, 0.256, 0.436, 1).get_function2D()
        Z_new = gau_interp(energy, energy)
        
        # Non-Normalized
        Non_interp = Gaussian_interp2D.input_data(energy).input_change(0, 0, 0.256, 0.436, 0).get_function2D()
        Z_non_new = Non_interp(energy, energy)
        
        
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
        ax.tick_params(axis='y', direction='in', pad =10, length=25)                # For y-axis markers
        ax.tick_params(axis='both', which='major', width=2.5, labelsize=24)         # For the main numbers: 'major' / 'minor' / 'both'

        # Specifying the values that will appear on the x and y axes
        plt.xticks([0, 3, 5, 10, 15, 20])                                           # Only the values 0, 3., 5, ... , 20 will be shown on the x-axis
        plt.yticks([0, 5, 10, 15, 20])                                              # Only the values 0, 5, 10, ... , 20 will be shown on the y-axis

        # Writing on the frame: text
        plt.text( 1.95, 6, r'$E_{\nu}^{\rm true} < E_{\tau}^{\rm threshold}$', color='white', fontsize=24, rotation=90 )
        plt.text( 11, 12.5, r'$E_{\nu}^{\rm reco.} = E_{\nu}^{\rm true}$', color='white', fontsize=24, rotation=45 )
        
        plt.xlabel( r'$E_{\nu}^{\rm true} \ [{\rm GeV}]$', fontsize=27 )
        plt.ylabel( r'$E_{\nu}^{\rm reco.} \ [{\rm GeV}]$', fontsize=27, labelpad=8 )
        plt.title( r'$P \left( E_{\nu}^{\rm reco.} | E_{\nu}^{\rm true} \right) : {\rm Gaussian \ function}$', fontsize=28, pad=15 )

        # Show the graph: Gaussian
        plt.imshow(Z_new, extent=(0, 20, 0, 20), origin='lower', cmap='viridis')
        cbar = plt.colorbar(shrink=0.985)                                                                                      # Control the size of the colorbar by setting shrink

        # Adds a label to the colorbar
        cbar.set_label( r'$(\ \sigma \ |\ \mu_{\rm mean}\ )=(\ 0.256\ | \ 0.436 \ ) \cdot E_{\nu}^{\rm true}$', fontsize=22, labelpad=10 ) 
        cbar.outline.set_linewidth(3)                                                                                          # Sets the width of the frame
        cbar.ax.tick_params(labelsize=18, direction='in', width=2.5, length=15)                                                # Define the size of the numbers
        cbar.ax.set_yticklabels([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])                                                                # Defines the specific values to be displayed

        en_true = energy
        en_reco = en_true
        plt.plot(en_true, en_reco, color="black", linewidth=2.6)
        plt.plot([3.35,3.35],[0,20], color="white", linewidth=2.0, linestyle='dashed' )
        
        # Save with .pdf
        #plt.savefig('../Image_article/Event_Gaussian_Norm.pdf', format='pdf')

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
        
        plt.xlabel( r'$E_{\nu}^{\rm true} \ [{\rm GeV}]$', fontsize=27 )
        plt.ylabel( r'$E_{\nu}^{\rm reco.} \ [{\rm GeV}]$', fontsize=27, labelpad=8 )
        plt.title( r'$P \left( E_{\nu}^{\rm reco.} | E_{\nu}^{\rm true} \right) : {\rm Non-Normalized}$', fontsize=28, pad=15 )

        # Show the graph: Non-Normalized
        plt.imshow(Z_non_new, extent=(0, 20, 0, 20), origin='lower', cmap='viridis')
        cbar = plt.colorbar(shrink=0.985)                                                                                      # Control the size of the colorbar by setting shrink

        # Adds a label to the colorbar
        cbar.set_label( r'$(\ \sigma \ |\ \mu_{\rm mean}\ )=(\ 0.256\ | \ 0.436 \ ) \cdot E_{\nu}^{\rm true}$', fontsize=22, labelpad=10 ) 
        cbar.outline.set_linewidth(3)                                                                                          # Sets the width of the frame
        cbar.ax.tick_params(labelsize=18, direction='in', width=2.5, length=15)                                                # Define the size of the numbers
        cbar.ax.set_yticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])                                                                # Defines the specific values to be displayed

        en_true = energy
        en_reco = en_true
        plt.plot(en_true, en_reco, color="black", linewidth=2.6)
        plt.plot([3.35,3.35],[0,20], color="white", linewidth=2.0, linestyle='dashed' )

        # Save with .pdf
        #plt.savefig('../Image_article/Event_Gaussian_Non_Norm.pdf', format='pdf')
        
        # Displaying the graph and pausing execution
        plt.pause(0.01)

        # Waiting for keyboard input to continue
        input("Enter to continue: ")
        plt.close()

