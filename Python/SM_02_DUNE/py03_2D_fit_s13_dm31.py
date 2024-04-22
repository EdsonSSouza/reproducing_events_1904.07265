###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				06th Mar 2024	                  #####
###########################################################

import datetime
import numpy as np

# Import our libraries
from py00_chi2_BC import *
from lib_vector_read import *
from py00_SM_new_events_reco import *


class Tab_test:
    def __init__(self, data_Minus_reco, instance_NewEv_Minus_reco, data_Plus_reco, instance_NewEv_Plus_reco ) -> None:
        self.data_Minus_reco = data_Minus_reco
        self.inst_Minus_reco = instance_NewEv_Minus_reco
        self.data_Plus_reco = data_Plus_reco
        self.inst_Plus_reco = instance_NewEv_Plus_reco
    @classmethod
    def input_data( cls, data_Minus_reco, instance_NewEv_Minus_reco, data_Plus_reco, instance_NewEv_Plus_reco ):
        return cls( data_Minus_reco, instance_NewEv_Minus_reco, data_Plus_reco, instance_NewEv_Plus_reco )
    
    def get_s13_dm31( self ):
        Minus_reco = self.inst_Minus_reco
        Plus_reco = self.inst_Plus_reco

        row = Minus_reco.row
        col = Minus_reco.col
        sign = Minus_reco.sign
        hist = Minus_reco.hist
        L = Minus_reco.L
        dens = Minus_reco.dens

        #if Plus_reco.row != row and Plus_reco.col != col and Plus_reco.sign != sign and Plus_reco.hist != hist and Plus_reco.L != L and Plus_reco.dens != dens:
        #    raise Exception( ' Non-compatible data ! ' )
        
        data_Minus_true = Minus_reco.old_ev
        data_Plus_true = Plus_reco.old_ev

        s2_13_init  = 0.0
        s2_13_final = 0.5

        dm31_init  = 0.1
        dm31_final = 0.6

        interval = 4


        # Escolha o diretório onde você quer salvar o arquivo
        dir = '/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/Python/02_SM_DUNE/my_data/'
        
        # Nome do arquivo para salvar
        name_file = "Neut_fit_SM_dcp_s23_Test.dat"

        # Caminho completo do arquivo
        path_file = os.path.join(dir, name_file)

        # Abrir o arquivo para escrita
        with open(path_file, 'w') as save_file:
        
            for i in range( interval+1 ):
                for j in range( interval+1 ):
                    
                    s2_13_i = s2_13_init + i*( s2_13_final - s2_13_init )/interval
                    dm31_j  = dm31_init  + j*( dm31_final  - dm31_init  )/interval
                    
                    Upmns = Matrix_Osc.input_data( 0.310, s2_13_i, 0.582, -0.79444*np.pi )

                    EvNew_Minus_reco = NewEvent_Smearing_SM.input_data( row, col, sign, hist, L, dens, dm31_j*1e-3, Upmns, data_Minus_true ).get_reco()
                    EvNew_Plus_reco  = NewEvent_Smearing_SM.input_data( row, col, sign, hist, L, dens, dm31_j*1e-3, Upmns, data_Plus_true  ).get_reco()
                    chi2_BC = Chi2BC_NuAnti.input_data( self.data_Minus_reco, EvNew_Minus_reco, self.data_Plus_reco, EvNew_Plus_reco ).get_chi2()
                    #chi2_BC = Chi2BC_HighEn.input_data( self.data_Minus_reco, EvNew_Minus_reco ).get_chi2()
                    
                    save_file.write( "{:<12} {:<12} {:<12}\n".format( round(s2_13_i, 7), round(dm31_j*1e-3, 7), round(chi2_BC, 10) ) )
                
                
                print(f"{ round( ( (i+1)*j )/( (interval+1)*(interval) )*100, 0 ) } %")
            
            return print("\nFinish in:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M \n"))
        

