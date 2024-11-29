###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				22th May 2024	                  #####
###########################################################

import datetime

# Import our libraries
from Init_00_tau.read_vec                import *
from Init_00_tau.histogram               import Histogram
from SM_01_Prob.matrix_PMNS              import Matrix_Osc
from SM_01_DUNE.py0_new_events_SM        import NewEvent_true_SM
from NSI_03_Near_DUNE.py0_chi2BC_NSI     import Chi2BC_331_Near_NSI
from NSI_03_Near_DUNE.py0_new_events_NSI import NewEvent_Near_true_NSI, NewEvent_Near_reco_NSI


class Tab_Fit_2D:
    def __init__(self, sin2_th12:float, sin2_th13:float, sin2_th23:float, delta_CP:float, dm31:float, phi_mut:float, interval:int ) -> None:
        self.s2_12   = sin2_th12
        self.s2_13   = sin2_th13
        self.s2_23   = sin2_th23
        self.del_CP  = delta_CP
        self.dm31    = dm31
        self.phi_mut = phi_mut
        self.interv  = int( interval )
    @classmethod
    def input_data( cls, sin2_th12:float, sin2_th13:float, sin2_th23:float, delta_CP:float, dm31:float, phi_mut:float, interval:int ):
        return cls( sin2_th12, sin2_th13, sin2_th23, delta_CP, dm31, phi_mut, interval )

    def get_eps_alpha( self, name:str ):                                                                # get: eps_alpha
        L    = 0.574
        dens = 0
        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )
        Umix = Matrix_Osc.input_data(self.s2_12, self.s2_13, self.s2_23, self.del_CP)

        alp_init  = - 0.5
        alp_final = + 0.5

        eps_init  = 0
        eps_final = 2e-4

        New_MNu_true_Nu   = NewEvent_true_SM(row, col, +1, hist, L, dens, self.dm31, Umix, In_MNu_true_Nu  ).get_event()
        New_MAn_true_Nu   = NewEvent_true_SM(row, col, +1, hist, L, dens, self.dm31, Umix, In_MAn_true_Nu  ).get_event()
        New_MHE_true_Nu   = NewEvent_true_SM(row, col, +1, hist, L, dens, self.dm31, Umix, In_MHE_true_Nu  ).get_event()
        New_MNu_true_Anti = NewEvent_true_SM(row, col, -1, hist, L, dens, self.dm31, Umix, In_MNu_true_Anti).get_event()
        New_MAn_true_Anti = NewEvent_true_SM(row, col, -1, hist, L, dens, self.dm31, Umix, In_MAn_true_Anti).get_event()

        # Escolha o diretório onde você quer salvar o arquivo
        dir = '/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/NSI_03_Near_DUNE/my_data_2D/'
        #dir = r'C:\Users\e2356\OneDrive\Documentos\Doutorado\reproducing_events_1904.07265\DUNE_py\NSI_03_Near_DUNE\my_data_2D'
        path_file = os.path.join(dir, str(name))                                                    # Full path of the file with its name

        print('\n',str(name))
        print( "\nStarting in:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M ") )
        with open(path_file, 'w') as save_file:                                                     # Open the file to writing

            for loop_eps in range( self.interv + 1 ):
                eps_i = eps_init + loop_eps*( eps_final - eps_init )/self.interv
                print("\n",loop_eps)

                for loop_alp in range( self.interv + 1 ):
                    alp_i = alp_init + loop_alp*( alp_final - alp_init )/self.interv

                    new_Near_MNu_Nu  = NewEvent_Near_reco_NSI.input_data( 1,2,+1,hist,L,dens,self.dm31,Umix, New_MNu_true_Nu )
                    Near_reco_MNu_Nu = new_Near_MNu_Nu.get_event( Norm5x5_MNu_Nu, eps_i, self.phi_mut )
                    new_Near_MAn_Nu  = NewEvent_Near_reco_NSI.input_data( 1,2,+1,hist,L,dens,self.dm31,Umix, New_MAn_true_Nu )
                    Near_reco_MAn_Nu = new_Near_MAn_Nu.get_event( Norm5x5_MAn_Nu, eps_i, self.phi_mut )
                    new_Near_MHE_Nu  = NewEvent_Near_reco_NSI.input_data( 1,2,+1,hist,L,dens,self.dm31,Umix, New_MHE_true_Nu )
                    Near_reco_MHE_Nu = new_Near_MHE_Nu.get_event( Norm5x5_MHE_Nu, eps_i, self.phi_mut )

                    new_Near_MNu_Anti  = NewEvent_Near_reco_NSI.input_data( 1,2,-1,hist,L,dens,self.dm31,Umix, New_MNu_true_Anti )
                    Near_reco_MNu_Anti = new_Near_MNu_Anti.get_event( Norm5x5_MNu_Anti, eps_i, self.phi_mut )
                    new_Near_MAn_Anti  = NewEvent_Near_reco_NSI.input_data( 1,2,-1,hist,L,dens,self.dm31,Umix, New_MAn_true_Anti )
                    Near_reco_MAn_Anti = new_Near_MAn_Anti.get_event( Norm5x5_MAn_Anti, eps_i, self.phi_mut )

                    chi2_BC = Chi2BC_331_Near_NSI(Near_reco_MNu_Nu, Near_reco_MAn_Nu, Near_reco_MHE_Nu, Near_reco_MNu_Anti, Near_reco_MAn_Anti,1).get_all( alp_i, eps_i )

                    save_file.write("{:.8f}\t{:.8f}\t{:.12f}\n".format(round(eps_i, 7), round(alp_i, 7), round(chi2_BC, 12)))
                
                print( f"{ round( ( (loop_eps+1)/(self.interv+1) )*100, 0 ) } % \t", datetime.datetime.now().strftime("%H:%M") )    
            
        return print( "\nFinish in:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M \n") )




