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
import pandas as pd


# Name of the table to be imported
def read_fit4D(name_tab):
    table = pd.read_csv( name_tab, delim_whitespace=True, header=None )                             # Read tada from the table using pd.read_csv

    table.columns = ['column1', 'column2', 'column3', 'column4', 'chi2_last']                       # Rename the columns for easier access
    
    col1_used = table['column1'].values                                                             # Separate the data into three vectors
    col2_used = table['column2'].values
    col3_used = table['column3'].values
    col4_used = table['column4'].values
    chi2_used = table['chi2_last'].values
    
    return col1_used, col2_used, col3_used, col4_used, chi2_used



"""     

    Tables of Fit_4D: 

"""
# Path to the Mathematic directory: Input Files
#directory_path = "/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/SM_01_DUNE/my_data"
directory_path = "/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/SM_01_DUNE"

# Names of files
Fit4D_free = "DUNE_fit_SM_4Dfree.dat"                                      # Names of files: Free_4D
# Join: directory_path/name_file:                                          # Directory (Join): dir_path/name_file:
fit4D_free = os.path.join(directory_path, Fit4D_free)                          # delta_cp x sin2_13 x sin2_23 x dm2_31 x chi2
# Input: three arrays (col1, col2 and chi2) in:                            # Three arrays (col1, col2 and chi2):
In_4D_free = read_fit4D( fit4D_free )                                          # dcp[0] x s13[1] x s23[2] x dm31[3] x chi2[4]



"""     

    Reducing of Fit_4D to Fit_2D: 

"""
class Fit4D_to_Fit2D:
    def __init__(self, tab_4D) -> None:
        self.tab_4D = tab_4D
    
    def dcp_and_s23(self,  name):
        df = self.tab_4D

        n = int( round( ( np.shape(df)[1] )**( 1/(np.shape(df)[0] - 1) ) , 0) )
        print(n)

        dcp  = np.zeros(n)      # to col1 = df[0]                                               # Defining the 2 fixed variables
        s13  = np.zeros(n)      # to col2 = df[1]
        s23  = np.zeros(n)      # to col3 = df[2]
        dm31 = np.zeros(n)      # to col4 = df[3]

        for i in range(0,n,1):                                                                  # Number of points being varied
            dcp[i]  = df[0][n*n*n*i]

        for i in range(0,n,1):
            s13[i]  = df[1][n*n*i]

        for i in range(0,n,1):
            s23[i]  = df[2][n*i]
    
        for i in range(0,n,1):
            dm31[i] = df[3][i]

        chi2_4D = np.zeros( shape=(n, n, n, n) )                                                # chi2_4D: All Free

        for i0 in range(0,n,1):                                                                 # Filling the chi2_4D
            for i1 in range(0,n,1):
                for i2 in range(0,n,1):
                    for i3 in range(0,n,1):
                        chi2_4D[i0][i1][i2][i3] = df[4][ n*n*n*i0 + n*n*i1 + n*i2 + i3 ]        # chi2_4D[0][1][2][3] : where [0] and [2] are the fixed variables,
                                                                                                #                       while [1] and [3] are the marginalized variables. 

        chi2_3D = np.min( chi2_4D, axis=3 )                                                     # Maginalize on axis : 3 

        chi2_2D = np.min( chi2_3D, axis=1 )                                                     # Maginalize on axis : 1 


        # Escolha o diretório onde você quer salvar o arquivo
        dir = '/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/SM_01_DUNE/my_data/fit_2D/'              # Directory in which it will be saved
        name_file = str(name)                                                                                       # Name of the file to save
        path_file = os.path.join(dir, name_file)                                                                    # Complete file path

        with open(path_file, 'w') as save_file:                                                                     # Open the file for writing
            for i in range(0,n,1):
                for j in range(0,n,1):
                    save_file.write( "{:<10} {:<10} {:<12}\n".format( dcp[i], s23[j], chi2_2D[i][j] ) )
        
        return print( np.shape( chi2_2D ) )




if __name__== "__main__":
  Fit4D_to_Fit2D( In_4D_free ).dcp_and_s23( 'DUNE_SM_Far_fit2D_dcp_s23.dat' )
