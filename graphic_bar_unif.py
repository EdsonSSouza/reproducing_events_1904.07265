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


# Class that graphs histograms with uniform bins and joints (bin_UJ means bin Uniform and Joint)
class Graph_single_bar_UJ:
    # Note: This function draws one frame of the article at a time, i.e. neutrino mode for tau_minus or tau_plus and so on.
    _instance = None

    def __init__( self, histogram, In_true, In_reco, Calculed_reco, type_tau, type_neutrino ):
        self.histogram = histogram
        self.In_true = In_true
        self.In_reco = In_reco
        self.Calculed_reco = Calculed_reco
        self.type_tau = type_tau
        self.type_neutrino = type_neutrino
        #
        Graph_single_bar_UJ._instance = self
    
    @classmethod
    def input_data(cls, in_histogram, in_In_true, in_In_reco, in_Calculed_reco):
        setup_hist = cls( in_histogram, in_In_true, in_In_reco, in_Calculed_reco, -1, -1 )
        cls._instance = setup_hist 
        return cls._instance
    @classmethod
    def graph_change(cls, in_type_tau, in_type_neutrino):
        if cls._instance is None:
            raise Exception(" No existing instance. Use get_input_Uniform(histgram, events_bin) first. ")
        else:
            if abs(in_type_tau) != +1:
                raise Exception(" choose : +1 for Tau_plus or -1 for Tau_minus. ")
            elif abs(in_type_neutrino) != +1:
                raise Exception(" choose : +1 for Antineutrino or -1 for Neutrino. ")
            else:
                cls._instance.type_tau = in_type_tau
                cls._instance.type_neutrino = in_type_neutrino
                return cls._instance
    


    def plot_bar(self):    
        # Execute the histogram: set in the center
        build_bins = [ (bin.left + bin.right)/2   for bin in self.histogram.bins ] # Defined in the library histogram_unif.py

        """ 
            Creating the frame 
        """
        # Creates the figure with a customized proportion
        plt.figure( figsize=(13, 10) )

        # Limit axis
        plt.xlim(0,20)
        plt.ylim(0,40)

        # Adjust the edges of the frame
        plt.gca().spines['top'].set_linewidth(4)     # Top edge
        plt.gca().spines['right'].set_linewidth(4)   # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)  # Bottom edge
        plt.gca().spines['left'].set_linewidth(4)    # left edge

        # Getting the current axes and setting the scale markers / scale numbers
        ax = plt.gca()
        ax.tick_params(axis='x', direction='in', pad =10, length=13)            # For x-axis markers
        ax.tick_params(axis='y', direction='in', pad=10, length=13)             # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=20)     # For the main numbers: 'major' / 'minor' / 'both'

        # Add label and title (plt.title())
        plt.xlabel(r'$E_{\nu}^{\rm true/reco.} \ [GeV]$', fontdict={'size':25})
        plt.ylabel(r'${\rm N_{evt.}/bin/3.5 \ yr}$', fontdict={'size':25}, labelpad=7)


        # Write on the frame:
        
        #
        ## Neutrino type
        #
        if self.type_neutrino == -1:
            #
            if self.type_tau == -1:
                #
                ##   Tau_minus : Neutrino
                #
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{-} \ events:\ {\rm neutrino \ mode}}$'
                            f"           "
                        ,fontsize=16, color='green', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            elif self.type_tau == +1:
                #
                ##   Tau_plus : Neutrino
                #
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{+} \ events:\ {\rm neutrino \ mode}}$'
                            f"           "
                        ,fontsize=16, color='darkorange', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            else:
                raise Exception(" choose : +1 for tau_plus or -1 for tau_minus. ")
            
            plt.text(0.3, 37, f'Neutrino mode', fontsize=35)
        
        #
        ## Antineutrino type
        #
        elif self.type_neutrino == +1:
            #
            if self.type_tau == -1:
                #
                ##   Tau_minus : Antineutrino
                #
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{-} \ events:\ {\rm antineutrino \ mode}}$'
                            f"           "
                        ,fontsize=16, color='green', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            elif self.type_tau == +1:
                #
                ##   Tau_plus : Antieutrino
                #
                plt.text(11, 27.2, 
                            r'$\bf{\tau^{+} \ events:\ {\rm antineutrino \ mode}}$'
                            f"           "
                        ,fontsize=16, color='darkorange', 
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
            #
            else:
                raise Exception(" choose : +1 for tau_plus or -1 for tau_minus. ")
            
            plt.text(0.3, 37, f'Antineutrino mode', fontsize=35)
        
        #
        ## If it is not a Neutrino or Antineutrino type
        #
        else:
            raise Exception(" choose : +1 for Antineutrino or -1 for Neutrino. ")
            
        plt.text(11, 20,
                    r'$\bf{\qquad types}\qquad$'   r'$\bf{\qquad\qquad\qquad \ \ total}$' 
                    f"\n"
                    f"Events data_in true            {round(sum( self.In_true ),2)}\n"
                    f"Events data_in reconst.      {round(sum( self.In_reco ),2)}\n"
                    f"Events data_cal reconst.    {round(sum( self.Calculed_reco ),2)}"
                ,fontsize=16, color='blue', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))



        """ 
            Creating the Plot 
        """
    
        if self.type_tau == -1:
            #
            ##   Tau_minus : Neutrino
            #
            plt.pause(1)
            plt.bar( build_bins, self.In_true, width = 0.5, 
                    edgecolor='green', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )          # Graph_Input      :  In_minus_(Anti)Nu_true      (tau_minus)
            plt.legend( fontsize=16 )
            plt.pause(2)
            #
            plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                # Graph_Input      :  In_minus_(Anti)Nu_reco
            plt.legend( fontsize=16 )
            plt.pause(2)
            #
            plt.bar( build_bins, self.Calculed_reco, width = 0.5, 
                    edgecolor='green', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )                     # Graph_Calculate  :  vet_minus_(Anti)Nu_reco
        
        elif self.type_tau == +1:
            #
            ##   Tau_plus : Neutrino
            #
            plt.pause(1)
            plt.bar( build_bins, self.In_true, width = 0.5, 
                    edgecolor='darkorange', facecolor='none', linestyle='dotted', linewidth=1.8, label='Input: data true' )     # Graph_Input      :  In_plus_(Anti)Nu_true       (tau_plus)
            plt.legend( fontsize=16 )
            plt.pause(2)
            #
            plt.scatter( build_bins, self.In_reco, color='black', label='Input: data reconst.' )                                # Graph_Input      :  In_plus_(Anti)Nu_reco
            plt.legend( fontsize=16 )
            plt.pause(2)
            #
            plt.bar( build_bins, self.Calculed_reco, width = 0.5, 
                    edgecolor='darkorange', facecolor='none', linewidth=2.0, label='Calculated: data reconst.' )                # Graph_Calculate  :  vet_plus_(Anti)Nu_reco


        # Add legend
        plt.legend( fontsize=16 )

        # Displaying the graph and pausing execution
        plt.pause(0.01)

        # Waiting for keyboard input to continue
        input("Enter to continue: ")
        plt.close()

        return

  