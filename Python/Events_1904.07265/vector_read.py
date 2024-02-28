###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				18th Fev 2024	                  #####
###########################################################

import pandas as pd


# Name of the file to be imported
def read_arq(name_arq):
    table = pd.read_csv( name_arq, delimiter='\t', header=None ) 
    vector_used = [ table.iloc[row_i][1]     for row_i in range( len(table) ) ] # Row [i] and second column ([1]) -> [i][1]
    return vector_used

