###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				06th Mar 2024	                  #####
###########################################################

import numpy as np

# Import our library
from Init_00_tau.read_vec import *


# Function Chi^2:
class Chi2_build:
    def __init__(self, data, model, normalize_NC) -> None:
        self.dat  = data
        self.mod  = model
        self.norm = normalize_NC

        if self.dat == 0:
            self.chi = 2*( self.mod - self.dat ) + (4*self.norm)**2
        elif self.dat != 0 and self.mod != 0:
            self.chi = 2*( self.mod - self.dat + self.dat * np.log( self.dat/self.mod ) ) + ( 4*self.norm )**2    # 1/0.25 = 4
        else:
            self.mod = 5e-5
            self.chi = 2*( self.mod - self.dat + self.dat * np.log( self.dat/self.mod ) ) + ( 4*self.norm )**2


#  Neutrino and Antineutrino Mode: For 3.5 + 3.5 years
class Chi2BC:
    def __init__( self, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti ) -> None:
        self.cal_MNu_Nu   = Calc_MNu_reco_Nu
        self.cal_MAn_Nu   = Calc_MAn_reco_Nu
        self.cal_MNu_Anti = Calc_MNu_reco_Anti
        self.cal_MAn_Anti = Calc_MAn_reco_Anti
    @classmethod
    def input_data( cls, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti ):
        return cls( Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti )

    # Neutrino Mode: Neutrino
    def get_MNu_Nu( self, alpha ):
        numb_loop = len( Pre_cal_MNu_Nu )
        if len( self.cal_MNu_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )        
        Ndat_Nu = [ Pre_cal_MNu_Nu[i]           for i in range(numb_loop) ]    
        Nmod_Nu = [ self.cal_MNu_Nu[i]          for i in range(numb_loop) ]
        return sum( [ Chi2_build( Ndat_Nu[i] + (1 + alpha) * In_MNu_BG[i], \
                                  Nmod_Nu[i] + (1 + alpha) * In_MNu_BG[i], alpha ).chi          for i in range(numb_loop) ] )
    # Antineutrino Mode: Neutrino
    def get_MAn_Nu( self, alpha ):
        numb_loop = len( Pre_cal_MAn_Nu )
        if len( self.cal_MAn_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Nu = [ Pre_cal_MAn_Nu[i]           for i in range(numb_loop) ]    
        Nmod_Nu = [ self.cal_MAn_Nu[i]          for i in range(numb_loop) ]
        return sum( [ Chi2_build( Ndat_Nu[i] + (1 + alpha) * In_MAn_BG[i], \
                                  Nmod_Nu[i] + (1 + alpha) * In_MAn_BG[i], alpha ).chi          for i in range(numb_loop) ] )  
    # Neutrino Mode: Antineutrino
    def get_MNu_Anti( self, alpha ):
        numb_loop = len( Pre_cal_MNu_Anti )
        if len( self.cal_MNu_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = [ Pre_cal_MNu_Anti[i]       for i in range(numb_loop) ]
        Nmod_Anti = [ self.cal_MNu_Anti[i]      for i in range(numb_loop) ]
        return sum( [ Chi2_build( Ndat_Anti[i] + ( 1 + alpha ) * In_MNu_BG[i], \
                                  Nmod_Anti[i] + ( 1 + alpha ) * In_MNu_BG[i], alpha ).chi      for i in range(numb_loop) ] )  
    # Antineutrino Mode: Antineutrino
    def get_MAn_Anti( self, alpha ):
        numb_loop = len( Pre_cal_MAn_Anti )
        if len( self.cal_MAn_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = [ Pre_cal_MAn_Anti[i]       for i in range(numb_loop) ]
        Nmod_Anti = [ self.cal_MAn_Anti[i]      for i in range(numb_loop) ]
        return sum( [ Chi2_build( Ndat_Anti[i] + ( 1 + alpha ) * In_MAn_BG[i], \
                                  Nmod_Anti[i] + ( 1 + alpha ) * In_MAn_BG[i], alpha ).chi      for i in range(numb_loop) ] )
    # All things together: Modes and Particles
    def get_all( self, alpha ):
        chi2_all = self.get_MNu_Nu(alpha) + self.get_MAn_Nu(alpha) + self.get_MNu_Anti(alpha) + self.get_MAn_Anti(alpha)
        return chi2_all


# Neutrino and Antineutrino Mode: For 3 + 3 + 1 years
class Chi2BC_331:
    def __init__( self, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MHE_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti ) -> None:
        self.cal_MNu_Nu   = Calc_MNu_reco_Nu
        self.cal_MAn_Nu   = Calc_MAn_reco_Nu
        self.cal_MHE_Nu   = Calc_MHE_reco_Nu
        self.cal_MNu_Anti = Calc_MNu_reco_Anti
        self.cal_MAn_Anti = Calc_MAn_reco_Anti
    @classmethod
    def input_data( cls, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MHE_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti ):
        return cls( Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MHE_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti )

    # Neutrino Mode: Neutrino
    def get_MNu_Nu( self, alpha ):
        fac331 = 0.857142857                                                         #EScrever: 3/3.5
        numb_loop = len( Pre_cal_MNu_Nu )
        if len( self.cal_MNu_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )        
        Ndat_Nu = [ Pre_cal_MNu_Nu[i]           for i in range(numb_loop) ]    
        Nmod_Nu = [ self.cal_MNu_Nu[i]          for i in range(numb_loop) ]
        return sum( [ Chi2_build( fac331*Ndat_Nu[i] + (1 + alpha) * fac331*In_MNu_BG[i], \
                                  fac331*Nmod_Nu[i] + (1 + alpha) * fac331*In_MNu_BG[i], alpha ).chi    for i in range(numb_loop) ] )
    # Antineutrino Mode: Neutrino
    def get_MAn_Nu( self, alpha ):
        fac331 = 0.857142857 #3/3.5
        numb_loop = len( Pre_cal_MAn_Nu )
        if len( self.cal_MAn_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Nu = [ Pre_cal_MAn_Nu[i]           for i in range(numb_loop) ]    
        Nmod_Nu = [ self.cal_MAn_Nu[i]          for i in range(numb_loop) ]
        return sum( [ Chi2_build( fac331*Ndat_Nu[i] + (1 + alpha) * fac331*In_MAn_BG[i], \
                                  fac331*Nmod_Nu[i] + (1 + alpha) * fac331*In_MAn_BG[i], alpha ).chi    for i in range(numb_loop) ] )
    # High Energy Mode: Neutrino
    def get_MHE_Nu( self, alpha ):
        fac331 = 1
        numb_loop = len( Pre_cal_MHE_Nu )
        if len( self.cal_MHE_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Nu = [ Pre_cal_MHE_Nu[i]           for i in range(numb_loop) ]    
        Nmod_Nu = [ self.cal_MHE_Nu[i]          for i in range(numb_loop) ]
        return sum( [ Chi2_build( fac331*Ndat_Nu[i] + (1 + alpha) * fac331*In_MHE_BG[i], \
                                  fac331*Nmod_Nu[i] + (1 + alpha) * fac331*In_MHE_BG[i], alpha ).chi    for i in range(numb_loop) ] )
    # Neutrino Mode: Antineutrino
    def get_MNu_Anti( self, alpha ):
        fac331 = 0.857142857 #3/3.5
        numb_loop = len( Pre_cal_MNu_Anti )
        if len( self.cal_MNu_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = [ Pre_cal_MNu_Anti[i]       for i in range(numb_loop) ]
        Nmod_Anti = [ self.cal_MNu_Anti[i]      for i in range(numb_loop) ]
        return sum( [ Chi2_build( fac331*Ndat_Anti[i] + ( 1 + alpha ) * fac331*In_MNu_BG[i], \
                                  fac331*Nmod_Anti[i] + ( 1 + alpha ) * fac331*In_MNu_BG[i], alpha ).chi    for i in range(numb_loop) ] )  
    # Antineutrino Mode: Antineutrino
    def get_MAn_Anti( self, alpha ):
        fac331 = 0.857142857 #3/3.5
        numb_loop = len( Pre_cal_MAn_Anti )
        if len( self.cal_MAn_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = [ Pre_cal_MAn_Anti[i]       for i in range(numb_loop) ]
        Nmod_Anti = [ self.cal_MAn_Anti[i]      for i in range(numb_loop) ]
        return sum( [ Chi2_build( fac331*Ndat_Anti[i] + ( 1 + alpha ) * fac331*In_MAn_BG[i], \
                                  fac331*Nmod_Anti[i] + ( 1 + alpha ) * fac331*In_MAn_BG[i], alpha ).chi    for i in range(numb_loop) ] )
    # All things together: Modes and Particles
    def get_all( self, alpha ):
        chi2_all = self.get_MNu_Nu(alpha) + self.get_MAn_Nu(alpha) + self.get_MHE_Nu(alpha) + self.get_MNu_Anti(alpha) + self.get_MAn_Anti(alpha)
        return chi2_all




if __name__=="__main__":
    show = 1

    if show == 1:
        chi = Chi2_build( 1. + 0.1, 1, 0.2 ).chi
        print(chi)
    
    elif show == 2:
        chi2   = Chi2BC.input_data( Pre_cal_MNu_Nu, Pre_cal_MAn_Nu, Pre_cal_MNu_Anti, Pre_cal_MAn_Anti ).get_MNu_Nu(0)
        chi2_2 = Chi2BC.input_data( [1.1*i for i in Pre_cal_MNu_Nu], [1.1*i for i in Pre_cal_MAn_Nu], [1.1*i for i in Pre_cal_MNu_Anti], [1.1*i for i in Pre_cal_MAn_Anti] ).get_MAn_Nu(0.02)
        print(chi2)
        print(f"alpha = {0.02}, fac={1.1}:\n{chi2_2}")
    
    elif show == 3:
        chi2_all = Chi2BC.input_data( [1.1*i for i in Pre_cal_MNu_Nu], [1.1*i for i in Pre_cal_MAn_Nu], [1.1*i for i in Pre_cal_MNu_Anti], [1.1*i for i in Pre_cal_MAn_Anti] ).get_all(0.02)
        print(f"{chi2_all}")
    
    elif show == 4:
        chi2_all = Chi2BC_331.input_data( [1.1*i for i in Pre_cal_MNu_Nu], [1.1*i for i in Pre_cal_MAn_Nu], [1.1*i for i in Pre_cal_MHE_Nu], \
                                          [1.1*i for i in Pre_cal_MNu_Anti], [1.1*i for i in Pre_cal_MAn_Anti] ).get_all(0.02)
        print(f"{chi2_all}")
    
