###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				12th Mar 2024	                  #####
###########################################################

import numpy as np

# Import our libraries
from Init_00_tau.histogram import Histogram
from Init_00_tau.rules_reco import Rule_smear
from SM_01_Prob.mass_order import Mass_order
from SM_01_Prob.matrix_PMNS import Matrix_Osc
from SM_01_Prob.prob_SM import Probability_SM


class Prob_ratio_SM:
    def __init__( self, pick_row, pick_column, sign_cp, energy, distance_L, density, dm2_31, instance_U_PMNS ) -> None:
        self.row     = pick_row
        self.col     = pick_column
        self.sign_cp = sign_cp
        self.en      = energy
        self.dist_L  = distance_L
        self.dens    = density                          # número de eletrons por cm^3
        self.m31     = dm2_31                            # 2.525*1e-3
        self.inst_U  = instance_U_PMNS
    
    def get_osc( self ):
        mass_bf = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
        U_bf    = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, -0.795775*np.pi )
        prob_SM_bf = Probability_SM.input_data( self.sign_cp, self.en, self.dist_L, U_bf, mass_bf, self.dens ).get_osc_SM()

        mass_out    = Mass_order.input_data( 7.39*1e-5, self.m31 )
        prob_SM_out = Probability_SM.input_data( self.sign_cp, self.en, self.dist_L, self.inst_U, mass_out, self.dens ).get_osc_SM()
        ratio_SM = prob_SM_out[self.row][self.col]/prob_SM_bf[self.row][self.col]
        return ratio_SM


class NewEvents_true_SM:
    def __init__( self, pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true ) -> None:
        self.row = pick_row
        self.col = pick_column
        self.sign = sign_cp
        self.hist = histogram
        self.dist_L = L
        self.dens = density
        self.m31 = dm2_31                            # 2.525*1e-3
        self.inst_U = instance_U_PMNS
        self.old_ev = events_true
    
    def get_event( self ):
        bin_width = (self.hist.bins[0].right - self.hist.bins[0].left)

        bin_left =     [ bin.left                                    for bin in self.hist.bins ]
        bin_midleft =  [ bin.left + bin_width/4                      for bin in self.hist.bins ]
        bin_middle =   [ (bin.left + bin.right)/2                    for bin in self.hist.bins ]
        bin_midright = [ (bin.left + bin.right)/2 + bin_width/4      for bin in self.hist.bins ]
        bin_right =    [ bin.right                                   for bin in self.hist.bins ]
        
        new_ev_true = np.zeros( len(self.old_ev) )
        for i in range( len(self.old_ev) ):
            if bin_middle[i] < 3.25:
                #ratio_mid      =  Prob_ratio_SM( self.row, self.col, self.sign, bin_middle[i], self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                new_ev_true[i] =  self.old_ev[i] #* ratio_mid
            elif bin_middle[i] == 3.25:
                ratio_35       =  Prob_ratio_SM( self.row, self.col, self.sign, 3.35 , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                ratio_425      =  Prob_ratio_SM( self.row, self.col, self.sign, 3.425, self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                ratio_50       =  Prob_ratio_SM( self.row, self.col, self.sign, 3.50 , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                new_ev_true[i] =  self.old_ev[i] * 1/3 * ( ratio_35 + ratio_425 + ratio_50 )
            else:
                ratio_left     =  Prob_ratio_SM( self.row, self.col, self.sign, bin_left[i]    , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                ratio_midleft  =  Prob_ratio_SM( self.row, self.col, self.sign, bin_midleft[i] , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                ratio_mid      =  Prob_ratio_SM( self.row, self.col, self.sign, bin_middle[i]  , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                ratio_midright =  Prob_ratio_SM( self.row, self.col, self.sign, bin_midright[i], self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                ratio_right    =  Prob_ratio_SM( self.row, self.col, self.sign, bin_right[i]   , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc()
                new_ev_true[i] =  self.old_ev[i] * 0.1 * (  1*ratio_left + 2*ratio_midleft + 4*ratio_mid + 2*ratio_midright + 1*ratio_right   )
        return [ round( abs(ev_new_true_i), 4 )   for ev_new_true_i in new_ev_true ]


class NewEvent_Smearing_SM:
    def __init__( self, pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true ) -> None:
        self.row = pick_row
        self.col = pick_column
        self.sign = sign_cp
        self.hist = histogram
        self.dist_L = L
        self.dens = density
        self.m31 = dm2_31                            # 2.525*1e-3
        self.inst_U = instance_U_PMNS
        self.old_ev = events_true
    @classmethod
    def input_data( cls, pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true ):
        return cls( pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true )
    
    def get_reco( self ):
        new_ev_true = NewEvents_true_SM( self.row, self.col, self.sign, self.hist, self.dist_L, self.dens, self.m31, self.inst_U, self.old_ev ).get_event()
        new_ev_reco = Rule_smear( self.hist, new_ev_true ).get_5to5_pre()
        return [ round( abs(ev_new_reco_i), 4 )   for ev_new_reco_i in new_ev_reco ]




if __name__ == "__main__":
    from Init_00_tau.read_vec import *
    from Init_00_tau.migrate import Mapping_matrix

    show = 3

    if show == 1:
        #matrix_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, -0.79444*np.pi )
        matrix_PMNS = Matrix_Osc.input_data( 0.3, 0.021, 0.45, 1.5*np.pi )
        
        ratio_SM = Prob_ratio_SM( 1, 2, +1, 0.01, 1300, 2.84, 2.525*1e-3, matrix_PMNS )
        print( ratio_SM.get_osc() )
    
    elif show == 2 :
        L = 1300
        dens = 2.84
        row = 1
        col = 2
        
        #U_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, -0.79444*np.pi )
        U_PMNS = Matrix_Osc.input_data( 0.3, 0.021, 0.05, -1.0*np.pi )
        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )
        
        new_event = NewEvents_true_SM( row, col, +1, hist, L, dens, 2.525*1e-3, U_PMNS, In_MNu_true_Nu )
        print(f"\n{new_event.get_event()}\n")

    else:
        L = 1300
        dens = 2.84
        row = 1
        col = 2

        U_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, -0.79444*np.pi )
        #U_PMNS = Matrix_Osc.input_data( 0.3, 0.021, 0.05, -1.0*np.pi )
        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )

        new_ev_reco = NewEvent_Smearing_SM.input_data( row, col, +1, hist, L, dens, 2.525*1e-3, U_PMNS, In_MNu_true_Nu ).get_reco()
        print(f"\n{new_ev_reco}\n")

        energy_test = np.linspace( 0.25, 19.75, 40)
        map_matrix = Mapping_matrix.input_data( energy_test)                                                          # Calling the mapping matrix
        map_matrix = map_matrix.get_mapping_mean()

        cal_minus_Nu_reco = 0.5*np.dot( map_matrix, In_MNu_true_Nu )                                                  # Tau_minus :  Events/bin Neutrino ( Reco. ) 
        fator_normal = 1*sum(In_MNu_true_Nu)/sum(cal_minus_Nu_reco)                                                   #
        cal_minus_Nu_reco = [ round( fator_normal*vet , 2 )     for vet in cal_minus_Nu_reco ]  
        print(cal_minus_Nu_reco)
        print(In_MNu_reco_Nu)

