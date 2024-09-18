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
from Init_00_tau.histogram  import Histogram
from Init_00_tau.rules_reco import Rule_smear
from SM_01_Prob.mass_order  import Mass_order
from SM_01_Prob.matrix_PMNS import Matrix_Osc
from SM_01_Prob.prob_SM     import Probability_SM
from NSI_02_Prob.prob_NSI   import Probability_NSI


class Prob_ratio_NSI:
    def __init__( self, pick_row, pick_column, sign_cp, energy, distance_L, density, dm2_31, instance_U_PMNS ) -> None:
        self.row     = pick_row
        self.col     = pick_column
        self.sign_cp = sign_cp
        self.en      = energy
        self.dist_L  = distance_L
        self.dens    = density                          # número de eletrons por cm^3
        self.m31     = dm2_31                           # Best-Fit (nu-fit 2024): 2.511*1e-3
        self.inst_U  = instance_U_PMNS
    
    def get_osc( self, delta_mut, phi_mut ):
        mass_bf    = Mass_order.input_data( 7.41*1e-5, 2.511*1e-3 )
        U_bf       = Matrix_Osc.input_data( 0.307, 0.02203, 0.572, (197/180)*np.pi )
        prob_SM_bf = Probability_SM.input_data( self.sign_cp, self.en, self.dist_L, U_bf, mass_bf, self.dens ).get_osc_SM()

        mass_out     = Mass_order.input_data( 7.41*1e-5, self.m31 )
        prob_NSI_out = Probability_NSI.input_data( self.sign_cp, self.en, self.dist_L, self.inst_U, mass_out, self.dens ).get_osc_NSI(delta_mut, phi_mut)
        ratio_NSI    = prob_NSI_out[self.row][self.col]/prob_SM_bf[self.row][self.col]
        return ratio_NSI


