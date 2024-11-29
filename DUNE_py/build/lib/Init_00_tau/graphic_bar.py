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
import matplotlib.pyplot as plt

# Import our libraries
from Init_00_tau.read_vec import *


# OBJ: Neutrino Mode (+1) and Antineutrino Mode (-1)

# Plot only the outline of the bars 
class Contour_bar:
    def __init__( self, histogram, signal:np.ndarray ) -> None:
        self.hist  = histogram
        self.sign  = signal 

    def get_plot( self, fac_alpha:float, str_color:str, str_style:str, width:float, str_label:str ):
        n = len([ numb.left  for numb in self.hist.bins ] ) - 1
        x_contour, y_contour = [], []
            
        x_contour.append( self.hist.bins[0].left ), x_contour.append( self.hist.bins[0].left )                # Adding the vertical line in hist.bins[0].left
        y_contour.append( 0 ), y_contour.append( self.sign[0] )

        for i in range( len(self.sign) ):
            x_contour.extend( [self.hist.bins[i].left, self.hist.bins[i].right] )                             # Adding the coordinates of the top lines of the bars
            y_contour.extend( [self.sign[i], self.sign[i]] )

        x_contour.append( self.hist.bins[n].right ), x_contour.append( self.hist.bins[n].right )              # Adding the vertical line in hist.bins[39].right
        y_contour.append( self.sign[n] ), y_contour.append(0) 

        if type(str_color) == str:                                                                            # Plotting the outer contour of the members
            plt.plot(x_contour, y_contour, color=str(str_color), linestyle=str(str_style), linewidth=width, label=str(str_label), alpha=fac_alpha )
        else:
            buil_color = [ icolor   for icolor in str_color ]
            buil_color.append(fac_alpha) 
            color_real = tuple( buil_color )
            plt.plot(x_contour, y_contour, color=color_real    , linestyle=str(str_style), linewidth=width, label=str(str_label) )


