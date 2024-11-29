###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				18th Fev 2024	                  #####
###########################################################

import matplotlib.pyplot as plt

# Import our libraries
from Init_00_tau.read_vec import *


# OBJ: Neutrino Mode (+1) and Antineutrino Mode (-1)

# Plot only the outline of the bars
class Contour_bar:
    def __init__( self, histogram, signal:np.ndarray ) -> None:
        self.hist = histogram
        self.sign = signal 

    def get_plot( self, select:int, str_color:str, str_label:str ):
        n = len([ numb.left  for numb in self.hist.bins ] ) - 1
        x_contour, y_contour = [], []
            
        x_contour.append( self.hist.bins[0].left ), x_contour.append( self.hist.bins[0].left )                # Adding the vertical line in hist.bins[0].left
        y_contour.append( 0 ), y_contour.append( self.sign[0] )

        for i in range( len(self.sign) ):
            x_contour.extend( [self.hist.bins[i].left, self.hist.bins[i].right] )                             # Adding the coordinates of the top lines of the bars
            y_contour.extend( [self.sign[i], self.sign[i]] )

        x_contour.append( self.hist.bins[n].right ), x_contour.append( self.hist.bins[n].right )              # Adding the vertical line in hist.bins[39].right
        y_contour.append( self.sign[n] ), y_contour.append(0) 

        # Plotting the outer contour of the bar
        if select == 0:    
            if str_label is None:
                if type(str_color) == str:
                    plt.plot(x_contour, y_contour, color=str(str_color), linewidth=2.7, linestyle='dashed' )
                else:
                    plt.plot(x_contour, y_contour, color=str_color     , linewidth=2.7, linestyle='dashed' )
            else:
                if type(str_color) == str:
                    plt.plot(x_contour, y_contour, color=str(str_color), linewidth=2.7, linestyle='dashed', label=str(str_label) )
                else:
                    plt.plot(x_contour, y_contour, color=str_color     , linewidth=2.7, linestyle='dashed', label=str(str_label) )

        elif select == 1:    
            if type(str_color) == str:                                                                            
                plt.plot(x_contour, y_contour, color=str(str_color), linewidth=3, label=str(str_label) )
            else:
                plt.plot(x_contour, y_contour, color=str_color     , linewidth=3, label=str(str_label) )

        else:
            raise Exception(" Select 0 for Best-Fit and 1 for New case! ")


