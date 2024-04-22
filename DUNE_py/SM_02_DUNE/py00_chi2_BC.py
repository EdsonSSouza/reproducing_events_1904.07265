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


#   Neutrino and Antineutrino Mode: For 3.5 + 3.5 years
class Chi2BC_NuAnti:
    def __init__( self, data_minus, model_minus, data_plus, model_plus ) -> None:
        self.dat_neg = data_minus
        self.mod_neg = model_minus
        self.dat_pos = data_plus
        self.mod_pos = model_plus
    @classmethod
    def input_data( cls, data_minus, model_minus, data_plus, model_plus ):
        return cls( data_minus, model_minus, data_plus, model_plus )
    
    def get_chi2( self ):
        numb_loop = len(self.dat_neg)

        if len(self.dat_pos) != numb_loop and len(self.mod_neg) != numb_loop and len(self.mod_pos) != numb_loop:
            raise Exception( " Numbers different from the data entered ! " )

        Ndat_neg = self.dat_neg
        Nmod_neg = self.mod_neg
        Ndat_pos = self.dat_pos
        Nmod_pos = self.mod_pos

        chi2_i = np.zeros( numb_loop )

        for i in range( numb_loop ):
            if Ndat_neg[i] != 0 and Nmod_neg[i] != 0:
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] + Ndat_neg[i]*np.log(Ndat_neg[i]/Nmod_neg[i]) )
                #
                if Ndat_pos[i] != 0 and Nmod_pos[i] != 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                #
                elif Ndat_pos[i] == 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] )
                #
                else:
                    Nmod_pos[i] = 0.00005
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                            
            elif Ndat_neg[i] == 0:
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] )
                #
                if Ndat_pos[i] != 0 and Nmod_pos[i] != 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                #
                elif Ndat_pos[i] == 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] )
                #
                else:
                    Nmod_pos[i] = 0.00005
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
            
            else:
                Nmod_neg[i] = 0.00005
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] + Ndat_neg[i]*np.log(Ndat_neg[i]/Nmod_neg[i]) )
                #
                if Ndat_pos[i] != 0 and Nmod_pos[i] != 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                #
                elif Ndat_pos[i] == 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] )
                #
                else:
                    Nmod_pos[i] = 0.00005
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
        
        chi2_BC = sum(chi2_i)

        return chi2_BC



#   Neutrino and Antineutrino Mode: For 3 + 3 + 1 years
class Chi2BC_NuAnti_331:
    def __init__( self, data_minus, model_minus, data_plus, model_plus ) -> None:
        self.dat_neg = data_minus
        self.mod_neg = model_minus
        self.dat_pos = data_plus
        self.mod_pos = model_plus
    @classmethod
    def input_data( cls, data_minus, model_minus, data_plus, model_plus ):
        return cls( data_minus, model_minus, data_plus, model_plus )
    
    def get_chi2( self ):
        numb_loop = len(self.dat_neg)

        if len(self.dat_pos) != numb_loop and len(self.mod_neg) != numb_loop and len(self.mod_pos) != numb_loop:
            raise Exception( " Numbers different from the data entered ! " )

        Ndat_neg = self.dat_neg
        Nmod_neg = self.mod_neg
        Ndat_pos = self.dat_pos
        Nmod_pos = self.mod_pos

        chi2_i = np.zeros( numb_loop )

        for i in range( numb_loop ):
            if Ndat_neg[i] != 0 and Nmod_neg[i] != 0:
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] + Ndat_neg[i]*np.log(Ndat_neg[i]/Nmod_neg[i]) )
                #
                if Ndat_pos[i] != 0 and Nmod_pos[i] != 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                #
                elif Ndat_pos[i] == 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] )
                #
                else:
                    Nmod_pos[i] = 0.00005
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                            
            elif Ndat_neg[i] == 0:
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] )
                #
                if Ndat_pos[i] != 0 and Nmod_pos[i] != 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                #
                elif Ndat_pos[i] == 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] )
                #
                else:
                    Nmod_pos[i] = 0.00005
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
            
            else:
                Nmod_neg[i] = 0.00005
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] + Ndat_neg[i]*np.log(Ndat_neg[i]/Nmod_neg[i]) )
                #
                if Ndat_pos[i] != 0 and Nmod_pos[i] != 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
                #
                elif Ndat_pos[i] == 0:
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] )
                #
                else:
                    Nmod_pos[i] = 0.00005
                    chi2_i[i] += 2*( Nmod_pos[i] - Ndat_pos[i] + Ndat_pos[i]*np.log(Ndat_pos[i]/Nmod_pos[i]) )
        
        chi2_BC_331 = 0.857142857*sum(chi2_i)   # 3/3.5 = 0.857142857

        return chi2_BC_331


#   High Energy Mode (neutrino): For 3 + 3 + 1 years
class Chi2BC_HighEn_331:
    def __init__( self, data_minus, model_minus ) -> None:
        self.dat_neg = data_minus
        self.mod_neg = model_minus
    @classmethod
    def input_data( cls, data_minus, model_minus ):
        return cls( data_minus, model_minus )
    
    def get_chi2( self ):
        numb_loop = len(self.dat_neg)

        if len(self.mod_neg) != numb_loop:
            raise Exception( " Numbers different from the data entered ! " )

        Ndat_neg = self.dat_neg
        Nmod_neg = self.mod_neg

        chi2_i = np.zeros( numb_loop )

        for i in range( numb_loop ):
            if Ndat_neg[i] != 0 and Nmod_neg[i] != 0:
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] + Ndat_neg[i]*np.log(Ndat_neg[i]/Nmod_neg[i]) )
                            
            elif Ndat_neg[i] == 0:
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] )
            
            else:
                Nmod_neg[i] = 0.00005
                chi2_i[i] = 2*( Nmod_neg[i] - Ndat_neg[i] + Ndat_neg[i]*np.log(Ndat_neg[i]/Nmod_neg[i]) )

        chi2_BC_331 = sum(chi2_i)

        return chi2_BC_331




if __name__=="__main__":
    event_Minus_data  = [ 1.1, 3.05, 6.2, 1.02, 1.2, 0.1, 0.00 , 0.1 ]
    event_Minus_model = [ 1.0, 3.00, 6.0, 1.00, 1.0, 0.1, 0.00 , 0.0 ]
    event_Plus_data   = [ 1.1, 3.05, 6.2, 1.02, 1.2, 2.0, 0.00 , 0.1 ]
    event_Plus_model  = [ 1.0, 3.00, 6.0, 1.00, 1.0, 2.1, 0.00 , 0.0 ]

    chi2_BC_1 = Chi2BC_NuAnti.input_data( event_Minus_data, event_Minus_model, event_Plus_data, event_Plus_model ).get_chi2()
    chi2_BC_2 = Chi2BC_HighEn_331.input_data( event_Minus_data, event_Minus_model ).get_chi2()
    print(f"{chi2_BC_1} \t {chi2_BC_2}")