#
##     Graph_all_bar (Uniform and Joint)
#
class Graph_all:
    """ 
    Note: 
    
        This function draws all (all) the graphs in the article frame, i.e., neutrino mode will have tau_minus and tau_plus and so on. 
    
    """
    _instance = None

    def __init__( self, type_Mode:int, histogram, 
                  In_true_Nu:np.ndarray  , Calc_reco_Nu:np.ndarray,
                  In_true_Anti:np.ndarray, Calc_reco_Anti:np.ndarray,
                  In_reco_Nu:np.ndarray  , In_reco_Anti:np.ndarray ):
        self.type_mode     = type_Mode
        self.hist          = histogram
        self.In_true_Nu    = In_true_Nu
        self.Cal_reco_Nu   = Calc_reco_Nu
        self.In_true_Anti  = In_true_Anti
        self.Cal_reco_Anti = Calc_reco_Anti
        self.In_reco_Nu    = In_reco_Nu
        self.In_reco_Anti  = In_reco_Anti
        #
        Graph_all._instance = self    
    @classmethod
    def input_data(cls, type_Mode:int, histogram, 
                        In_true_Nu:np.ndarray  , Calc_reco_Nu:np.ndarray, 
                        In_true_Anti:np.ndarray, Calc_reco_Anti:np.ndarray ):
        setup_hist    = cls( type_Mode, histogram, In_true_Nu, Calc_reco_Nu, In_true_Anti, Calc_reco_Anti, None, None )
        cls._instance = setup_hist 
        return cls._instance
    @classmethod
    def input_change(cls, In_reco_Nu:np.ndarray=None, In_reco_Anti:np.ndarray=None):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(options) first. ")
        else:
            if In_reco_Nu is not None and In_reco_Anti is not None:
                cls._instance.In_reco_Nu   = In_reco_Nu
                cls._instance.In_reco_Anti = In_reco_Anti
            elif In_reco_Nu is None and In_reco_Anti is None:
                cls._instance.In_reco_Nu   = None
                cls._instance.In_reco_Anti = None
            else:
                raise Exception(" Both vectors of In_reco_Nu(Anti) must be non-zero! ")
            return cls._instance
    
    def get_plot_bar(self, y_lim:float, y_list_scale:list):                                     # Getting the plot    
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        # Adjust the edges of the frame
        plt.gca().spines['top'].set_linewidth(4)                                                # Top edge
        plt.gca().spines['right'].set_linewidth(4)                                              # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'].set_linewidth(4)                                               # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x', direction='in', pad =10, length=15)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad =10, length=15)                            # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=24)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm true/reco.} \ [GeV]$', fontdict={'size':27})                 # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/3.5 \ yr}$', fontdict={'size':27}, labelpad=8)      # Add label y-axis
        
        #
        ## Neutrino Mode
        #
        if self.type_mode == +1:                                                                       # Write on the frame - Neutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,y_lim)
            plt.xticks([0, 5, 10, 15, 20] )                                                                # Specifying the values that will appear on the x axis
            plt.yticks(y_list_scale)                                                                       # Specifying the values that will appear on the y axis    
            plt.text(0.3, 37, f'Neutrino mode', fontsize=35, color='black')
        #
        ## Antineutrino Mode
        #
        elif self.type_mode == -1:                                                                     # Write on the frame - AntiNeutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,y_lim)
            plt.xticks([0, 5, 10, 15, 20])                                                                 # Specifying the values that will appear on the x axis
            plt.yticks(y_list_scale)                                                                       # Specifying the values that will appear on the y axis
            plt.text(0.3, 37/2, f'Antineutrino mode', fontsize=35, color='black')
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
        if self.type_mode == +1:                                                                                                 # Neutrino Mode:
            # Tau_minus : Neutrino                                                                                               # Tau_minus : Neutrino
            Contour_bar(self.hist, self.In_true_Nu  ).get_plot(.8, 'green', 'dashed', 2, r'${{\rm Input: } \ \tau^{-} \ {\rm events}}$')            # Input : In_MNu_true_Nu
            Contour_bar(self.hist, self.Cal_reco_Nu ).get_plot(1 , 'green', 'solid' , 3, r'${ \tau^{-} \ {\rm events}}$'               )            # Calc. : Cal_MNu_reco_Nu
            if self.In_reco_Nu is not None:
                plt.scatter( build_bins, self.In_reco_Nu, color='black', label='Input: data reconst.' )                                             # Input : In_MNu_reco_Nu
            # Tau_plus : Antineutrino                                                                                            # Tau_plus  : Antineutrino
            Contour_bar(self.hist, self.In_true_Anti  ).get_plot(.8, (0.9, 0.5, 0), 'dashed', 2, r'${{\rm Input: } \ \tau^{+} \ {\rm events}}$')    # Input : In_MNu_true_Anti
            Contour_bar(self.hist, self.Cal_reco_Anti ).get_plot(1 , (0.9, 0.5, 0), 'solid' , 3, r'${ \tau^{+} \ {\rm events}}$'               )    # Calc. : Cal_MNu_reco_Anti
            if self.In_reco_Anti is not None:
                plt.scatter( build_bins, self.In_reco_Anti, color='black' )                                                                         # Input : In_MNu_reco_Anti
        #
        ##   Antineutrino Mode
        #
        else:                                                                                                                    # AntiNeutrino Mode:
            # Tau_minus : Neutrino                                                                                               # Tau_minus : Neutrino
            Contour_bar(self.hist, self.In_true_Nu  ).get_plot(.8, 'green', 'dashed', 2, r'${{\rm Input: } \ \tau^{-} \ {\rm events}}$')            # Input : In_MAn_true_Nu
            Contour_bar(self.hist, self.Cal_reco_Nu ).get_plot(1 , 'green', 'solid' , 3, r'${ \tau^{-} \ {\rm events}}$'               )            # Calc. : Cal_MAn_reco_Nu
            if self.In_reco_Nu is not None:
                plt.scatter( build_bins, self.In_reco_Nu, color='black', label='Input: data reconst.' )                                             # Input : In_MAn_reco_Nu
            # Tau_plus : Antineutrino                                                                                            # Tau_plus : AntiNeutrino
            Contour_bar(self.hist, self.In_true_Anti  ).get_plot(.8, (0.9, 0.5, 0), 'dashed', 2, r'${{\rm Input: } \ \tau^{+} \ {\rm events}}$')    # Input : In_MAn_true_Anti
            Contour_bar(self.hist, self.Cal_reco_Anti ).get_plot(1 , (0.9, 0.5, 0), 'solid' , 3, r'${ \tau^{+} \ {\rm events}}$'               )    # Calc. : Cal_MAn_reco_Anti
            if self.In_reco_Anti is not None:
                plt.scatter( build_bins, self.In_reco_Anti, color='black' )                                                                         # Input : In_MAn_reco_Anti
            
        plt.legend( fontsize=24 )                                                                                      # Add legend
        
        plt.pause(0.01)                                                                                                # Displaying the graph and pausing execution
        print(f"\nEvents_minus: { round(sum( [ 0.5*vec     for vec in self.Cal_reco_Nu]   ), 3) }")
        print(f"Events_plus : {   round(sum( [ 0.5*vec     for vec in self.Cal_reco_Anti] ), 3) }")

        #plt.savefig('../Image_article/Fig2_Event_MAn.pdf', format='pdf')                                              # Save with .pdf
        input("Enter to continue: ")                                                                                   # Waiting for keyboard input to continue
        plt.close()                                                                                                    # Close image
        return


