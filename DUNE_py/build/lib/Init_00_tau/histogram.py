###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				18th Fev 2024	                  #####
###########################################################

""" 
Description about this script:
    The purpose of this script is to create histograms. In particular, we have three different ways of doing this:
        get_Uniform_LR: we used this option when we knew the numbers of the bins and the start and end points of the energy spectrum
        get_Uniform_SP: we used this option when we knew the starting point of the energy spectrum and the numbers and width of the bins
        get_Uniform_WB: we used this option when we knew the width of the bins and the endges points of the energy spectrum
"""

import numpy as np


class Bin:
    def __init__(self, left:float, right:float) -> None:
        self.left  = left
        self.right = right


class Histogram:
    def __init__(self, list_in:np.ndarray) -> None:
        self.bins = []
        for i in range( len(list_in)-1 ):
            bin_interval = Bin(list_in[i], list_in[i+1]) # Forming pairs (bin)
            self.bins.append( bin_interval )
    @classmethod
    # Uniform histogram (LR): Left_min - Right_max (LR) / number bins
    # LR : Left_Right
    def get_Uniform_LR( cls, Left_min:float, Right_max:float, number_bin:int ) -> None:   
        """ Note: I know point_Left, point_Right and numbers_bin """
        bins_LR = np.linspace( Left_min, Right_max, int(number_bin)+1 )
        hist_LR = cls( bins_LR )
        return hist_LR                                                                          # new values in list_in
    @classmethod
    # Uniform histogram (SP): Start Point (SP) / number bins / interval
    # SP : Start_Point
    def get_Uniform_SP( cls, StarPoint_in:float, number_bin:int, width_bin:float ) -> None: 
        """ Note: I know point_Started (initial), numbers_bin and width_bin """
        bins_sp = [ StarPoint_in + width_bin*i for i in range( int(number_bin)+1 ) ]
        hist_sp = cls( bins_sp )
        return hist_sp                                                                          # new values in list_in
    @classmethod
    # Uniform histogram (WB): left_min / right_max / Width_Bin (WB)
    # WB : Width_Bin
    def get_Uniform_WB( cls, left_min:float, right_max:float, Width_Bin:float ) -> None:
        """ Note: I know point_left, point_right and width_bin """
        elem_number = (right_max - left_min)/Width_Bin + 1
        bins_wb = np.linspace( left_min, right_max, int(elem_number) )
        hist_wb = cls( bins_wb )
        return hist_wb                                                                          # new values in list_in



if __name__ == "__main__":
    print( f"{ Bin(2,4).left, Bin(2,4).right }\n" )

    print( f"{Histogram.get_Uniform_LR(2,6,4).bins[0].right}\n" )
    print( f"{Histogram.get_Uniform_SP(2,4,1).bins[0].right}\n" )
    print( f"{Histogram.get_Uniform_WB(2,6,1).bins[0].right}" )
    
    