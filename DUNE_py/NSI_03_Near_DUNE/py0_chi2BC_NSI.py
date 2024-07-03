###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				06th Mar 2024	                  #####
###########################################################

""" 
Description about this script:
    This script create the function chi2_BC ( Baker and Cousins ) in the Near Detector.
"""

import numpy as np

# Import our library
from Init_00_tau.read_vec import *


class Chi2_build:                                                                                      # Chi^2_i: i_th element of the chi^2_BC ( Baker and Cousins )
    def __init__(self, data, model) -> None:
        self.dat = data                                                # Selected data_ith (best fit) from the article: In_Near_pre_calculated
        self.mod = model                                               # Theoretical data_ith for probability rations

        if self.dat == 0:
            self.chi = 2*( self.mod - self.dat )
        elif self.dat != 0 and self.mod != 0:
            self.chi = 2*( self.mod - self.dat + self.dat * np.log( self.dat/self.mod ) )      
        else:
            self.mod = 5e-11
            self.chi = 2*( self.mod - self.dat + self.dat * np.log( self.dat/self.mod ) )


class Chi2BC_Near_NSI:                                                                                 # For 3.5 + 3.5 years: Mode_Nu and Mode_An 
    """ For 3.5 + 3.5 years: Mode_Neutrino and Mode_Antineutrino

        class Chi2BC_Near_NSI has 5 different chi2_BC:
            
            get_MNu_Nu; get_MAn_Nu;
            
            get_MNu_Anti; get_MAn_Anti;
            
            get_all = sum( get_MNu_Nu, get_MAn_Nu, get_MNu_Anti, get_MAn_Anti )
    """
    def __init__( self, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti, BG_On_or_Off=1 ) -> None:
        self.cal_MNu_Nu   = Calc_MNu_reco_Nu                           # MNu_Nu
        self.cal_MAn_Nu   = Calc_MAn_reco_Nu                           # MAn_Nu
        self.cal_MNu_Anti = Calc_MNu_reco_Anti                         # MNu_Anti
        self.cal_MAn_Anti = Calc_MAn_reco_Anti                         # MAn_Anti
        # If there is BG select 1 (On) or 0 (Off) if there is not
        if BG_On_or_Off == 1 or BG_On_or_Off == 0:                   
            self.BG = 2957.5*BG_On_or_Off                              # Factor Near detector: 70/40000 * (1300/1)^2 = 2957.5
        else:
            Exception( " If there is BG select 1 (On) or 0 (Off) if there is not ! " )
    @classmethod
    def input_data( cls, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti, BG_On_or_Off=1 ):
        return cls( Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti, BG_On_or_Off )

    def get_MNu_Nu( self, alpha, delta_mut ):                                                          # get_MNu_Nu
        """ Neutrino Mode: Neutrino """
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MNu_Nu )
        if len( self.cal_MNu_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )        
        Ndat_Nu = In_Near_pre_MNu_Nu    
        Nmod_Nu = self.cal_MNu_Nu
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(Ndat_Nu[i] + self.BG*In_MNu_BG[i], Nmod_Nu[i] + (1+alpha)*fac_NSI*In_MNu_BG[i]).chi for i in range(numb_loop) ]) + err_sys
    
    def get_MAn_Nu( self, alpha, delta_mut ):                                                          # get_MAn_Nu
        """ Antineutrino Mode: Neutrino """
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MAn_Nu )
        if len( self.cal_MAn_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Nu = In_Near_pre_MAn_Nu    
        Nmod_Nu = self.cal_MAn_Nu
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(Ndat_Nu[i] + self.BG*In_MAn_BG[i], Nmod_Nu[i] + (1+alpha)*fac_NSI*In_MAn_BG[i]).chi for i in range(numb_loop) ]) + err_sys  
    
    def get_MNu_Anti( self, alpha, delta_mut ):                                                        # get_MNu_Anti
        """ Neutrino Mode: Antineutrino """
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MNu_Anti )
        if len( self.cal_MNu_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = In_Near_pre_MNu_Anti
        Nmod_Anti = self.cal_MNu_Anti
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(Ndat_Anti[i] + self.BG*In_MNu_BG[i], Nmod_Anti[i] + (1+alpha)*fac_NSI*In_MNu_BG[i]).chi for i in range(numb_loop) ]) + err_sys  
    
    def get_MAn_Anti( self, alpha, delta_mut ):                                                        # get_MAn_Anti
        """ Antineutrino Mode: Antineutrino """
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MAn_Anti )
        if len( self.cal_MAn_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = In_Near_pre_MAn_Anti
        Nmod_Anti = self.cal_MAn_Anti
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(Ndat_Anti[i] + self.BG*In_MAn_BG[i], Nmod_Anti[i] + (1+alpha)*fac_NSI*In_MAn_BG[i]).chi for i in range(numb_loop) ]) + err_sys
    
    def get_all( self, alpha, delta_mut ):                                                             # get_all: Modes and Particles
        """ All things together: Modes and Particles """
        return self.get_MNu_Nu(alpha, delta_mut) + self.get_MAn_Nu(alpha, delta_mut) + self.get_MNu_Anti(alpha, delta_mut) + self.get_MAn_Anti(alpha, delta_mut)