class Graph_all_comp:
    """ Note: This function draws all (all) the graphs in the article frame, i.e., neutrino mode will have tau_minus and tau_plus and so on. """
    def __init__( self, type_mode:int, histogram, new_reco_Nu:np.ndarray, new_reco_Anti:np.ndarray ):
        self.type_mode = type_mode
        self.hist      = histogram
        self.new_Nu    = new_reco_Nu
        self.new_Anti  = new_reco_Anti   
    @classmethod
    def input_data(cls, type_mode:int, histogram, new_reco_Nu:np.ndarray, new_reco_Anti:np.ndarray):
        return cls( type_mode, histogram, new_reco_Nu, new_reco_Anti )
    
    def get_plot_bar(self, y_lim:float, y_list_scale:list):                                     # Getting the plot    
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
        plt.xlabel(r'$E_{\nu}^{\rm reco.} \ [GeV]$'    , fontdict={'size':27})                  # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/3.5 \ yr}$', fontdict={'size':27}, labelpad=8)      # Add label y-axis
        
        #
        ## Neutrino Mode
        #
        if self.type_mode == +1:                                                                       # Write on the frame - Neutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,y_lim)
            plt.xticks([0, 5, 10, 15, 20])                                                                 # Specifying the values that will appear on the x axis
            plt.yticks(y_list_scale)                                                                       # Specifying the values that will appear on the y axis
            
            plt.text(14.45, 16.0, f'Neutrino mode', fontsize=26, color='blue')
        #
        ## Antineutrino Mode
        #
        elif self.type_mode == -1:                                                                     # Write on the frame - AntiNeutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,y_lim)
            plt.xticks([0, 5, 10, 15, 20])                                                                 # Specifying the values that will appear on the x axis
            plt.yticks(y_list_scale)                                                                       # Specifying the values that will appear on the y axis
            
            plt.text(13.10, 16, f'Antineutrino mode', fontsize=26, color='blue')
        #
        ## Different Mode
        #
        else:                                                                                              # If it is not a Neutrino or Antineutrino Mode
            raise Exception(" Choose : +1 for Neutrino Mode or -1 for Antineutrino Mode. ")
            
        """ 
            Creating the Plot 
        """
        #
        ##   Neutrino Mode
        #
        if self.type_mode == +1:                                                                                                 # Neutrino Mode:
            BF_Nu   = In_pre_MNu_Nu
            BF_Anti = In_pre_MNu_Anti          
            # Tau_minus : Neutrino                                                                                               # Tau_minus : Neutrino
            Contour_bar( self.hist, BF_Nu       ).get_plot( .6, 'green', 'dashed', 2, r'${{\rm Best-Fit: } \ \tau^{-} \ {\rm events}}$'   )         # Input : B-F_MNu_true_Nu
            Contour_bar( self.hist, self.new_Nu ).get_plot( 1 , 'green', 'solid' , 3, r'${{\rm New \ case: } \ \tau^{-} \ {\rm events}}$' )         # Calc. : Cal_MNu_reco_Nu
            # Tau_plus : Antineutrino                                                                                            # Tau_plus : Antineutrino
            Contour_bar( self.hist, BF_Anti       ).get_plot( .6, (0.9, 0.5, 0), 'dashed', 2, r'${{\rm Best-Fit: } \ \tau^{+} \ {\rm events}}$'   ) # Input : B-F_MNu_true_Anti
            Contour_bar( self.hist, self.new_Anti ).get_plot( 1 , (0.9, 0.5, 0), 'solid' , 3, r'${{\rm New \ case: } \ \tau^{+} \ {\rm events}}$' ) # Calc. : Cal_MNu_reco_Anti
        #
        ##   Antineutrino Mode
        #
        else:                                                                                                                    # AntiNeutrino Mode:
            BF_Nu   = In_pre_MAn_Nu
            BF_Anti = In_pre_MAn_Anti
            # Tau_minus : Neutrino                                                                                               # Tau_minus : Neutrino
            Contour_bar( self.hist, BF_Nu       ).get_plot( .6, 'green', 'dashed', 2, r'${{\rm Best-Fit: } \ \tau^{-} \ {\rm events}}$' )           # Input : B-F_MAn_true_Nu
            Contour_bar( self.hist, self.new_Nu ).get_plot( 1 , 'green', 'solid' , 3, r'${{\rm New case: } \ \tau^{-} \ {\rm events}}$' )           # Calc. : Cal_MAn_reco_Nu
            # Tau_plus : Antineutrino                                                                                            # Tau_plus : AntiNeutrino
            Contour_bar( self.hist, BF_Anti       ).get_plot( .6, (0.9, 0.5, 0), 'dashed', 2, r'${{\rm Best-Fit: } \ \tau^{+} \ {\rm events}}$' )   # Input : B-F_MAn_true_Anti
            Contour_bar( self.hist, self.new_Anti ).get_plot( 1 , (0.9, 0.5, 0), 'solid' , 3, r'${{\rm New case: } \ \tau^{+} \ {\rm events}}$' )   # Calc. : Cal_MAN_reco_Anti
            
        legend = plt.legend( fontsize=24 )                                                                             # Add legend
        frame = legend.get_frame()
        frame.set_edgecolor('black')                                                                                   # Add legend
        
        plt.pause(0.01)                                                                                                # Displaying the graph and pausing execution
        print(f"\nEvents_minus: { round(sum( [ 0.5*vec     for vec in self.new_Nu] ), 3)   }")
        print(f"Events_plus : {   round(sum( [ 0.5*vec     for vec in self.new_Anti] ), 3) }")

        input("Enter to continue: ")                                                                                   # Waiting for keyboard input to continue
        plt.close()                                                                                                    # Close image
        return