#
##     Graph_all_bar(fill) (Uniform and Joint)
#
class Graph_fill:
    """ Note: This function draws all (fill) the graphs in the article frame, i.e., neutrino mode will have tau_minus, tau_plus and background and so on. """
    _instance = None
    
    def __init__( self, type_mode:int, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray, Calc_reco_Anti:np.ndarray, In_comparison:np.ndarray ):
        self.type_mode = type_mode
        self.hist      = histogram
        self.BG        = In_BG
        self.Calc_Nu   = Calc_reco_Nu
        self.Calc_Anti = Calc_reco_Anti
        self.In_comp   = In_comparison
        #
        Graph_fill._instance = self    
    @classmethod
    def input_data(cls, type_mode:int, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray, Calc_reco_Anti:np.ndarray):
        setup_hist    = cls( type_mode, histogram, In_BG, Calc_reco_Nu, Calc_reco_Anti, None )
        cls._instance = setup_hist 
        return cls._instance
    @classmethod
    def input_change(cls, In_comparison:np.ndarray):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(options) first. ")
        else:
            if len(In_comparison) == len(cls._instance.BG):
                cls._instance.In_comp = In_comparison
                return cls._instance
            else:
                raise Exception(" The number of bins is wrong! ")
    
    def get_plot_bar(self):                                                                     # Getting the plot: Function
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        # Adjust the edges of the frame
        plt.gca().spines['top'   ].set_linewidth(4)                                             # Top edge
        plt.gca().spines['right' ].set_linewidth(4)                                             # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'  ].set_linewidth(4)                                             # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x', direction='in', pad =10, length=15)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad =10, length=15)                            # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=24)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm reco.} \ [GeV]$', fontdict={'size':27})                      # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/3.5 \ yr}$', fontdict={'size':27}, labelpad=8)      # Add label y-axis
        
        #
        ## Neutrino Mode
        #
        if self.type_mode == +1:                                                                           # Write on the frame - Neutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,40)
            plt.xticks([0, 5, 10, 15, 20] )                                                                # Specifying the values that will appear on the x axis
            plt.yticks([0, 10, 20, 30, 40])                                                                # Specifying the values that will appear on the y axis    
            plt.text(14.4, 25.5 if self.In_comp is not None else 28.4, f'Neutrino mode', fontsize=26, color='blue')
        #
        ## Antineutrino Mode
        #
        elif self.type_mode == -1:                                                                         # Write on the frame - AntiNeutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,40/2)
            plt.xticks([0, 5, 10, 15, 20])                                                                 # Specifying the values that will appear on the x axis
            plt.yticks([0, 5, 10, 15, 20])                                                                 # Specifying the values that will appear on the y axis
            plt.text(13.05, 25.5/2 if self.In_comp is not None else 28.4/2, f'Antineutrino mode', fontsize=26, color='blue')
        #
        ## Different Mode
        #
        else:                                                                                              # If it is not a Neutrino or Antineutrino Mode
            raise Exception(" Choose : +1 for Neutrino Mode or -1 for Antineutrino Mode. ")
            
        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.hist.bins ]                              # Defined in the library histogram_unif.py

        #
        ##   Neutrino Mode
        #
        if self.type_mode == +1:                                                                                            # Neutrino Mode:
            Signal_minus, Signal_plus = [], []                                                                                                       
            Signal_plus  = [ self.BG[i]     + self.Calc_Anti[i]     for i in range(len(self.BG)) ]                                  # Sinal_plus : BG + Anti
            Signal_minus = [ Signal_plus[i] + self.Calc_Nu[i]       for i in range(len(self.BG)) ]                                  # Sinal_minus: BG + Anti + Nu
            
            if self.In_comp is not None:
                plt.scatter( build_bins, self.In_comp, color='black', label='Input: data comparison'  )                             # Input : In_comparison

            Contour_bar( self.hist, Signal_minus ).get_plot( 1,'green', \
                                                            r'${\left({\rm BG}\ +\ \tau^{+}\ +\ \tau^{-}\right)\ {\rm events}}$')   # Contour
            plt.bar( build_bins, Signal_minus, width = 0.5, edgecolor='none', facecolor='lightgreen', alpha=0.72                )   # Calc. : Signal_minus

            Contour_bar( self.hist, Signal_plus  ).get_plot( 1, (0.9, 0.5, 0), \
                                                            r'${\left({\rm BG}\ +\ \tau^{+}\right)\ {\rm events}}$' )               # Contour
            plt.bar( build_bins, Signal_plus, width = 0.5, edgecolor='none', facecolor=(1.0, 0.74, 0.5, 0.8)        )               # Calc. : Siganl_plus
            
            light_gray = tuple( origin_gray * 1.1      for origin_gray in (0.5, 0.5, 0.5) )
            Contour_bar( self.hist, self.BG ).get_plot( 1, 'black', 'NC background events'     )                                    # Contour
            plt.bar( build_bins, self.BG, width = 0.5, edgecolor='none', facecolor= light_gray )                                    # Input : In_background  
        #
        ##   Antineutrino Mode
        #
        else:                                                                                                               # AntiNeutrino type:
            Signal_minus, Signal_plus = [], []
            Signal_minus = [ self.BG[i]      + self.Calc_Nu[i]      for i in range(len(self.BG)) ]                                  # Sinal_minus: BG + Nu
            Signal_plus  = [ Signal_minus[i] + self.Calc_Anti[i]    for i in range(len(self.BG)) ]                                  # Sinal_plus : BG + NU + Anti
            
            if self.In_comp is not None:
                plt.scatter( build_bins, self.In_comp, color='black', label='Input: data comparison' )                              # Input : In_comparison
            
            Contour_bar( self.hist, Signal_plus  ).get_plot( 1, (0.9, 0.5, 0), \
                                                            r'${\left({\rm BG}\ +\ \tau^{-}\ +\ \tau^{+}\right)\ {\rm events}}$')   # Contour
            plt.bar( build_bins, Signal_plus, width = 0.5, edgecolor='none', facecolor=(1.0, 0.74, 0.5, 0.8)                    )   # Calc. : Siganl_plus
            
            Contour_bar( self.hist, Signal_minus ).get_plot( 1, 'green', \
                                                            r'${\left({\rm BG}\ +\ \tau^{-}\right)\ {\rm events}}$' )               # Contour
            plt.bar( build_bins, Signal_minus, width = 0.5, edgecolor='none', facecolor='lightgreen', alpha=0.72    )               # Calc. : Signal_minus

            light_gray = tuple( origin_gray * 1.1      for origin_gray in (0.5, 0.5, 0.5) )
            Contour_bar( self.hist, self.BG ).get_plot( 1, 'black', 'NC background events'     )                                    # Contour
            plt.bar( build_bins, self.BG, width = 0.5, edgecolor='none', facecolor=light_gray  )                                    # Input : In_background

        legend = plt.legend( fontsize=24 )                                                                                  # Add legend
        frame = legend.get_frame()
        frame.set_edgecolor('black')

        plt.pause(0.01)                                                                                                     # Displaying the graph and pausing execution
        #plt.savefig('../Image_article/Fig3_Event+BG_MAn.pdf', format='pdf')                                                 # Save with .pdf
        input("Enter to continue: ")                                                                                        # Waiting for keyboard input to continue
        plt.close()                                                                                                         # Close image
        return


