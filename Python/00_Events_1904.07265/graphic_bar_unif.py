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


#
##     Graph_single_bar_UJ (Uniform and Joint)
#
# Class that graphs histograms with uniform bins and joints (bin_UJ means bin Uniform and Joint)
    # Note: This function draws one type (single) of graph on the article frame at a time, i.e., neutrino mode for tau_minus or tau_plus and so on.
class Graph_single_bar_UJ:
    _instance = None

    def __init__( self, histogram, In_true, In_reco, Calculed_reco, type_neutrino, type_tau ):
        self.histogram = histogram
        self.In_true = In_true
        self.In_reco = In_reco
        self.Calculed_reco = Calculed_reco
        self.type_neutrino = type_neutrino
        self.type_tau = type_tau
        #
        Graph_single_bar_UJ._instance = self
    @classmethod
    def input_data(cls, in_histogram, in_In_true, in_In_reco, in_Calculed_reco):
        setup_hist = cls( in_histogram, in_In_true, in_In_reco, in_Calculed_reco, +1, -1 )
        cls._instance = setup_hist 
        return cls._instance
    @classmethod
    def input_change(cls, in_type_neutrino, in_type_tau):
        if cls._instance is None:
            raise Exception(" No existing instance. Use get_input_Uniform(histgram, events_bin) first. ")
        else:
            if abs(in_type_tau) != +1:
                raise Exception(" choose : +1 for Tau_plus or -1 for Tau_minus. ")
            elif abs(in_type_neutrino) != +1:
                raise Exception(" choose : +1 for Neutrino or -1 for Antineutrino. ")
            else:
                cls._instance.type_tau = in_type_tau
                cls._instance.type_neutrino = in_type_neutrino
                return cls._instance    

    # Getting the plot
    def get_plot_bar(self):    
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
        ax.tick_params(axis='x', direction='in', pad =10, length=13)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad=10, length=13)                             # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=20)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm true/reco.} \ [GeV]$', fontdict={'size':25})                 # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/3.5 \ yr}$', fontdict={'size':25}, labelpad=7)      # Add label y-axis
        
        #
        ## Neutrino type
        #
        if self.type_neutrino == +1:                                                                       # Write on the frame - Neutrino type:
            plt.xlim(0,20)                                                                                      # Axis limit 
            plt.ylim(0,40)
            
            plt.text(11, 20,
                        r'$\bf{\qquad types}\qquad$'   r'$\bf{\qquad\qquad \ \ total/3.5 \ yr \quad }$' 
                        f"\n"
                        f"Input: data true                    {round( 0.5*sum( self.In_true ), 2 )}\n"
                        f"Input: data reconst.              {round( 0.5*sum( self.In_reco ), 2 )}\n"
                        f"Calc.: data reconst.              {round( 0.5*sum( self.Calculed_reco ), 2 )}"
                    ,fontsize=16, color='blue', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            
            #
            if self.type_tau == -1:                                                                             # Tau_minus : Neutrino
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{-} \ events:\ {\rm neutrino \ mode\ \ \:}} $'
                            f"            "
                        ,fontsize=16, color='green', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            elif self.type_tau == +1:                                                                           # Tau_plus : Neutrino
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{+} \ events:\ {\rm neutrino \ mode\ \ \ \ \:}}$'
                            f"          "
                        ,fontsize=16, color='darkorange', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            else:                                                                                               # Invalidated choice
                raise Exception(" choose : +1 for tau_plus or -1 for tau_minus. ")
            
            plt.text(0.3, 37, f'Neutrino mode', fontsize=35)
        
        #
        ## Antineutrino type
        #
        elif self.type_neutrino == -1:                                                                     # Write on the frame - AntiNeutrino type:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,40/2)
            
            plt.text(11, 20/2,
                        r'$\bf{\qquad types}\qquad$'   r'$\bf{\qquad\qquad \ \ total/3.5 \ yr \quad }$' 
                        f"\n"
                        f"Input: data true                    {round( 0.5*sum( self.In_true ), 2 )}\n"
                        f"Input: data reconst.              {round( 0.5*sum( self.In_reco ), 2)}\n"
                        f"Calc.: data reconst.              {round( 0.5*sum( self.Calculed_reco ), 2)}"
                    ,fontsize=16, color='blue', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            
            #
            if self.type_tau == -1:                                                                             # Tau_minus : Antineutrino
                plt.text(11, 27.2/2, 
                            r'$\bf{\tau^{-} \ events:\ {\rm antineutrino \ mode\ \ \ \:}}$'
                            f"     "
                        ,fontsize=16, color='green', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            elif self.type_tau == +1:                                                                           # Tau_plus : Antieutrino
                plt.text(11, 27.2/2, 
                            r'$\bf{\tau^{+} \ events:\ {\rm antineutrino \ mode\ \ \ \:}}$'
                            f"     "
                        ,fontsize=16, color='darkorange', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            else:                                                                                               # Invalidated choice
                raise Exception(" choose : +1 for tau_plus or -1 for tau_minus. ")
            
            plt.text(0.3, 37/2, f'Antineutrino mode', fontsize=35)
        
        #
        ## If it is not a Neutrino or Antineutrino type
        #
        else:                                                                                              # If it is not a Neutrino or Antineutrino type
            raise Exception(" choose : +1 for Antineutrino or -1 for Neutrino. ")
            
        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.histogram.bins ]                                          # Defined in the library histogram_unif.py
        
        if self.type_tau == -1:                                                                                             # Tau_minus : ( Neutrino | AntiNeutrino )
            plt.pause(0.2)
            plt.bar( build_bins, self.In_true, width = 0.5,                                                                         # Graph_Input     :  In_minus_(Anti)Nu_true    (tau_minus)
                    edgecolor='green', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )
            plt.legend( fontsize=16 )
            plt.pause(0.5)
            #
            plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                    # Graph_Input     :  In_minus_(Anti)Nu_reco
            plt.legend( fontsize=16 )
            plt.pause(0.5)
            #
            plt.bar( build_bins, self.Calculed_reco, width = 0.5,                                                                   # Graph_Calculate :  vet_minus_(Anti)Nu_reco
                    edgecolor='green', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )
        
        elif self.type_tau == +1:                                                                                           # Tau_plus : ( Neutrino | AntiNeutrino )
            plt.pause(0.2)
            plt.bar( build_bins, self.In_true, width = 0.5,                                                                         # Graph_Input     :  In_plus_(Anti)Nu_true     (tau_plus)
                    edgecolor='darkorange', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )
            plt.legend( fontsize=16 )
            plt.pause(0.5)
            #
            plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                    # Graph_Input     :  In_plus_(Anti)Nu_reco
            plt.legend( fontsize=16 )
            plt.pause(0.5)
            #
            plt.bar( build_bins, self.Calculed_reco, width = 0.5,                                                                   # Graph_Calculate :  vet_plus_(Anti)Nu_reco
                    edgecolor='darkorange', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )


        plt.legend( fontsize=16 )                                                                                                # Add legend

        plt.pause(0.01)                                                                                                          # Displaying the graph and pausing execution

        input("Enter to continue: ")                                                                                             # Waiting for keyboard input to continue
        plt.close()                                                                                                              # Close image

        return


#
##     Graph_all_bar_UJ (Uniform and Joint))
#
# Class that graphs histograms with uniform bins and joints (bin_UJ means bin Uniform and Joint)
    # Note: This function draws all (all) the graphs in the article frame, i.e., neutrino mode will have tau_minus and tau_plus and so on.
class Graph_all_bar_UJ:
    _instance = None

    def __init__( self, histogram, In_true_minus, In_reco_minus, Calculed_reco_minus, In_true_plus, In_reco_plus, Calculed_reco_plus, type_neutrino ):
        self.histogram = histogram
        self.In_true_minus = In_true_minus
        self.In_reco_minus = In_reco_minus
        self.Calculed_reco_minus = Calculed_reco_minus
        self.In_true_plus = In_true_plus
        self.In_reco_plus = In_reco_plus
        self.Calculed_reco_plus = Calculed_reco_plus
        self.type_neutrino = type_neutrino
        #
        Graph_single_bar_UJ._instance = self    
    @classmethod
    def input_data(cls, in_histogram, in_In_true_minus, in_In_reco_minus, in_Calculed_reco_minus, in_In_true_plus, in_In_reco_plus, in_Calculed_reco_plus):
        setup_hist = cls( in_histogram, in_In_true_minus, in_In_reco_minus, in_Calculed_reco_minus, in_In_true_plus, in_In_reco_plus, in_Calculed_reco_plus, -1 )
        cls._instance = setup_hist 
        return cls._instance
    @classmethod
    def graph_change(cls, in_type_neutrino):
        if cls._instance is None:
            raise Exception(" No existing instance. Use get_input_Uniform(histgram, events_bin) first. ")
        else:
            if abs(in_type_neutrino) != +1:
                raise Exception(" choose : +1 for Antineutrino or -1 for Neutrino. ")
            else:
                cls._instance.type_neutrino = in_type_neutrino
                return cls._instance
    
    # Getting the plot
    def get_plot_bar(self):    
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
        ax.tick_params(axis='x', direction='in', pad =10, length=13)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad=10, length=13)                             # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=20)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm true/reco.} \ [GeV]$', fontdict={'size':25})                 # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/3.5 \ yr}$', fontdict={'size':25}, labelpad=7)      # Add label y-axis
        
        #
        ## Neutrino type
        #
        if self.type_neutrino == +1:                                                                       # Write on the frame - Neutrino type:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,40)

            plt.text(1, 34.3, 
                    r'$\bf{\tau^{-} \ events}$'
                ,fontsize=16, color='green', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.45'))
            #
            plt.text(4.7, 34.3, 
                        r'$\bf{\tau^{+} \ events}$'
                    ,fontsize=16, color='darkorange', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.45'))
            
            plt.text(0.3, 37, f'Neutrino mode', fontsize=35, color='blue')
        
        #
        ## Antineutrino type
        #
        elif self.type_neutrino == -1:                                                                       # Write on the frame - AntiNeutrino type:
            plt.xlim(0,20)                                                                                      # Axis limit
            plt.ylim(0,40/2)

            plt.text(1, 34.3/2, 
                    r'$\bf{\tau^{-} \ events}$'
                ,fontsize=16, color='green', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.45'))
            #
            plt.text(4.7, 34.3/2, 
                        r'$\bf{\tau^{+} \ events}$'
                    ,fontsize=16, color='darkorange', 
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.45'))
            
            plt.text(0.3, 37/2, f'Antineutrino mode', fontsize=35, color='blue')
        
        #
        ## If it is not a Neutrino or Antineutrino type
        #
        else:                                                                                              # If it is not a Neutrino or Antineutrino type
            raise Exception(" choose : +1 for Antineutrino or -1 for Neutrino. ")
            
        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.histogram.bins ]                                          # Defined in the library histogram_unif.py

        #
        ##   Neutrino Mode
        #
        if self.type_neutrino == +1:                                                                                             # Neutrino type:
            # Tau_minus : Neutrino                                                                                               # Tau_minus : Neutrino 
            plt.bar( build_bins, self.In_true_minus, width = 0.5,                                                                         # Graph_Input     :  In_minus_Nu_true    (tau_minus) 
                    edgecolor='green', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )
            plt.legend( fontsize=16 )
            #
            plt.scatter( build_bins, self.In_reco_minus, color='black', label='Input: data reconst.' )                                    # Graph_Input     :  In_minus_Nu_reco
            plt.legend( fontsize=16 )
            #
            plt.bar( build_bins, self.Calculed_reco_minus, width = 0.5,                                                                   # Graph_Calculate :  vet_minus_Nu_reco
                    edgecolor='green', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )
        
            # Tau_plus : Neutrino                                                                                                # Tau_plus  : Neutrino
            plt.bar( build_bins, self.In_true_plus, width = 0.5,                                                                          # Graph_Input     :  In_plus_Nu_true     (tau_plus)
                    edgecolor='darkorange', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )
            plt.legend( fontsize=16 )
            #
            plt.scatter( build_bins, self.In_reco_plus, color='black' )                                                                   # Graph_Input     :  In_plus_Nu_reco
            #plt.legend( fontsize=16 )
            #
            plt.bar( build_bins, self.Calculed_reco_plus, width = 0.5,                                                                    # Graph_Calculate :  vet_plus_Nu_reco
                    edgecolor='darkorange', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )
        
        #
        ##   Antineutrino Mode
        #
        else:                                                                                                                    # AntiNeutrino type:
            # Tau_minus : Antineutrino                                                                                           # Tau_minus : AntiNeutrino
            plt.bar( build_bins, self.In_true_minus, width = 0.5,                                                                         # Graph_Input     :  In_minus_AntiNu_true     (tau_minus)
                    edgecolor='green', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )
            plt.legend( fontsize=16 )
            #
            plt.scatter( build_bins, self.In_reco_minus, color='black', label='Input: data reconst.' )                                    # Graph_Input     :  In_minus_AntiNu_reco
            plt.legend( fontsize=16 )
            #
            plt.bar( build_bins, self.Calculed_reco_minus, width = 0.5,                                                                   # Graph_Calculate :  vet_minus_AntiNu_reco
                    edgecolor='green', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )
        
            # Tau_plus : Antineutrino                                                                                            # Tau_plus : AntiNeutrino
            plt.bar( build_bins, self.In_true_plus, width = 0.5,                                                                          # Graph_Input     :  In_plus_AntiNu_true      (tau_plus)
                    edgecolor='darkorange', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )
            plt.legend( fontsize=16 )
            #
            plt.scatter( build_bins, self.In_reco_plus, color='black' )                                                                   # Graph_Input     :  In_plus_AntiNu_reco
            #plt.legend( fontsize=16 )
            #
            plt.bar( build_bins, self.Calculed_reco_plus, width = 0.5,                                                                    # Graph_Calculate :  vet_plus_AntiNu_reco
                    edgecolor='darkorange', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )


        plt.legend( fontsize=16 )                                                                                                # Add legend

        plt.pause(0.01)                                                                                                          # Displaying the graph and pausing execution

        input("Enter to continue: ")                                                                                             # Waiting for keyboard input to continue
        plt.close()                                                                                                              # Close image

        return


#
##     Graph_HE_bar_UJ 
#
# Class that graphs histograms with uniform bins and joints (bin_UJ means bin Uniform and Joint)
    # Note: This function draws one type of graph: High energy (HE) mode for tau_minus.
class Graph_HE_bar_UJ:
    def __init__( self, histogram, In_true, In_reco, Calculed_reco ):
        self.histogram = histogram
        self.In_true = In_true
        self.In_reco = In_reco
        self.Calculed_reco = Calculed_reco
    @classmethod
    def input_data(cls, in_histogram, in_In_true, in_In_reco, in_Calculed_reco):
        setup_hist = cls( in_histogram, in_In_true, in_In_reco, in_Calculed_reco ) 
        return setup_hist
    
    # Getting the plot
    def get_plot_bar(self):    
        """ 
            Creating the frame 
        """
        plt.figure( figsize=(13, 10) )                                                          # Creates the figure with a customized proportion

        plt.xlim(0,20)                                                                          # Axis limit
        plt.ylim(0,40/2)

        # Adjust the edges of the frame
        plt.gca().spines['top'].set_linewidth(4)                                                # Top edge
        plt.gca().spines['right'].set_linewidth(4)                                              # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'].set_linewidth(4)                                               # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x', direction='in', pad =10, length=13)                            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad=10, length=13)                             # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=20)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm true/reco.} \ [GeV]$', fontdict={'size':25})                 # Add label x-axis
        plt.ylabel(r'${\rm N_{evt.}\,/bin\,/yr}$', fontdict={'size':25}, labelpad=7)            # Add label y-axis

        plt.text(11, 27.2/2,                                                                    # Write on the frame: All
                    r'$\bf{\tau^{-} \ events:\ {\rm neutrino \ mode \ \ \:}}$'
                    f"            "
                ,fontsize=16, color='green', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            
            
        plt.text(0.3, 37/2, f'High energymode', fontsize=35, color='blue')
            
        plt.text(11, 20/2,
                    r'$\bf{\qquad types}\qquad$'   r'$\bf{\qquad\qquad \ \ total/1.0 \ yr }$' 
                    f"\n"
                    f"Input: data true                    {round( 0.5*sum( self.In_true ), 2)}\n"
                    f"Input: data reconst.              {round( 0.5*sum( self.In_reco ), 2)}\n"
                    f"Calc.: data reconst.              {round( 0.5*sum( self.Calculed_reco ), 2)}"
                ,fontsize=16, color='blue', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

        """ 
            Creating the Plot 
        """
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.histogram.bins ]                                          # Defined in the library histogram_unif.py
    
        # Tau_minus : High energy                                                                                           # Tau_minus : High energy
        plt.pause(0.2)
        plt.bar( build_bins, self.In_true, width = 0.5,                                                                            # Graph_Input     :  In_minus_(Anti)Nu_true    (tau_minus) 
                edgecolor='green', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )
        plt.legend( fontsize=16 )
        plt.pause(0.5)
        #
        plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                       # Graph_Input     :  In_minus_(Anti)Nu_reco
        plt.legend( fontsize=16 )
        plt.pause(0.5)
        #
        plt.bar( build_bins, self.Calculed_reco, width = 0.5,                                                                      # Graph_Calculate :  vet_minus_(Anti)Nu_reco
                edgecolor='green', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )
            

        plt.legend( fontsize=16 )                                                                                                # Add legend

        plt.pause(0.01)                                                                                                          # Displaying the graph and pausing execution

        input("Enter to continue: ")                                                                                             # Waiting for keyboard input to continue
        plt.close()                                                                                                              # Close image

        return