#
##     Graph_HE_bar (Uniform and Joint)
#
class Graph_HE:
    """ 
    Note: 
        
        This function draws one type of graph: High energy (HE) mode for tau_minus. 
    """
    _instance = None
    
    def __init__( self, histogram, In_true:np.ndarray, Calc_reco:np.ndarray, In_reco:np.ndarray ):
        self.hist      = histogram
        self.In_true   = In_true
        self.Calc_reco = Calc_reco
        self.In_reco   = In_reco
        #
        Graph_HE._instance = self
    @classmethod
    def input_data(cls, histogram, In_true:np.ndarray, Calc_reco:np.ndarray):
        setup_hist = cls( histogram, In_true, Calc_reco, None )
        cls._instance = setup_hist 
        return cls._instance
    @classmethod
    def input_change(cls, In_reco:np.ndarray):
        if cls._instance is None:
            raise Exception(" No existing instance. Use input_data(options) first. ")
        else:
            cls._instance.In_reco = In_reco
            return cls._instance
    
    def get_plot_bar(self, y_lim:float, y_list_scale:list):                                     # Getting the plot    
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        plt.xlim(0,20)                                                                          # Axis limit
        plt.ylim(0,y_lim)
        plt.xticks([0, 5, 10, 15, 20])                                                          # Specifying the values that will appear on the x axis
        plt.yticks(y_list_scale)                                                                # Specifying the values that will appear on the y axis

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
        plt.xlabel(r'$E_{\nu}^{\rm true/reco.} \ [GeV]$', fontdict={'size':27})                 # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/yr}$', fontdict={'size':27}, labelpad=8)            # Add label y-axis                   
        plt.text(0.3, 37/2, f'High energy mode', fontsize=35, color='black')

        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.hist.bins ]                                               # Defined in the library histogram_unif.py
    
        # High Energy Mode: Neutrino                                                                                        # High energy Mode: Neutrino
        Contour_bar(self.hist, self.In_true  ).get_plot(.8, 'green', 'dashed', 2, r'${{\rm Input: } \ \tau^{-} \ {\rm events}}$')   # Input : In_MFE_true_Nu
        Contour_bar(self.hist, self.Calc_reco).get_plot(1 , 'green', 'solid' , 3, r'${ \tau^{-} \ {\rm events}}$'               )   # Calc. : Cal_MHE_reco_Nu
        if self.In_reco is not None:
            plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                    # Input : In_MFE_reco_Nu
            
        plt.legend( fontsize=24 )                                                                                           # Add legend

        plt.pause(0.01)                                                                                                     # Displaying the graph and pausing execution
        print(f"\nEvents_minus: { round(sum( [ 0.5*vec     for vec in self.Calc_reco] ), 3) }")

        #plt.savefig('../Image_article/Fig2_Event_MHE.pdf', format='pdf')                                                    # Save with .pdf
        input("Enter to continue: ")                                                                                        # Waiting for keyboard input to continue
        plt.close()                                                                                                         # Close image
        return


