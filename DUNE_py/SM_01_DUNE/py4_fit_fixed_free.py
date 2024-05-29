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

# Import our libraries
from Init_00_tau.read_vec         import *
from Init_00_tau.histogram        import Histogram
from SM_01_Prob.matrix_PMNS       import Matrix_Osc
from SM_01_DUNE.py0_chi2BC_SM     import Chi2BC, Chi2BC_331
from SM_01_DUNE.py0_new_events_SM import NewEvent_reco_SM


class Tab_Fit_4D:
    def __init__(self, sin2_th12, interval ) -> None:
        self.s2_12 = sin2_th12
        self.interv = int( interval )
    @classmethod
    def input_data( cls, sin2_th12, interval ):
        return cls( sin2_th12, interval )
    
    def get_free( self, name ):
        row  = 1
        col  = 2
        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )
        L    = 1300
        dens = 2.84

        dcp_init    = -1
        dcp_final   = +1

        s2_13_init  = 0.0
        s2_13_final = 0.5

        s2_23_init  = 0.05
        s2_23_final = 0.95

        dm31_init   = 1
        dm31_final  = 6

        # Escolha o diretório onde você quer salvar o arquivo
        dir = '/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/SM_01_DUNE/my_data/'
        
        # Nome do arquivo para salvar
        name_file = str(name)
        
        # Caminho completo do arquivo
        path_file = os.path.join(dir, name_file)

        print( "\nStarting in:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M ") )
        # Abrir o arquivo para escrita
        with open(path_file, 'w') as save_file:
        
            for loop_cp in range( self.interv + 1 ):
                dcp_i = dcp_init + loop_cp*( dcp_final - dcp_init )/self.interv
                print("\n",loop_cp)

                for loop_s13 in range( self.interv + 1 ):
                    s13_i = s2_13_init + loop_s13*( s2_13_final - s2_13_init )/self.interv
                    
                    for loop_s23 in range( self.interv + 1 ):
                        s23_i = s2_23_init + loop_s23*( s2_23_final - s2_23_init )/self.interv

                        for loop_m31 in range( self.interv + 1 ):
                            dm31_i  = dm31_init + loop_m31*( dm31_final - dm31_init )/self.interv
                            
                            Upmns = Matrix_Osc.input_data( self.s2_12, s13_i, s23_i, dcp_i )

                            EvNew_Nu_TauMinus_reco = NewEvent_reco_SM.input_data( row, col, +1, hist, L, dens, dm31_i*1e-3, Upmns, In_MNu_true_Nu  ).get_event()
                            EvNew_Nu_TauPlus_reco  = NewEvent_reco_SM.input_data( row, col, +1, hist, L, dens, dm31_i*1e-3, Upmns, In_MNu_true_Anti).get_event()
                            chi2_BC_Nu = Chi2BC.input_data( In_MNu_reco_Nu, EvNew_Nu_TauMinus_reco, In_MNu_reco_Anti, EvNew_Nu_TauPlus_reco ).get_all( 1 )

                            EvNew_Anti_TauMinus_reco = NewEvent_reco_SM.input_data( row, col, -1, hist, L, dens, dm31_i*1e-3, Upmns, In_MAn_true_Nu  ).get_event()
                            EvNew_Anti_TauPlus_reco  = NewEvent_reco_SM.input_data( row, col, -1, hist, L, dens, dm31_i*1e-3, Upmns, In_MAn_true_Anti).get_event()
                            chi2_BC_Anti = Chi2BC.input_data( In_MAn_reco_Nu, EvNew_Anti_TauMinus_reco, In_MAn_reco_Anti, EvNew_Anti_TauPlus_reco ).get_all( 1 )

                            EvNew_HE_TauMinus_reco = NewEvent_reco_SM.input_data( row, col, +1, hist, L, dens, dm31_i*1e-3, Upmns, In_MHE_true_Nu ).get_event()
                            chi2_BC_HE = Chi2BC_331.input_data( In_MHE_reco_Nu, EvNew_HE_TauMinus_reco, In_MHE_reco_Nu, EvNew_HE_TauMinus_reco, EvNew_HE_TauMinus_reco ).get_all( 1 )
                            
                            chi2_BC = chi2_BC_Nu + chi2_BC_Anti + chi2_BC_HE
                            
                            save_file.write( "{:<10} {:<10} {:<10} {:<10} {:<12}\n".format( round(dcp_i, 4), round(s13_i, 4), round(s23_i, 4), round(dm31_i*1e-3, 4), round(chi2_BC, 12) ) )
                
                    print(f"{ round( ( (loop_s13+1)/(self.interv+1) )*100, 0 ) } % \t", datetime.datetime.now().strftime("%H:%M") )
                
            
        return print( "\nFinish in:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M \n") )
            
          
                
    
if __name__== "__main__":

    show = 1

    if show == 1:
        Tab_Fit_4D.input_data( 0.310, 10 ).get_free( "DUNE_fit_SM_4Dfree.dat" )
    
    else:
        a=1