class Chi2BC_331_Near_NSI:                                                                             # For 3 + 3 + 1 years: Mode_Nu and Mode_An
    """ For 3 + 3 + 1 years: Mode_Neutrino and Mode_Antineutrino

        class Chi2BC_331_Near_NSI has 6 different chi2_BC:
            
            get_MNu_Nu; get_MAn_Nu; get_MHE_Nu;
            
            get_MNu_Anti; get_MAn_Anti;
            
            get_all = sum( get_MNu_Nu, get_MAn_Nu, get_MHE_Nu, get_MNu_Anti, get_MAn_Anti )
    """
    def __init__( self, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MHE_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti, BG_On_or_Off=1 ) -> None:
        self.cal_MNu_Nu   = Calc_MNu_reco_Nu                           # MNu_Nu
        self.cal_MAn_Nu   = Calc_MAn_reco_Nu                           # MAn_Nu
        self.cal_MHE_Nu   = Calc_MHE_reco_Nu                           # MHE_Nu
        self.cal_MNu_Anti = Calc_MNu_reco_Anti                         # MNu_Anti
        self.cal_MAn_Anti = Calc_MAn_reco_Anti                         # MAn_Anti
        # If there is BG select 1 (On) or 0 (Off) if there is not
        if BG_On_or_Off == 1 or BG_On_or_Off == 0:
            self.BG = 2957.5*BG_On_or_Off                              # Factor Near detector: 70/40000 * (1300/1)^2 = 2957.5
        else:
            Exception( " If there is BG select 1 (On) or 0 (Off) if there is not ! " )
    @classmethod
    def input_data( cls, Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MHE_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti, BG_On_or_Off=1 ):
        return cls( Calc_MNu_reco_Nu, Calc_MAn_reco_Nu, Calc_MHE_reco_Nu, Calc_MNu_reco_Anti, Calc_MAn_reco_Anti, BG_On_or_Off )

    def get_MNu_Nu( self, alpha, delta_mut ):                                                          # get_MNu_Nu
        """ Neutrino Mode: Neutrino """
        fac331    = 0.857142857                                                                        # factor_year: 3(yr)/3.5(yr)
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MNu_Nu )
        if len( self.cal_MNu_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )        
        Ndat_Nu = In_Near_pre_MNu_Nu    
        Nmod_Nu = self.cal_MNu_Nu
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(fac331*(Ndat_Nu[i] + self.BG*In_MNu_BG[i]          ), \
                                fac331*(Nmod_Nu[i] + (1+alpha)*fac_NSI*In_MNu_BG[i])).chi  for i in range(numb_loop) ]) + err_sys

    def get_MAn_Nu( self, alpha, delta_mut ):                                                          # get_MAn_Nu
        """ Antineutrino Mode: Neutrino """
        fac331    = 0.857142857                                                                        # factor_year: 3(yr)/3.5(yr)
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MAn_Nu )
        if len( self.cal_MAn_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Nu = In_Near_pre_MAn_Nu    
        Nmod_Nu = self.cal_MAn_Nu
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(fac331*(Ndat_Nu[i] + self.BG*In_MAn_BG[i]          ), \
                                fac331*(Nmod_Nu[i] + (1+alpha)*fac_NSI*In_MAn_BG[i])).chi   for i in range(numb_loop) ]) + err_sys

    def get_MHE_Nu( self, alpha, delta_mut ):                                                          # get_MHE_Nu
        """ High Energy Mode: Neutrino """
        fac331    = 1                                                                                  # factor_year: 1(yr)
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MHE_Nu )
        if len( self.cal_MHE_Nu ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Nu = In_Near_pre_MHE_Nu    
        Nmod_Nu = self.cal_MHE_Nu
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(fac331*(Ndat_Nu[i] + self.BG*In_MHE_BG[i]          ), \
                                fac331*(Nmod_Nu[i] + (1+alpha)*fac_NSI*In_MHE_BG[i])).chi   for i in range(numb_loop) ]) + err_sys

    def get_MNu_Anti( self, alpha, delta_mut ):                                                        # get_MNu_Anti
        """ Neutrino Mode: Antineutrino """
        fac331    = 0.857142857                                                                        # factor_year: 3(yr)/3.5(yr)
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MNu_Anti )
        if len( self.cal_MNu_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = In_Near_pre_MNu_Anti
        Nmod_Anti = self.cal_MNu_Anti
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(fac331*(Ndat_Anti[i] + self.BG*In_MNu_BG[i]          ), \
                                fac331*(Nmod_Anti[i] + (1+alpha)*fac_NSI*In_MNu_BG[i])).chi for i in range(numb_loop) ]) + err_sys

    def get_MAn_Anti( self, alpha, delta_mut ):                                                        # get_MAn_Anti
        """ Antineutrino Mode: Antineutrino """
        fac331    = 0.857142857                                                                        # factor_year: 3(yr)/3.5(yr)
        err_sys   = (4*alpha)**2                                                                       # Systematic error (25%): alpha/0.25 = 4*alpha
        numb_loop = len( In_Near_pre_MAn_Anti )
        if len( self.cal_MAn_Anti ) != numb_loop:
            raise Exception( " Number different from the data entered ! " )
        Ndat_Anti = In_Near_pre_MAn_Anti
        Nmod_Anti = self.cal_MAn_Anti
        eps_mut = 27 * delta_mut
        fac_NSI = self.BG*(1 + eps_mut**2 )
        return sum([ Chi2_build(fac331*(Ndat_Anti[i] + self.BG*In_MAn_BG[i]          ), \
                                fac331*(Nmod_Anti[i] + (1+alpha)*fac_NSI*In_MAn_BG[i])).chi for i in range(numb_loop) ]) + err_sys

    def get_all( self, alpha, delta_mut ):                                                             # get_all: Modes and Particles
        """ All things together: Modes and Particles """
        return self.get_MNu_Nu( alpha, delta_mut ) + self.get_MAn_Nu( alpha, delta_mut ) + self.get_MHE_Nu(alpha, delta_mut) +\
               0*self.get_MNu_Anti(alpha, delta_mut) + 0*self.get_MAn_Anti(alpha, delta_mut)