class Graph_HE_comp:
    """ 
    Note: 

        This function draws one type of graph: High energy (HE) mode for tau_minus. 
    """
    def __init__( self, histogram, new_reco_Nu:np.ndarray ):
        self.hist   = histogram
        self.new_Nu = new_reco_Nu
    @classmethod
    def input_data(cls, histogram, new_reco_Nu:np.ndarray):
        return cls( histogram, new_reco_Nu ) 
        
    def get_plot_bar(self, y_lim:float, y_list_scale:list):                                     # Getting the plot    
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        plt.xlim(0,20)                                                                          # Axis limit
        plt.ylim(0,y_lim)
        plt.xticks([0, 5, 10, 15, 20])                                                          # Specifying the values that will appear on the x axis
        plt.yticks(y_list_scale)                                                                # Specifying the values that will appear on the y axis

        # Adjust the edges of the frame
        plt.gca().spines['top'].set_linewidth(4)                                                # Top edge
        plt.gca().spines['right'].set_linewidth(4)                                              # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'].set_linewidth(4)                                               # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x', direction='in', pad =10, length=15)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad =10, length=15)                            # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=24)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm reco.} \ [GeV]$', fontdict={'size':27})                      # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/yr}$'  , fontdict={'size':27}, labelpad=8)          # Add label y-axis              
        plt.text(13.12, 19.25, f'High energy mode', fontsize=26, color='blue')

        """ 
            Creating the Plot 
        """
        # High Energy Mode                                                                                                  # High energy mode: Neutrino
        BF_HE = In_pre_MHE_Nu
        Contour_bar( self.hist, BF_HE      ).get_plot( .6, 'green', 'dashed', 2, r'${{\rm Best-Fit: } \ \tau^{-} \ {\rm events}}$' )     # Input : B-F_MHE_true_Nu
        Contour_bar( self.hist, self.new_Nu).get_plot( 1 , 'green', 'solid' , 3, r'${{\rm New \ case} \ \tau^{-} \ {\rm events}}$' )     # Calc. : Cal_MHE_reco_Nu
            
        legend = plt.legend( fontsize=24 )                                                                                  # Add legend
        frame = legend.get_frame()
        frame.set_edgecolor('black') 

        plt.pause(0.01)                                                                                                     # Displaying the graph and pausing execution

        print(f"\nEvents_minus: { round(sum( [ 0.5*vec     for vec in self.new_Nu] ), 3) }")
        input("Enter to continue: ")                                                                                        # Waiting for keyboard input to continue
        plt.close()                                                                                                         # Close image
        return