class Graph_fill_Cp:
    """ Note: This function draws all (fill) the graphs in the article frame, i.e., neutrino mode will have tau_minus, tau_plus and background and so on. """
    def __init__( self, type_mode:int, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray, Calc_reco_Anti:np.ndarray ):
        self.type_mode = type_mode
        self.hist      = histogram
        self.BG        = In_BG
        self.Calc_Nu   = Calc_reco_Nu
        self.Calc_Anti = Calc_reco_Anti
    @classmethod
    def input_data(cls, type_mode:int, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray, Calc_reco_Anti:np.ndarray):
        return cls( type_mode, histogram, In_BG, Calc_reco_Nu, Calc_reco_Anti ) 
    
    def get_plot_bar(self):                                                                     # Getting the plot: Function
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        # Adjust the edges of the frame
        plt.gca().spines['top'   ].set_linewidth(4)                                             # Top edge
        plt.gca().spines['right' ].set_linewidth(4)                                             # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'  ].set_linewidth(4)                                             # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x', direction='in', pad =10, length=15)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad =10, length=15)                            # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=24)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm reco.} \ [GeV]$', fontdict={'size':27})                      # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/3.5 \ yr}$', fontdict={'size':27}, labelpad=8)      # Add label y-axis
        
        #
        ## Neutrino Mode
        #
        if self.type_mode == +1:                                                                # Write on the frame - Neutrino Mode:
            plt.xlim(0,20)                                                                              # Axis limit
            plt.ylim(0,40)
            plt.xticks([0, 5, 10, 15, 20] )                                                     # Specifying the values that will appear on the x axis
            plt.yticks([0, 10, 20, 30, 40])                                                     # Specifying the values that will appear on the y axis           
            plt.text(14.4, 23, f'Neutrino mode', fontsize=26, color='blue')
        #
        ## Antineutrino Mode
        #
        elif self.type_mode == -1:                                                              # Write on the frame - AntiNeutrino Mode
            plt.xlim(0,20)                                                                              # Axis limit
            plt.ylim(0,30)
            plt.xticks([0, 5, 10, 15, 20])                                                      # Specifying the values that will appear on the x axis
            plt.yticks([0, 5, 10, 15, 20, 25, 30])                                              # Specifying the values that will appear on the y axis
            plt.text(13.05, 17.2, f'Antineutrino mode', fontsize=26, color='blue')
        #
        ## Different Mode
        #
        else:                                                                                   # If it is not a Neutrino or Antineutrino Mode
            raise Exception(" choose : +1 for Neutrino Mode or -1 for Antineutrino Mode. ")
            
        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.hist.bins ]                   # Defined in the library histogram_unif.py

        #
        ##   Neutrino Mode
        #
        if self.type_mode == +1:                                                                                          # Neutrino Mode:
            # New: Comparison
            Signal_minus, Signal_plus = [], []                                                                                                       
            Signal_plus  = [ self.BG[i]     + self.Calc_Anti[i]    for i in range(len(self.BG)) ]                                   # Sinal_plus : BG + Anti
            Signal_minus = [ Signal_plus[i] + self.Calc_Nu[i]      for i in range(len(self.BG)) ]                                   # Sinal_minus: NG + Anti + Nu
            
            Contour_bar( self.hist, Signal_minus ).get_plot( 1, 'green', \
                                                            r'${\left({\rm BG}\ +\ \tau^{+}\ +\ \tau^{-}\right) \ {\rm events}}$')  # Contour
            plt.bar( build_bins, Signal_minus, width = 0.5, edgecolor='none', facecolor='lightgreen', alpha=0.72                 )  # Calc. : Signal_minus

            Contour_bar( self.hist, Signal_plus ).get_plot( 1, (0.9, 0.5, 0), \
                                                           r'${\left({\rm BG}\ +\ \tau^{+}\right) \ {\rm events}}$' )               # Contour
            plt.bar( build_bins, Signal_plus, width = 0.5, edgecolor='none', facecolor=(1.0, 0.74, 0.5, 0.8)        )               # Calc. : Siganl_plus
            
            light_gray = tuple( origin_gray * 1.1      for origin_gray in (0.5, 0.5, 0.5) )
            Contour_bar( self.hist, self.BG ).get_plot( 1, 'black', 'NC background events'     )                                    # Contour
            plt.bar( build_bins, self.BG, width = 0.5, edgecolor='none', facecolor= light_gray )                                    # Input : In_background  

            # Best-Fit: sigma = 0.25453, mu = 0.43522
            Signal_minus, Signal_plus = [], []                                                                                                       
            Signal_plus  = [ self.BG[i]     + In_pre_MNu_Anti[i]   for i in range(len(self.BG)) ]                                   # Sinal_minus (BF): BG + Anti
            Signal_minus = [ Signal_plus[i] + In_pre_MNu_Nu[i]     for i in range(len(self.BG)) ]                                   # Sinal_plus  (BF): BG + Anti + Nu
            Contour_bar( self.hist, Signal_minus ).get_plot(0, 'green', r'${\rm Best-Fit}$' )                                       # Contour: Signal_minus 
            Contour_bar( self.hist, Signal_plus  ).get_plot( 0, (0.9, 0.5, 0), r'${\rm Best-Fit}$' )                                # Contour: Siganl_plus

        #
        ##   Antineutrino Mode
        #
        else:                                                                                                             # AntiNeutrino Mode:
            # New: Comparison
            Signal_minus, Signal_plus = [], []
            Signal_minus = [ self.BG[i]      + self.Calc_Nu[i]      for i in range(len(self.BG)) ]                                  # Sinal_minus: BG + Nu
            Signal_plus  = [ Signal_minus[i] + self.Calc_Anti[i]    for i in range(len(self.BG)) ]                                  # Sinal_plus : BG + Nu + Anti
            
            Contour_bar( self.hist, Signal_plus ).get_plot( 1, (0.9, 0.5, 0), \
                                                           r'${\left({\rm BG}\ +\ \tau^{-}\ +\ \tau^{+}\right) \ {\rm events}}$')   # Contour
            plt.bar( build_bins, Signal_plus, width = 0.5, edgecolor='none', facecolor=(1.0, 0.74, 0.5, 0.8)                    )   # Calc. : Siganl_plus
            
            Contour_bar( self.hist, Signal_minus ).get_plot( 1, 'green', \
                                                            r'${\left({\rm BG}\ +\ \tau^{-}\right) \ {\rm events}}$' )              # Contour
            plt.bar( build_bins, Signal_minus, width = 0.5, edgecolor='none', facecolor='lightgreen', alpha=0.72     )              # Calc. : Signal_minus

            light_gray = tuple( origin_gray * 1.1      for origin_gray in (0.5, 0.5, 0.5) )
            Contour_bar( self.hist, self.BG ).get_plot( 1, 'black', 'NC background events'     )                                    # Contour
            plt.bar( build_bins, self.BG, width = 0.5, edgecolor='none', facecolor=light_gray  )                                    # Input : In_background

            # Best-Fit: sigma = 0.25453, mu = 0.43522
            Signal_minus, Signal_plus = [], []
            Signal_minus = [ self.BG[i]      + In_pre_MAn_Nu[i]       for i in range(len(self.BG)) ]                                # Sinal_minus (BF): BG + Nu
            Signal_plus  = [ Signal_minus[i] + In_pre_MAn_Anti[i]     for i in range(len(self.BG)) ]                                # Sinal_plus  (BF): BG + Nu + Anti
            Contour_bar( self.hist, Signal_plus  ).get_plot( 0, (0.9, 0.5, 0), r'${\rm Best-Fit}$' )                                # Contour: Siganl_plus 
            Contour_bar( self.hist, Signal_minus ).get_plot(0, 'green', r'${\rm Best-Fit}$' )                                       # Contour: Signal_minus

        legend = plt.legend( fontsize=24 )                                                      # Add legend
        frame = legend.get_frame()
        frame.set_edgecolor('black')

        plt.pause(0.01)                                                                         # Displaying the graph and pausing execution

        input("Enter to continue: ")                                                            # Waiting for keyboard input to continue
        plt.close()                                                                             # Close image
        return