if __name__== "__main__":

    show = 1

    if show == 1:
        Tab_Fit_2D.input_data( 0.307, 0.02195, 0.561, 0.9833*np.pi, 2.534*1e-3, 0*np.pi, 10 ).get_eps_alpha('DUNE_Near9000_NSI_fit2D_WithBG_Eps_alpha')
        Tab_Fit_2D.input_data( 0.307, 0.02195, 0.561, 0.9833*np.pi, 2.534*1e-3, 1*np.pi, 10 ).get_eps_alpha('DUNE_Near9000_NSI_fit2D_WithBG_PiEps_alpha')

    if show == 2:
        Tab_Fit_2D.input_data( 0.307, 0.02195, 0.561, 0.9833*np.pi, 2.534*1e-3, 0*np.pi, 20 ).get_eps_alpha('DUNE_Near9000_NSI_fit2D_WithoutBG_Eps_alpha')
        Tab_Fit_2D.input_data( 0.307, 0.02195, 0.561, 0.9833*np.pi, 2.534*1e-3, 1*np.pi, 20 ).get_eps_alpha('DUNE_Near9000_NSI_fit2D_WithoutBG_PiEps_alpha')

    if show == 3:

        row  = 1
        col  = 2
        L    = 1297
        dens = 2.848
        m_31 = 2.534*1e-3
        hist = Histogram.get_Uniform_WB( 0, 20, 0.5 )
        Umix = Matrix_Osc.input_data( 0.307, 0.02195, 0.561, 0.9833*np.pi )

        New_MNu_true_Nu   = NewEvent_true_SM(row, col, +1, hist, L, dens, m_31, Umix, In_MNu_true_Nu  ).get_event()
        New_MAn_true_Nu   = NewEvent_true_SM(row, col, +1, hist, L, dens, m_31, Umix, In_MAn_true_Nu  ).get_event()
        New_MHE_true_Nu   = NewEvent_true_SM(row, col, +1, hist, L, dens, m_31, Umix, In_MHE_true_Nu  ).get_event()
        New_MNu_true_Anti = NewEvent_true_SM(row, col, -1, hist, L, dens, m_31, Umix, In_MNu_true_Anti).get_event()
        New_MAn_true_Anti = NewEvent_true_SM(row, col, -1, hist, L, dens, m_31, Umix, In_MAn_true_Anti).get_event()


        New_Near_pre_MNu_Nu   = NewEvent_Near_reco_NSI.input_data(row, col, +1, hist, L, dens, m_31, Umix, New_MNu_true_Nu  ).get_event(Norm5x5_MNu_Nu, 0, 0 )
        path_file_dat = os.path.join("/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau", 'New_Near_pre_MNu_Nu.dat')
        np.savetxt(path_file_dat, New_Near_pre_MNu_Nu, fmt='%.5e', delimiter=' ')

        New_Near_pre_MAn_Nu   = NewEvent_Near_reco_NSI.input_data(row, col, +1, hist, L, dens, m_31, Umix, New_MAn_true_Nu  ).get_event(Norm5x5_MAn_Nu, 0, 0  )
        path_file_dat = os.path.join("/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau", 'New_Near_pre_MAn_Nu.dat')
        np.savetxt(path_file_dat, New_Near_pre_MAn_Nu, fmt='%.5e', delimiter=' ')

        New_Near_pre_MHE_Nu   = NewEvent_Near_reco_NSI.input_data(row, col, +1, hist, L, dens, m_31, Umix, New_MHE_true_Nu  ).get_event(Norm5x5_MHE_Nu, 0, 0  )
        path_file_dat = os.path.join("/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau", 'New_Near_pre_MHE_Nu.dat')
        np.savetxt(path_file_dat, New_Near_pre_MHE_Nu, fmt='%.5e', delimiter=' ')

        New_Near_pre_MNu_Anti = NewEvent_Near_reco_NSI.input_data(row, col, -1, hist, L, dens, m_31, Umix, New_MNu_true_Anti).get_event(Norm5x5_MNu_Anti, 0, 0)
        path_file_dat = os.path.join("/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau", 'New_Near_pre_MNu_Anti.dat')
        np.savetxt(path_file_dat, New_Near_pre_MNu_Anti, fmt='%.5e', delimiter=' ')

        New_Near_pre_MAn_Anti = NewEvent_Near_reco_NSI.input_data(row, col, -1, hist, L, dens, m_31, Umix, New_MAn_true_Anti).get_event(Norm5x5_MAn_Anti, 0, 0)
        path_file_dat = os.path.join("/home/edson/Projeto_doutorado/Experimentos/Beam_Tau/DUNE_py/Init_00_tau", 'New_Near_pre_MAn_Anti.dat')
        np.savetxt(path_file_dat, New_Near_pre_MAn_Anti, fmt='%.5e', delimiter=' ')