if __name__=="__main__":
    show = 1

    if show == 1:
        chi = Chi2_build( 1. + 100*0.1, 1 ).chi
        print(chi)
    
    elif show == 2:
        chi2_MNu_Nu = Chi2BC_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti ).get_MNu_Nu(0.0, 1*1e-3)
        chi2_all    = Chi2BC_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti ).get_all(0.0, 1*1e-3)
        print(chi2_MNu_Nu)
        print(chi2_all)
        
    elif show == 3:
        chi2_MNu_Nu = Chi2BC_Near_NSI.input_data( [.1*i for i in In_Near_pre_MNu_Nu], In_Near_pre_MAn_Nu, In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti   ).get_MNu_Nu(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MNu_Nu}")
        
        chi2_MAn_Nu = Chi2BC_Near_NSI.input_data( In_Near_pre_MNu_Nu, [.1*i for i in In_Near_pre_MAn_Nu], In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti   ).get_MAn_Nu(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MAn_Nu}")
        
        chi2_MNu_Anti = Chi2BC_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, [.1*i for i in In_Near_pre_MNu_Anti], In_Near_pre_MAn_Anti ).get_MNu_Anti(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MNu_Anti}")
        
        chi2_MAn_Anti = Chi2BC_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, In_Near_pre_MNu_Anti, [.1*i for i in In_Near_pre_MAn_Anti] ).get_MAn_Anti(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MAn_Anti}")
        
        print( chi2_MNu_Nu + chi2_MAn_Nu + chi2_MNu_Anti + chi2_MAn_Anti )
        chi2_all = Chi2BC_Near_NSI.input_data( [.1*i for i in In_Near_pre_MNu_Nu], [.1*i for i in In_Near_pre_MAn_Nu], [.1*i for i in In_Near_pre_MNu_Anti], \
                                          [.1*i for i in In_Near_pre_MAn_Anti] ).get_all(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_all}")

    elif show == 4:
        chi2_MNu_Nu = Chi2BC_331_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, In_Near_pre_MHE_Nu, In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti ).get_MNu_Nu(0.0, 1*1e-3)
        chi2_all    = Chi2BC_331_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, In_Near_pre_MHE_Nu, In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti ).get_all(0.0, 1*1e-3)
        print(chi2_MNu_Nu)
        print(chi2_all)
    
    elif show == 5:
        chi2_MNu_Nu = Chi2BC_331_Near_NSI.input_data( [.1*i for i in In_Near_pre_MNu_Nu], In_Near_pre_MAn_Nu, \
                                                       In_Near_pre_MHE_Nu, In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti   ).get_MNu_Nu(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MNu_Nu}")
        
        chi2_MAn_Nu = Chi2BC_331_Near_NSI.input_data( In_Near_pre_MNu_Nu, [.1*i for i in In_Near_pre_MAn_Nu], \
                                                      In_Near_pre_MHE_Nu, In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti   ).get_MAn_Nu(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MAn_Nu}")
        
        chi2_MHE_Nu = Chi2BC_331_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, [.1*i for i in In_Near_pre_MHE_Nu], \
                                                      In_Near_pre_MNu_Anti, In_Near_pre_MAn_Anti   ).get_MHE_Nu(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MHE_Nu}")

        chi2_MNu_Anti = Chi2BC_331_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, In_Near_pre_MHE_Nu, \
                                                        [.1*i for i in In_Near_pre_MNu_Anti], In_Near_pre_MAn_Anti ).get_MNu_Anti(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MNu_Anti}")
        
        chi2_MAn_Anti = Chi2BC_331_Near_NSI.input_data( In_Near_pre_MNu_Nu, In_Near_pre_MAn_Nu, In_Near_pre_MHE_Nu, \
                                                        In_Near_pre_MNu_Anti, [.1*i for i in In_Near_pre_MAn_Anti] ).get_MAn_Anti(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_MAn_Anti}")
        
        print( chi2_MNu_Nu + chi2_MAn_Nu + chi2_MHE_Nu + chi2_MNu_Anti + chi2_MAn_Anti )
        chi2_all = Chi2BC_331_Near_NSI.input_data( [.1*i for i in In_Near_pre_MNu_Nu], [.1*i for i in In_Near_pre_MAn_Nu], [.1*i for i in In_Near_pre_MHE_Nu], \
                                              [.1*i for i in In_Near_pre_MNu_Anti], [.1*i for i in In_Near_pre_MAn_Anti] ).get_all(0.1, 1*1e-3)
        print(f"alpha = {0.1}, fac={0.1}:\t{chi2_all}")

