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

 
class Bin:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Histogram:
    def __init__(self, list_in) -> None:
        self.bins = []
        for i in range( len(list_in)-1 ):
            bin_interval = Bin(list_in[i], list_in[i+1]) # Forming pairs (bin)
            self.bins.append( bin_interval )
    
    @classmethod
    # Uniform histogram (LR): Left_min / Right_max / number bins
    def get_Uniform_LR(cls, Left_min, Right_max, number_bin): # n_bin: number of bins in the histogram
        bins_LR = np.linspace(Left_min, Right_max, int(number_bin)+1)
        hist_LR = cls(bins_LR)
        return hist_LR # new values in list_in
    
    @classmethod
    # Uniform histogram (SP): Start Point / number bins / interval
    def def_Uniform_SP(cls, StarPoint_in, number_bin, wigth_bin): # n_bin: number of bins in the histogram
        bins_sp = [ StarPoint_in + wigth_bin*i for i in range( number_bin+1 ) ]
        hist_sp = cls(bins_sp)
        return hist_sp # new values in list_in




if __name__ == "__main__":
    a=1
    print( f"{ Bin(2,4).left }" )