class Tab_Fit_2D:
    def __init__(self, sin2_th12, sin2_th13, sin2_th23, delta_cp, interval ) -> None:
        self.s2_12 = sin2_th12
        self.s2_13 = sin2_th13
        self.s2_23 = sin2_th23
        self.del_cp = delta_cp
        self.interv = int( interval )
    @classmethod
    def input_data( cls, sin2_th12, sin2_th13, sin2_th23, delta_cp, interval ):
        return cls( sin2_th12, sin2_th13, sin2_th23, delta_cp, interval )
    
    def get_s13_dm31( self ):
        row  = 1
        col  = 2
        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )
        L    = 1300
        dens = 2.84

        s2_13_init  = 0.0
        s2_13_final = 0.5

        dm31_init  = 1
        dm31_final = 6

        # s2_23_init  = 0.4
        # s2_23_final = 0.65

        dcp_init  = -1
        dcp_final = +1

        # Escolha o diretório onde você quer salvar o arquivo
        dir = '/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/Python/02_SM_DUNE/my_data/'
        # Nome do arquivo para salvar
        name_file = "DUNE_fit_SM_s13_dm31.dat"
        #name_file = "Neut_fit_SM_s13_dm31.dat"
        # Caminho completo do arquivo
        path_file = os.path.join(dir, name_file)

        # Abrir o arquivo para escrita
        print( "\nStarting in:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M \n") )
        with open(path_file, 'w') as save_file:
        
            for i in range( self.interv + 1 ):
                for j in range( self.interv + 1 ):
                    
                    chi2_BC = 1e+10

                    s2_13_i = s2_13_init + i*( s2_13_final - s2_13_init )/self.interv
                    dm31_j  = dm31_init  + j*( dm31_final  - dm31_init  )/self.interv
                    
                    #for free_i in range( 5 + 1 ):
                    for free_j in range( 4 + 1 ):

                        s23_i = self.s2_23 #s2_23_init + free_i*( s2_23_final - s2_23_init )/5
                        dcp_j = dcp_init   + free_j*( dcp_final   - dcp_init   )/4

                        Upmns = Matrix_Osc.input_data( self.s2_12, s2_13_i, s23_i, dcp_j )

                        EvNew_Nu_TauMinus_reco = NewEvent_Smearing_SM.input_data( row, col, +1, hist, L, dens, dm31_j*1e-3, Upmns, In_minus_Nu_true ).get_reco()
                        EvNew_Nu_TauPlus_reco  = NewEvent_Smearing_SM.input_data( row, col, +1, hist, L, dens, dm31_j*1e-3, Upmns, In_plus_Nu_true  ).get_reco()
                        chi2_BC_Nu = Chi2BC_NuAnti.input_data( In_minus_Nu_reco, EvNew_Nu_TauMinus_reco, In_plus_Nu_reco, EvNew_Nu_TauPlus_reco ).get_chi2()

                        EvNew_Anti_TauMinus_reco = NewEvent_Smearing_SM.input_data( row, col, -1, hist, L, dens, dm31_j*1e-3, Upmns, In_minus_AntiNu_true ).get_reco()
                        EvNew_Anti_TauPlus_reco  = NewEvent_Smearing_SM.input_data( row, col, -1, hist, L, dens, dm31_j*1e-3, Upmns, In_plus_AntiNu_true  ).get_reco()
                        chi2_BC_Anti = Chi2BC_NuAnti.input_data( In_minus_AntiNu_reco, EvNew_Anti_TauMinus_reco, In_plus_AntiNu_reco, EvNew_Anti_TauPlus_reco ).get_chi2()

                        EvNew_HE_TauMinus_reco = NewEvent_Smearing_SM.input_data( row, col, +1, hist, L, dens, dm31_j*1e-3, Upmns, In_minus_HE_true ).get_reco()
                        chi2_BC_HE = Chi2BC_HighEn.input_data( In_minus_HE_reco, EvNew_HE_TauMinus_reco ).get_chi2()
                        
                        chi2_test = chi2_BC_Nu + chi2_BC_Anti + chi2_BC_HE
                        if chi2_test < chi2_BC:
                            chi2_BC  = chi2_test

                    save_file.write( "{:<12} {:<12} {:<12}\n".format( round(s2_13_i, 7), round(dm31_j*1e-3, 7), round(chi2_BC, 10) ) )
                
                print(f"{ round( ( (i+1)*j )/( (self.interv+1)*(self.interv) )*100, 0 ) } % \t", datetime.datetime.now().strftime("%H:%M") )
            
        return print( "\nFinish in:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M \n") )
            
          
                
    
if __name__== "__main__":

    show = 2

    if show == 1:
        
        L = 1300
        dens = 2.84
        row = 1
        col = 2

        U_PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, -0.79444*np.pi )
        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )

        new_Minus_reco = NewEvent_Smearing_SM.input_data( row, col, +1, hist, L, dens, 2.525*1e-3, U_PMNS, In_minus_Nu_true )
        new_Plus_reco  = NewEvent_Smearing_SM.input_data( row, col, +1, hist, L, dens, 2.525*1e-3, U_PMNS, In_plus_Nu_true  )
        tab_dcp_s23 = Tab_test.input_data( In_minus_Nu_reco, new_Minus_reco, In_plus_Nu_reco, new_Plus_reco ).get_s13_s23()

        #new_Minus_reco = NewEvent_Smearing_SM.input_data( row, col, -1, hist, L, dens, 2.525*1e-3, U_PMNS, In_minus_AntiNu_true )
        #new_Plus_reco  = NewEvent_Smearing_SM.input_data( row, col, -1, hist, L, dens, 2.525*1e-3, U_PMNS, In_plus_AntiNu_true  )
        #tab_dcp_s23 = Tab_test.input_data( In_minus_AntiNu_reco, new_Minus_reco, In_plus_AntiNu_reco, new_Plus_reco ).get_dcp_s23()

        #new_Minus_reco = NewEvent_Smearing_SM.input_data( row, col, +1, hist, L, dens, 2.525*1e-3, U_PMNS, In_minus_HE_true )
        #tab_dcp_s23 = Tab_test.input_data( In_minus_HE_reco, new_Minus_reco, None, None ).get_dcp_s23()
    
    elif show == 2:
        Tab_Fit_2D.input_data( 0.310, 0.02240, 0.582, -0.79444*np.pi, 10 ).get_s13_dm31()
    
    else:
        a=1

