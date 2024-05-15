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


# Name of the table to be imported
def read_fit2D(name_tab):
    table = pd.read_csv( name_tab, delim_whitespace=True, header=None )       # Read tada from the table using pd.read_csv

    table.columns = ['column1', 'column2', 'chi2_last']                       # Rename the columns for easier access
    
    col1_used = table['column1'].values                                       # Separate the data into three vectors
    col2_used = table['column2'].values
    chi2_used = table['chi2_last'].values
    
    return col1_used, col2_used, chi2_used


"""     

    Tables of Fit_2D: 

"""
# Path to the Mathematic directory: Input Files
directory_path = "/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/Python/02_SM_DUNE/my_data"

# Names of files
Fit2D_dcp_s23 = "DUNE_fit_SM_dcp_s23.dat"                                      # delta_cp x sin2_23 x chi2
#   Fit2D_dcp_s23 = "Neut_fit_SM_dcp_s23.dat"
Fit2D_s13_s23 = "DUNE_fit_SM_s13_s23.dat"                                      # sin2_13 x sin2_23 x chi2
Fit2D_s13_m31 = "DUNE_fit_SM_s13_dm31.dat"                                     # sin2_13 x dm_31 x chi2

# Join: directory_path/name_file:                                          # Directory (Join): dir_path/name_file:
fit2D_dcp_s23 = os.path.join(directory_path, Fit2D_dcp_s23)                    # delta_cp x sin2_23 x chi2
fit2D_s13_s23 = os.path.join(directory_path, Fit2D_s13_s23)                    # sin2_13 x sin2_23 x chi2
fit2D_s13_m31 = os.path.join(directory_path, Fit2D_s13_m31)                     # sin2_13 x dm_31 x chi2


# Input: three arrays (col1, col2 and chi2) in:                            # Three arrays (col1, col2 and chi2):
In_dcp_s23 = read_fit2D( fit2D_dcp_s23 )                                        # dcp[0] x s23[1] x chi2[2]
In_s13_s23 = read_fit2D( fit2D_s13_s23 )                                        # s13[0] x s23[1] x chi2[2]
In_s13_m31 = read_fit2D( fit2D_s13_m31 )                                        # s13[0] x dm31[1] x chi2[2]