if __name__ == "__main__":
    from Init_00_tau.histogram  import *
    from Init_00_tau.rules_reco import *
    
    show = 0
    histogram = Histogram.get_Uniform_SP(0, 40, 0.5)                                                        # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5

    if show == 0:
        # Neutrino Mode (Calculate):                                                                                        # Neutrino (Calc.): Reconstruction
        cal_MNu_reco_Nu   = Rule_smear.input_data( histogram, In_MNu_true_Nu  ).get_middle(NormMid_MNu_Nu  )                         # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( histogram, In_MNu_true_Anti).get_middle(NormMid_MNu_Anti)                         # Mode_Nu : Events/bin Antineutrino
        #plt_Nu = Graph_all( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti, In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu = Graph_all.input_data( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti )
        plt_Nu.input_change( In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu.get_plot_bar(40, [0, 10, 20, 30, 40])

        # Antineutrino Mode (Calculate):                                                                                    # Antineutrino (Calc.): Reconstruction
        cal_MAn_reco_Nu   = Rule_smear.input_data( histogram, In_MAn_true_Nu  ).get_middle(NormMid_MAn_Nu  )                         # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( histogram, In_MAn_true_Anti).get_middle(NormMid_MAn_Anti)                         # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_all.input_data( -1, histogram, In_MAn_true_Nu, cal_MAn_reco_Nu, In_MAn_true_Anti, cal_MAn_reco_Anti )
        plt_Anti.input_change( In_MAn_reco_Nu, In_MAn_reco_Anti )
        plt_Anti.get_plot_bar(20, [0, 5, 10, 15, 20])

        # High Energy Mode (Calculate):                                                                                     # High Energy (Calc.): Reconstruction
        cal_MHE_reco_Nu = Rule_smear.input_data( histogram, In_MHE_true_Nu ).get_middle(NormMid_MHE_Nu)                              # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_HE.input_data( histogram, In_MHE_true_Nu, cal_MHE_reco_Nu )
        plt_HE.input_change( In_MHE_reco_Nu )
        plt_HE.get_plot_bar(20, [0, 5, 10, 15, 20])
    
    elif show == 1:
        # Neutrino Mode (Calculate):                                                                                        # Neutrino (Calc.): Reconstruction
        cal_MNu_reco_Nu   = Rule_smear.input_data( histogram, In_MNu_true_Nu  ).get_5to5(Norm5x5_MNu_Nu  )                           # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( histogram, In_MNu_true_Anti).get_5to5(Norm5x5_MNu_Anti)                           # Mode_Nu : Events/bin Antineutrino
        #plt_Nu = Graph_all( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti, In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu = Graph_all.input_data( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti )
        plt_Nu.input_change( In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu.get_plot_bar(40, [0, 10, 20, 30, 40])

        # Antineutrino Mode (Calculate):                                                                                    # Antineutrino (Calc.): Reconstruction
        cal_MAn_reco_Nu   = Rule_smear.input_data( histogram, In_MAn_true_Nu  ).get_5to5(Norm5x5_MAn_Nu  )                           # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( histogram, In_MAn_true_Anti).get_5to5(Norm5x5_MAn_Anti)                           # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_all.input_data( -1, histogram, In_MAn_true_Nu, cal_MAn_reco_Nu, In_MAn_true_Anti, cal_MAn_reco_Anti )
        plt_Anti.input_change( In_MAn_reco_Nu, In_MAn_reco_Anti )
        plt_Anti.get_plot_bar(20, [0, 5, 10, 15, 20])

        # High Energy Mode (Calculate):                                                                                     # High Energy (Calc.): Reconstruction
        cal_MHE_reco_Nu = Rule_smear.input_data( histogram, In_MHE_true_Nu ).get_5to5(Norm5x5_MHE_Nu)                                # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_HE.input_data( histogram, In_MHE_true_Nu, cal_MHE_reco_Nu )
        plt_HE.input_change( In_MHE_reco_Nu )
        plt_HE.get_plot_bar(20, [0, 5, 10, 15, 20])

    elif show == 2:
        # Neutrino Mode (Calculate):                                                                                        # Neutrino (Calc.): Reconstruction
        cal_MNu_reco_Nu   = Rule_smear.input_data( histogram, In_MNu_true_Nu  ).get_5to5_pre(Norm5x5_MNu_Nu  )                       # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( histogram, In_MNu_true_Anti).get_5to5_pre(Norm5x5_MNu_Anti)                       # Mode_Nu : Events/bin Antineutrino
        #plt_Nu = Graph_all( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti, In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu = Graph_all.input_data( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti )
        plt_Nu.input_change( In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu.get_plot_bar(40, [0, 10, 20, 30, 40])

        # Antineutrino Mode (Calculate):                                                                                    # Antineutrino (Calc.): Reconstruction
        cal_MAn_reco_Nu   = Rule_smear.input_data( histogram, In_MAn_true_Nu  ).get_5to5_pre(Norm5x5_MAn_Nu  )                       # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( histogram, In_MAn_true_Anti).get_5to5_pre(Norm5x5_MAn_Anti)                       # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_all.input_data( -1, histogram, In_MAn_true_Nu, cal_MAn_reco_Nu, In_MAn_true_Anti, cal_MAn_reco_Anti )
        plt_Anti.input_change( In_MAn_reco_Nu, In_MAn_reco_Anti )
        plt_Anti.get_plot_bar(20, [0, 5, 10, 15, 20])

        # High Energy Mode (Calculate):                                                                                     # High Energy (Calc.): Reconstruction
        cal_MHE_reco_Nu = Rule_smear.input_data( histogram, In_MHE_true_Nu ).get_5to5_pre(Norm5x5_MHE_Nu)                            # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_HE.input_data( histogram, In_MHE_true_Nu, cal_MHE_reco_Nu )
        plt_HE.input_change( In_MHE_reco_Nu )
        plt_HE.get_plot_bar(20, [0, 5, 10, 15, 20])

    elif show == 3:
        # Neutrino Mode (Calculate):                                                                                        # Neutrino (Calc.): Reconstruction
        cal_MNu_reco_Nu   = Rule_smear.input_data( histogram, In_MNu_true_Nu  ).input_change(0.28, 0.46, 1).get_5to5(Norm5x5_MNu_Nu  )  # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( histogram, In_MNu_true_Anti).input_change(0.28, 0.46, 1).get_5to5(Norm5x5_MNu_Anti)  # Mode_Nu : Events/bin Antineutrino
        plt_Nu = Graph_all_comp( +1, histogram, cal_MNu_reco_Nu, cal_MNu_reco_Anti  )
        #plt_Nu = Graph_all_comp.input_data( +1, histogram, cal_MNu_reco_Nu, cal_MNu_reco_Anti )
        plt_Nu.get_plot_bar(25, [0, 5, 10, 15, 20, 25])

        # Antineutrino Mode (Calculate):                                                                                    # Antineutrino (Calc.): Reconstruction
        cal_MAn_reco_Nu   = Rule_smear.input_data( histogram, In_MAn_true_Nu  ).input_change(0.28, 0.46, 1).get_5to5(Norm5x5_MAn_Nu  )  # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( histogram, In_MAn_true_Anti).input_change(0.28, 0.46, 1).get_5to5(Norm5x5_MAn_Anti)  # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_all_comp.input_data( -1, histogram, cal_MAn_reco_Nu, cal_MAn_reco_Anti )
        plt_Anti.get_plot_bar(25, [0, 5, 10, 15, 20, 25])

        # High Energy Mode (Calculate):                                                                                     # High Energy (Calc.): Reconstruction
        cal_MHE_reco_Nu = Rule_smear.input_data( histogram, In_MHE_true_Nu ).input_change(0.28, 0.46, 1).get_5to5(Norm5x5_MHE_Nu)       # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_HE_comp.input_data( histogram, cal_MHE_reco_Nu )
        plt_HE.get_plot_bar(25, [0, 5, 10, 15, 20, 25])

    elif show == 4:
        # Neutrino Mode (Calculate):                                                                                        # Neutrino (Calc.): Reconstruction
        """ cal_MNu_reco_Nu   = Rule_smear.input_data( histogram, In_MNu_true_Nu  ).get_5to5_pre(Norm5x5_MNu_Nu  )                          # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( histogram, In_MNu_true_Anti).get_5to5_pre(Norm5x5_MNu_Anti)                          # Mode_Nu : Events/bin Antineutrino
        #plt_Nu = Graph_all( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti, In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu = Graph_all.input_data( +1, histogram, In_MNu_true_Nu, cal_MNu_reco_Nu, In_MNu_true_Anti, cal_MNu_reco_Anti )
        plt_Nu.input_change( In_MNu_reco_Nu, In_MNu_reco_Anti )
        plt_Nu.get_plot_bar(40, [0, 10, 20, 30, 40]) """ 
        #plt.savefig('../Image_article/Fig2_Event_MNu.pdf', format='pdf')


        # Antineutrino Mode (Calculate):                                                                                    # Antineutrino (Calc.): Reconstruction
        """ cal_MAn_reco_Nu   = Rule_smear.input_data( histogram, In_MAn_true_Nu  ).get_5to5_pre(Norm5x5_MAn_Nu  )                          # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( histogram, In_MAn_true_Anti).get_5to5_pre(Norm5x5_MAn_Anti)                          # Mode_An : Events/bin Antineutrino
        plt_Anti = Graph_all.input_data( -1, histogram, In_MAn_true_Nu, cal_MAn_reco_Nu, In_MAn_true_Anti, cal_MAn_reco_Anti )
        plt_Anti.input_change( In_MAn_reco_Nu, In_MAn_reco_Anti )
        plt_Anti.get_plot_bar(20, [0, 5, 10, 15, 20]) """
        #plt.savefig('../Image_article/Fig2_Event_MAn.pdf', format='pdf')


        # High Energy Mode (Calculate):                                                                                     # High Energy (Calc.): Reconstruction
        """ cal_MHE_reco_Nu = Rule_smear.input_data( histogram, In_MHE_true_Nu ).get_5to5_pre(Norm5x5_MHE_Nu)                               # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_HE.input_data( histogram, In_MHE_true_Nu, cal_MHE_reco_Nu )
        plt_HE.input_change( In_MHE_reco_Nu )
        plt_HE.get_plot_bar(20, [0, 5, 10, 15, 20]) """
        #plt.savefig('../Image_article/Fig2_Event_MHE.pdf', format='pdf')