#
##     Graph_HE_bar(fill)_UJ 
#
class Graph_fill_HE:
    """ Note: This function draws one type of graph: High energy (HE) mode for tau_minus. """
    _instance = None
    def __init__( self, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray, In_comparison:np.ndarray ):
        self.hist    = histogram
        self.BG      = In_BG
        self.Calc_Nu = Calc_reco_Nu
        self.In_comp = In_comparison
        #
        Graph_fill_HE._instance = self  
    @classmethod
    def input_data(cls, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray):
        setup_hist    = cls( histogram, In_BG, Calc_reco_Nu, None ) 
        cls._instance = setup_hist 
        return cls._instance
    @classmethod
    def input_change(cls, In_comparison:np.ndarray):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(options) first. ")
        else:
            if len(In_comparison) == len(cls._instance.BG):
                cls._instance.In_comp = In_comparison
                return cls._instance
            else:
                raise Exception(" The number of bins is wrong! ")
    
    def get_plot_bar(self):                                                                     # Getting the plot: Function
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        # Adjust the edges of the frame
        plt.gca().spines['top'   ].set_linewidth(4)                                             # Top edge
        plt.gca().spines['right' ].set_linewidth(4)                                             # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'  ].set_linewidth(4)                                             # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x', direction='in', pad =10, length=15)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad =10, length=15)                            # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=24)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm reco.} \ [GeV]$', fontdict={'size':27})                      # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/ yr}$', fontdict={'size':27}, labelpad=8)           # Add label y-axis
        
        # Write on the frame - Neutrino type:
        plt.xlim(0,20)                                                                          # Axis limit
        plt.ylim(0,25)
        plt.xticks([0, 5, 10, 15, 20])                                                          # Specifying the values that will appear on the x axis
        plt.yticks([0, 5, 10, 15, 20, 25])                                                      # Specifying the values that will appear on the y axis
        
        plt.text(13.11, 17.5 if self.In_comp is not None else 19.45, f'High energy mode', fontsize=26, color='blue')
            
        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.hist.bins ]                   # Defined in the library histogram_unif.py

        Signal_minus = []                                                                                                       
        Signal_minus = [ self.BG[i] + self.Calc_Nu[i]    for i in range(len(self.BG)) ]                                      # Sinal_minus: BG + Nu
        
        if self.In_comp is not None:
            plt.scatter( build_bins, self.In_comp, color='black', label='Input: data comparison' )                           # Input : In_comparison

        Contour_bar( self.hist, Signal_minus ).get_plot( 1, 'green', \
                                                        r'${\left({\rm BG}\ +\ \tau^{-}\right) \ {\rm events}}$')            # Contour
        plt.bar( build_bins, Signal_minus, width = 0.5, edgecolor='none', facecolor='lightgreen', alpha=0.72    )            # Calc. : Signal_minus
        
        light_gray = tuple( origin_gray * 1.1      for origin_gray in (0.5, 0.5, 0.5) )
        Contour_bar( self.hist, self.BG ).get_plot( 1, 'black', 'NC background events'     )                                 # Contour
        plt.bar( build_bins, self.BG, width = 0.5, edgecolor='none', facecolor= light_gray )                                 # Input : In_background  

        legend = plt.legend( fontsize=24 )                                                                                   # Add legend
        frame = legend.get_frame()
        frame.set_edgecolor('black')

        plt.pause(0.01)                                                                                                      # Displaying the graph and pausing execution
        #plt.savefig('../Image_article/Fig3_Event+BG_MHE.pdf', format='pdf')                                                  # Save with .pdf
        input("Enter to continue: ")                                                                                         # Waiting for keyboard input to continue
        plt.close()                                                                                                          # Close image
        return