class NewEvent_true_NSI:
    def __init__( self, pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true ) -> None:
        self.row    = pick_row
        self.col    = pick_column
        self.sign   = sign_cp
        self.hist   = histogram
        self.dist_L = L
        self.dens   = density
        self.m31    = dm2_31                            # Best-Fit: 2.525*1e-3
        self.inst_U = instance_U_PMNS
        self.old_ev = events_true
    
    def get_event( self, delta_mut, phi_mut ):
        bin_width = (self.hist.bins[0].right - self.hist.bins[0].left)
        bin_left =     [ bin.left                                    for bin in self.hist.bins ]
        bin_midleft =  [ bin.left + bin_width/4                      for bin in self.hist.bins ]
        bin_middle =   [ (bin.left + bin.right)/2                    for bin in self.hist.bins ]
        bin_midright = [ (bin.left + bin.right)/2 + bin_width/4      for bin in self.hist.bins ]
        bin_right =    [ bin.right                                   for bin in self.hist.bins ]
        
        new_ev_true = np.zeros( len(self.old_ev) )
        for i in range( len(self.old_ev) ):
            if bin_middle[i] < 3.25:
                new_ev_true[i] =  self.old_ev[i]
            elif bin_middle[i] == 3.25:
                ratio_35       =  Prob_ratio_NSI( self.row, self.col, self.sign, 3.35 , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                ratio_425      =  Prob_ratio_NSI( self.row, self.col, self.sign, 3.425, self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                ratio_50       =  Prob_ratio_NSI( self.row, self.col, self.sign, 3.50 , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                new_ev_true[i] =  self.old_ev[i] * 1/3 * ( ratio_35 + ratio_425 + ratio_50 )
            else:
                ratio_left     =  Prob_ratio_NSI( self.row, self.col, self.sign, bin_left[i]    , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                ratio_midleft  =  Prob_ratio_NSI( self.row, self.col, self.sign, bin_midleft[i] , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                ratio_mid      =  Prob_ratio_NSI( self.row, self.col, self.sign, bin_middle[i]  , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                ratio_midright =  Prob_ratio_NSI( self.row, self.col, self.sign, bin_midright[i], self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                ratio_right    =  Prob_ratio_NSI( self.row, self.col, self.sign, bin_right[i]   , self.dist_L, self.dens, self.m31, self.inst_U ).get_osc(delta_mut, phi_mut)
                new_ev_true[i] =  self.old_ev[i] * 0.2 * ( ratio_left + ratio_midleft + ratio_mid + ratio_midright + ratio_right )
        return [ round( abs(ev_new_true_i), 4 )   for ev_new_true_i in new_ev_true ]


class NewEvent_reco_NSI:
    def __init__( self, pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true ) -> None:
        self.row = pick_row
        self.col = pick_column
        self.sign = sign_cp
        self.hist = histogram
        self.dist_L = L
        self.dens = density
        self.m31 = dm2_31                            # 2.511*1e-3
        self.inst_U = instance_U_PMNS
        self.old_ev = events_true
    @classmethod
    def input_data( cls, pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true ):
        return cls( pick_row, pick_column, sign_cp, histogram, L, density, dm2_31, instance_U_PMNS, events_true )
    
    def get_event( self, Norm_type, delta_mut, phi_mut ):
        new_ev_true = NewEvent_true_NSI( self.row, self.col, self.sign, self.hist, self.dist_L, self.dens, self.m31, self.inst_U, self.old_ev ).get_event(delta_mut, phi_mut)
        new_ev_reco = Rule_smear.input_data( self.hist, new_ev_true ).get_5to5_pre( Norm_type )
        return [ round( abs(ev_new_reco_i), 4 )   for ev_new_reco_i in new_ev_reco ]




if __name__ == "__main__":
    from Init_00_tau.read_vec import *

    hist = Histogram.get_Uniform_WB(0, 20, 0.5)
    energy = [ (bin.left+bin.right)/2 for bin in hist.bins ]
    L = 1300
    dens = 2.848
    
    show = 3

    if show == 0:
        PMNS = Matrix_Osc.input_data( 0.3, 0.02, 0.49, 1.0*np.pi )
        mass = 2.25*1e-3
        ratio_NSI = np.zeros( (3,3) )
        for i in range(3):
            for j in range(3):
                ratio_NSI[i][j] = Prob_ratio_NSI( i, j, +1, 3.7, 1300, 2.84, mass, PMNS ).get_osc(1*1e-3, 1.25*np.pi)
        print( f"{ratio_NSI}\n" )    
    
    elif show == 1:
        PMNS_BF = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, 1.204225*np.pi )
        mass_BF = 2.525*1e-3
        ratio_NSI = [ Prob_ratio_NSI( 1, 2, -1, en, 1300, 2.84, mass_BF, PMNS_BF ).get_osc(1*1e-3, 1.25*np.pi)  for en in energy ]
        print( f"{ratio_NSI}\n" )

        In_event = In_MAn_true_Anti
        norm_fac = Norm5x5_MAn_Anti
        In_pre   = In_pre_MAn_Anti
        new_event = NewEvent_reco_NSI.input_data( 1, 2, -1, hist, L, dens, mass_BF, PMNS_BF, In_event  ).get_event( norm_fac , 1*1e-3, 1.25*np.pi)
        print( f"{new_event}\n{[vec     for vec in In_pre]}\n\n{sum([ new_event[i] - In_pre[i]   for i in range(len(In_pre)) ])}" )

    elif show == 2:
        matrix_PMNS = Matrix_Osc.input_data( 0.35, 0.041, 0.5, 0.5*np.pi )
        mass =  2.29*1e-3
        ratio_NSI = Prob_ratio_NSI( 1, 2, +1, 3.51, 1300, 2.84, mass, matrix_PMNS ).get_osc(1*1e-3, 1.25*np.pi)
        print( f"{ratio_NSI}\n" )

        In_event = In_MAn_true_Nu
        norm_fac = Norm5x5_MAn_Nu
        In_pre   = In_pre_MAn_Nu
        new_event = NewEvent_reco_NSI.input_data( 1, 2, +1, hist, L, dens, mass, matrix_PMNS, In_event  ).get_event( norm_fac , 1*1e-3, 1.25*np.pi)
        print( f"{new_event}\n{[vec     for vec in In_pre]}\n\n{sum([ new_event[i] - In_pre[i]   for i in range(len(In_pre)) ])}" )
    
    elif show == 3:
        matrix_PMNS = Matrix_Osc.input_data( 0.35, 0.041, 0.5, 0.5*np.pi )
        mass =  2.29*1e-3
        ratio_NSI = [ round(Prob_ratio_NSI( 1, 2, +1, en, 1300, 2.84, mass, matrix_PMNS ).get_osc(1*1e-3, 1.25*np.pi), 2)  for en in energy ]
        print( f"{ratio_NSI}\n" )

        In_event = In_MAn_true_Anti
        new_event = NewEvent_true_NSI( 1, 2, +1, hist, L, dens, mass, matrix_PMNS, In_event  ).get_event(1*1e-3,1.25*np.pi)
        print( f"{[vec for vec in In_event]}\n{new_event}\n\n{sum([ new_event[i] - In_event[i]   for i in range(len(In_event)) ])}" )
        
