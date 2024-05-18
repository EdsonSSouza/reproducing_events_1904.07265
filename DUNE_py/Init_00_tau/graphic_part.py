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


# OBJ: Neutrino Mode (+1) and Antineutrino Mode (-1)

# Plot only the outline of the bars
class Contour_bar:
    def __init__( self, histogram, signal ) -> None:
        self.hist  = histogram
        self.sign  = signal 

    def get_plot( self, int_alpha, str_color, str_style, width, str_label ):
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
            plt.plot(x_contour, y_contour, color=str(str_color), linestyle=str(str_style), linewidth=width, label=str(str_label), alpha=int_alpha )
        else:
            buil_color = [ icolor   for icolor in str_color ]
            buil_color.append(int_alpha) 
            color_real = tuple( buil_color )
            plt.plot(x_contour, y_contour, color=color_real    , linestyle=str(str_style), linewidth=width, label=str(str_label) )


#
##     Graph_events_bar (Uniform and Joint)
#
class Graph_each:
    """ Note: This function draws one type (single) of graph on the article frame at a time with the events number, i.e., neutrino mode for tau_minus or tau_plus and so on. """
    def __init__( self, type_mode, signal_tau, histogram, In_true, In_reco, Calc_reco ):
        self.type_mode = type_mode
        self.sign_tau  = signal_tau
        self.hist      = histogram
        self.In_true   = In_true
        self.In_reco   = In_reco
        self.Calc_reco = Calc_reco
        #
        Graph_each._instance = self
    @classmethod
    def input_data(cls, type_mode, signal_tau, histogram, In_true, In_reco, Calc_reco):
        return cls( type_mode, signal_tau, histogram, In_true, In_reco, Calc_reco )

    def get_plot_bar(self):                                                                     # Getting the plot    
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
        if self.type_mode == +1:                                                                           # Write on the frame - Neutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit 
            plt.ylim(0,40)
            plt.xticks([0, 5, 10, 15, 20] )                                                                # Specifying the values that will appear on the x axis
            plt.yticks([0, 10, 20, 30, 40])                                                                # Specifying the values that will appear on the y axis
            
            plt.text(11, 20,
                        r'$\bf{\qquad types}\qquad$'   r'$\bf{\qquad\qquad \ \ total/3.5 \ yr \quad }$' 
                        f"\n"
                        f"Input: data true                    {round( 0.5*sum( self.In_true ), 2 )}\n"
                        f"Input: data reconst.              {round( 0.5*sum( self.In_reco ), 2 )}\n"
                        f"Calc.: data reconst.              {round( 0.5*sum( self.Calc_reco ), 2 )}"
                    ,fontsize=16, color='blue', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            
            if self.sign_tau == -1:                                                                             # Tau_minus : Neutrino
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{-} \ events:\ {\rm neutrino \ mode\ \ \:}} $'
                            f"            "
                        ,fontsize=16, color='green', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            elif self.sign_tau == +1:                                                                           # Tau_plus : Antineutrino
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{+} \ events:\ {\rm neutrino \ mode\ \ \ \ \:}}$'
                            f"          "
                        ,fontsize=16, color='darkorange', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            else:                                                                                               # Invalidated choice
                raise Exception(" Choose : +1 for tau_plus or -1 for tau_minus. ")
            
            plt.text(0.3, 37, f'Neutrino mode', fontsize=35)
        #
        ## Antineutrino Mode
        #
        elif self.type_mode == -1:                                                                         # Write on the frame - AntiNeutrino Mode:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,40/2)
            plt.xticks([0, 5, 10, 15, 20])                                                                 # Specifying the values that will appear on the x axis
            plt.yticks([0, 5, 10, 15, 20])                                                                 # Specifying the values that will appear on the y axis
            
            plt.text(11, 20/2,
                        r'$\bf{\qquad types}\qquad$'   r'$\bf{\qquad\qquad \ \ total/3.5 \ yr \quad }$' 
                        f"\n"
                        f"Input: data true                    {round( 0.5*sum( self.In_true ), 2 )}\n"
                        f"Input: data reconst.              {round( 0.5*sum( self.In_reco ), 2)}\n"
                        f"Calc.: data reconst.              {round( 0.5*sum( self.Calc_reco ), 2)}"
                    ,fontsize=16, color='blue', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            
            if self.sign_tau == -1:                                                                             # Tau_minus : Neutrino
                plt.text(11, 27.2/2, 
                            r'$\bf{\tau^{-} \ events:\ {\rm antineutrino \ mode\ \ \ \:}}$'
                            f"     "
                        ,fontsize=16, color='green', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            elif self.sign_tau == +1:                                                                           # Tau_plus : Antieutrino
                plt.text(11, 27.2/2, 
                            r'$\bf{\tau^{+} \ events:\ {\rm antineutrino \ mode\ \ \ \:}}$'
                            f"     "
                        ,fontsize=16, color='darkorange', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            else:                                                                                               # Invalidated choice
                raise Exception(" Choose : +1 for tau_plus or -1 for tau_minus. ")
            
            plt.text(0.3, 37/2, f'Antineutrino mode', fontsize=35) 
        #
        ## Different Mode
        #
        else:                                                                                              # If it is not a Neutrino or Antineutrino Mode
            raise Exception(" choose : +1 for Neutrino Mode or -1 for Antineutrino Mode. ")
            
        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.hist.bins ]                                               # Defined in the library histogram_unif.py
        
        if self.sign_tau == -1:                                                                                             # Tau_minus : Neutrino
            plt.pause(0.2)
            Contour_bar( self.hist, self.In_true ).get_plot( 1, 'green', 'dashed', 2.0, 'Input: data true' )                        # Input : In_MNu(An)_true_Nu
            plt.pause(0.5)
            plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                    # Input : In_MNu(An)_reco_Nu
            plt.pause(0.5)
            Contour_bar( self.hist, self.Calc_reco ).get_plot( 1, 'green', 'solid', 3.0, 'Calculated: data reconst.' )              # Calc. : Cal_MNu(An)_reco_Nu
            
        elif self.sign_tau == +1:                                                                                           # Tau_plus : AntiNeutrino
            plt.pause(0.2)
            Contour_bar( self.hist, self.In_true ).get_plot( 1, (0.9, 0.5, 0), 'dashed', 2.0, 'Input: data true' )                  # Input : In_MNu(An)_true_Anti
            plt.pause(0.5)
            plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                    # Input : In_MNu(An)_reco_Anti
            plt.pause(0.5)
            Contour_bar( self.hist, self.Calc_reco ).get_plot( 1, (0.9, 0.5, 0), 'solid', 3.0, 'Calculated: data reconst.' )        # Calc. : Cal_MNu(An)_reco_Anti

        plt.legend( fontsize=22 )                                                                                           # Add legend

        plt.pause(0.01)                                                                                                     # Displaying the graph and pausing execution

        input("Enter to continue: ")                                                                                        # Waiting for keyboard input to continue
        plt.close()                                                                                                         # Close image
        return 


#
##     Graph_HE(events)_bar (Uniform and Joint)
#
class Graph_each_HE:
    """ Note: This function draws one type of graph: High energy (HE) mode for tau_minus with the events number. """
    def __init__( self, histogram, In_true, In_reco, Calc_reco ):
        self.hist      = histogram
        self.In_true   = In_true
        self.In_reco   = In_reco
        self.Calc_reco = Calc_reco
    @classmethod
    def input_data(cls, histogram, In_true, In_reco, Calc_reco):
        return cls( histogram, In_true, In_reco, Calc_reco ) 
    
    def get_plot_bar(self):                                                                     # Getting the plot    
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        plt.xlim(0,20)                                                                          # Axis limit
        plt.ylim(0,40/2)
        plt.xticks([0, 5, 10, 15, 20])                                                          # Specifying the values that will appear on the x axis
        plt.yticks([0, 5, 10, 15, 20])                                                          # Specifying the values that will appear on the y axis

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
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/yr}$', fontdict={'size':27}, labelpad=8)            # Add label y-axis

        plt.text(11, 27.2/2,                                                                    # Write on the frame: All
                    r'$\bf{\tau^{-} \ events:\ {\rm neutrino \ mode \ \ \:}}$'
                    f"            "
                ,fontsize=16, color='green', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            
            
        plt.text(0.3, 37/2, f'High energy mode', fontsize=35, color='black')
            
        plt.text(11, 20/2,
                    r'$\bf{\qquad types}\qquad$'   r'$\bf{\qquad\qquad \ \ total/1.0 \ yr }$' 
                    f"\n"
                    f"Input: data true                    {round( 0.5*sum( self.In_true ), 2)}\n"
                    f"Input: data reconst.              {round( 0.5*sum( self.In_reco ), 2)}\n"
                    f"Calc.: data reconst.              {round( 0.5*sum( self.Calc_reco ), 2)}"
                ,fontsize=16, color='blue', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.hist.bins ]                                               # Defined in the library histogram_unif.py
    
        # High energy Mode                                                                                                  # High energy Mode
        plt.pause(0.2)
        Contour_bar( self.hist, self.In_true ).get_plot( 1, 'green', 'dashed', 2, 'Input: data true' )                             # Input : In_MHE_true_Nu
        plt.pause(0.5)
        Contour_bar( self.hist, self.Calc_reco ).get_plot( 1, 'green', 'solid', 3.0, 'Calculated: data reconst.' )                 # Calc. : Cal_MHE_reco_Nu
        plt.pause(0.5)
        plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                       # Input : In_MHE_reco_Nu
            
        plt.legend( fontsize=22 )                                                                                           # Add legend

        plt.pause(0.01)                                                                                                     # Displaying the graph and pausing execution

        input("Enter to continue: ")                                                                                        # Waiting for keyboard input to continue
        plt.close()                                                                                                         # Close image
        return




if __name__ == "__main__":
    from Init_00_tau.read_vec   import *
    from Init_00_tau.histogram  import *
    from Init_00_tau.rules_reco import *
    
    show = 1
    histogram = Histogram.get_Uniform_SP(0, 40, 0.5)                                                        # Histogram_Bins : SP (Start Point = 0.0) for 40 bins of width 0.5

    if show == 1:
        # Neutrino Mode (Calculate):                                                                                    # Neutrino (Calc.): Reconstruction
        cal_MNu_reco_Nu   = Rule_smear.input_data( histogram, In_MNu_true_Nu  ).get_5to5_pre(Norm5x5_MNu_Nu  )                      # Mode_Nu : Events/bin Neutrino
        cal_MNu_reco_Anti = Rule_smear.input_data( histogram, In_MNu_true_Anti).get_5to5_pre(Norm5x5_MNu_Anti)                      # Mode_Nu : Events/bin Antineutrino
        plt_minus_Nu = Graph_each.input_data( +1, -1, histogram, In_MNu_true_Nu, In_MNu_reco_Nu, cal_MNu_reco_Nu )
        plt_minus_Nu.get_plot_bar()
        plt_plus_Nu  = Graph_each.input_data( +1, +1, histogram, In_MNu_true_Anti, In_MNu_reco_Anti, cal_MNu_reco_Anti )
        plt_plus_Nu.get_plot_bar()


        # Antineutrino Mode (Calculate):                                                                                # Antineutrino (Calc.): Reconstruction
        cal_MAn_reco_Nu   = Rule_smear.input_data( histogram, In_MAn_true_Nu  ).get_5to5_pre(Norm5x5_MAn_Nu  )                      # Mode_An : Events/bin Neutrino
        cal_MAn_reco_Anti = Rule_smear.input_data( histogram, In_MAn_true_Anti).get_5to5_pre(Norm5x5_MAn_Anti)                      # Mode_An : Events/bin Antineutrino
        plt_minus_Anti = Graph_each.input_data( -1, -1,histogram, In_MAn_true_Nu, In_MAn_reco_Nu, cal_MAn_reco_Nu )
        plt_minus_Anti.get_plot_bar() 
        plt_plus_Anti  = Graph_each.input_data( -1, +1, histogram, In_MAn_true_Anti, In_MAn_reco_Anti, cal_MAn_reco_Anti )
        plt_plus_Anti.get_plot_bar()

        # High Energy Mode (Calculate):                                                                                 # High Energy (Calc.): Reconstruction
        cal_MHE_reco_Nu = Rule_smear.input_data( histogram, In_MHE_true_Nu).get_5to5_pre( Norm5x5_MHE_Nu )                          # Mode_HE : Events/bin Neutrino
        plt_HE = Graph_each_HE.input_data( histogram, In_MHE_true_Nu, In_MHE_reco_Nu, cal_MHE_reco_Nu )
        plt_HE.get_plot_bar()


    if show == 2:
        a=1