class Graph_fill_Cp_HE:
    """ Note: This function draws one type of graph: High energy (HE) mode for tau_minus. """
    def __init__( self, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray ):
        self.hist    = histogram
        self.BG      = In_BG
        self.Calc_Nu = Calc_reco_Nu
    @classmethod
    def input_data(cls, histogram, In_BG:np.ndarray, Calc_reco_Nu:np.ndarray):
        return cls( histogram, In_BG, Calc_reco_Nu) 
    
    def get_plot_bar(self):                                                                     # Getting the plot: Function
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        # Adjust the edges of the frame
        plt.gca().spines['top'   ].set_linewidth(4)                                             # Top edge
        plt.gca().spines['right' ].set_linewidth(4)                                             # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'  ].set_linewidth(4)                                             # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x', direction='in', pad =10, length=15)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad =10, length=15)                            # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=24)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm reco.} \ [GeV]$', fontdict={'size':27})                      # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/ yr}$', fontdict={'size':27}, labelpad=8)           # Add label y-axis
        
        # Write on the frame - Neutrino type:
        plt.xlim(0,20)                                                                          # Axis limit
        plt.ylim(0,30)
        plt.xticks([0, 5, 10, 15, 20])                                                          # Specifying the values that will appear on the x axis
        plt.yticks([0, 5, 10, 15, 20, 25, 30])                                                  # Specifying the values that will appear on the y axis
        
        plt.text(13.11, 21.1, f'High energy mode', fontsize=26, color='blue')
            
        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.hist.bins ]                   # Defined in the library histogram_unif.py

        # New: Comparison 
        Signal_minus = []                                                                                                       
        Signal_minus = [ self.BG[i] + self.Calc_Nu[i]    for i in range(len(self.BG)) ]                                         # Sinal_minus : BG + Nu

        Contour_bar( self.hist, Signal_minus ).get_plot( 1, 'green', \
                                                        r'${\left({\rm BG}\ +\ \tau^{-}\right) \ {\rm events}}$' )              # Contour
        plt.bar( build_bins, Signal_minus, width = 0.5, edgecolor='none', facecolor='lightgreen', alpha=0.72     )              # Calc. : Signal_minus
        
        light_gray = tuple( origin_gray * 1.1      for origin_gray in (0.5, 0.5, 0.5) )
        Contour_bar( self.hist, self.BG ).get_plot( 1, 'black', 'NC background events'     )                                    # Contour
        plt.bar( build_bins, self.BG, width = 0.5, edgecolor='none', facecolor= light_gray )                                    # Input : In_background  

        # Best-Fit: sigma = 0.25453, mu = 0.43522
        Signal_minus = []                                                                                                       
        Signal_minus = [ self.BG[i] + In_pre_MHE_Nu[i]    for i in range(len(self.BG)) ]                                        # Sinal_minus (BG): BG + Nu
        Contour_bar( self.hist, Signal_minus ).get_plot( 0, 'green', r'${\rm Best-Fit}$')                                       # Contour Signal_minus

        legend = plt.legend( fontsize=24 )                                                                                      # Add legend
        frame = legend.get_frame()
        frame.set_edgecolor('black')

        plt.pause(0.01)                                                                                                         # Displaying the graph and pausing execution

        input("Enter to continue: ")                                                                                            # Waiting for keyboard input to continue
        plt.close()                                                                                                             # Close image
        return




if __name__ == "__main__":
    from Init_00_tau.histogram  import *
    from Init_00_tau.rules_reco import *

    show = 1
    hist = Histogram.get_Uniform_SP(0, 40, 0.5)                                                        # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5
    
    if show == 1:
        # Neutrino Mode (Calculate):                                                                            # Neutrino (Calc.): Reconstruction
        cal_MNu_reco_Nu   = Rule_smear.input_data( hist, In_MNu_true_Nu  ).get_5to5_pre(Norm5x5_MNu_Nu  )             # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( hist, In_MNu_true_Anti).get_5to5_pre(Norm5x5_MNu_Anti)             # Mode_Nu : Events/bin Antineutrino
        #plt_Nu = Graph_fill( +1, hist, In_MNu_BG, cal_MNu_reco_Nu, cal_MNu_reco_Anti, In_Cp_Nu )
        plt_Nu = Graph_fill.input_data( +1, hist, In_MNu_BG, cal_MNu_reco_Nu, cal_MNu_reco_Anti)
        plt_Nu.input_change( In_MNu_Cp )
        plt_Nu.get_plot_bar()
        
        # Antineutrino Mode (Calculate):                                                                        # Antineutrino (Calc.): Reconstruction
        cal_MAn_reco_Nu   = Rule_smear.input_data( hist, In_MAn_true_Nu  ).get_5to5_pre(Norm5x5_MAn_Nu  )             # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( hist, In_MAn_true_Anti).get_5to5_pre(Norm5x5_MAn_Anti)             # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_fill.input_data( -1, hist, In_MAn_BG, cal_MAn_reco_Nu, cal_MAn_reco_Anti)
        plt_Anti.input_change( In_MAn_Cp )
        plt_Anti.get_plot_bar()

        # High Energy Mode (Calculate):                                                                         # High Energy (Calc.): Reconstruction
        cal_MHE_reco_Nu = Rule_smear.input_data( hist, In_MHE_true_Nu ).get_5to5_pre(Norm5x5_MHE_Nu)                  # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_fill_HE.input_data( hist, In_MHE_BG, cal_MHE_reco_Nu)
        plt_HE.input_change( In_MHE_Cp )
        plt_HE.get_plot_bar()    

    if show == 2:
        # Neutrino Mode (Calculate):                                                                            # Neutrino (Calc.): Reconstruction
        cal_MNu_reco_Nu   = Rule_smear.input_data( hist, In_MNu_true_Nu  ).input_change(.2, .3, 1).get_5to5(Norm5x5_MNu_Nu  ) # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( hist, In_MNu_true_Anti).input_change(.2, .3, 1).get_5to5(Norm5x5_MNu_Anti) # Mode_Nu : Events/bin Antineutrino
        #plt_Nu = Graph_fill_Cp( +1, hist, In_MNu_BG, cal_MNu_reco_Nu, cal_MNu_reco_Anti )
        plt_Nu  = Graph_fill_Cp.input_data( +1, hist, In_MNu_BG, cal_MNu_reco_Nu, cal_MNu_reco_Anti)
        plt_Nu.get_plot_bar()

        # Antineutrino Mode (Calculate):                                                                        # Antineutrino (Calc.): Reconstruction
        cal_MAn_reco_Nu   = Rule_smear.input_data( hist, In_MAn_true_Nu  ).input_change(.2, .3, 1).get_5to5(Norm5x5_MAn_Nu  ) # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( hist, In_MAn_true_Anti).input_change(.2, .3, 1).get_5to5(Norm5x5_MAn_Anti) # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_fill_Cp.input_data( -1, hist, In_MAn_BG, cal_MAn_reco_Nu, cal_MAn_reco_Anti)
        plt_Anti.get_plot_bar()

        # High Energy Mode (Calculate):                                                                         # High Energy (Calc.): Reconstruction
        cal_MHE_reco_Nu = Rule_smear.input_data( hist, In_MHE_true_Nu ).input_change(.2, .3, 1).get_5to5(Norm5x5_MHE_Nu)      # Mode_HE : Events/bin Neutrino        
        plt_HE = Graph_fill_Cp_HE.input_data( hist, In_MHE_BG, cal_MHE_reco_Nu)
        plt_HE.get_plot_bar()

    elif show == 3:
        # Neutrino Mode (Calculate):                                                                            # Neutrino (Calc.): Reconstruction
        """ cal_MNu_reco_Nu   = Rule_smear.input_data( hist, In_MNu_true_Nu  ).get_5to5_pre(Norm5x5_MNu_Nu  )             # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( hist, In_MNu_true_Anti).get_5to5_pre(Norm5x5_MNu_Anti)             # Mode_Nu : Events/bin Antineutrino
        #plt_Nu = Graph_fill( +1, hist, In_MNu_BG, cal_MNu_reco_Nu, cal_MNu_reco_Anti, In_Cp_Nu )
        plt_Nu = Graph_fill.input_data( +1, hist, In_MNu_BG, cal_MNu_reco_Nu, cal_MNu_reco_Anti)
        plt_Nu.input_change( In_MNu_Cp )
        plt_Nu.get_plot_bar() """
        #plt.savefig('../Image_article/Fig3_Event+BG_MNu.pdf', format='pdf')
        
        # Antineutrino Mode (Calculate):                                                                        # Antineutrino (Calc.): Reconstruction
        """ cal_MAn_reco_Nu   = Rule_smear.input_data( hist, In_MAn_true_Nu  ).get_5to5_pre(Norm5x5_MAn_Nu  )             # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( hist, In_MAn_true_Anti).get_5to5_pre(Norm5x5_MAn_Anti)             # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_fill.input_data( -1, hist, In_MAn_BG, cal_MAn_reco_Nu, cal_MAn_reco_Anti)
        plt_Anti.input_change( In_MAn_Cp )
        plt_Anti.get_plot_bar() """
        #plt.savefig('../Image_article/Fig3_Event+BG_MAn.pdf', format='pdf')

        # High Energy Mode (Calculate):                                                                         # High Energy (Calc.): Reconstruction
        """ cal_MHE_reco_Nu = Rule_smear.input_data( hist, In_MHE_true_Nu ).get_5to5_pre(Norm5x5_MHE_Nu)                  # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_fill_HE.input_data( hist, In_MHE_BG, cal_MHE_reco_Nu)
        plt_HE.input_change( In_MHE_Cp )
        plt_HE.get_plot_bar() """
        #plt.savefig('../Image_article/Fig3_Event+BG_MHE.pdf', format='pdf') 
    
