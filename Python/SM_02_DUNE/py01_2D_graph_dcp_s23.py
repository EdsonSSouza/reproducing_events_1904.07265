###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				17th Mar 2024	                  #####
###########################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline as RBS_interp2d

# Import our libraries
from lib_fit2D_read import *


class Organization_2D:
    def __init__(self, arrays) -> None:
        self.vectors = arrays
    
    def get_data( self ):
        num_loop = 2

        col1 = self.vectors[0]
        col2 = self.vectors[1]
        chi2 = self.vectors[2]

        number = int( len( chi2 )**(1/num_loop) )
        vec_col1 = np.zeros( number )
        vec_col2 = np.zeros( number )
        matrix_chi2 = np.zeros( ( number , number ) )

        for i in range( number ):
            vec_col1[i] = col1[i*number]
            vec_col2[i] = col2[i]
        
        for i in range( number ):
            for j in range( number ):
                matrix_chi2[i][j] = chi2[i*number + j]
        
        return vec_col1, vec_col2, matrix_chi2



class Graph_fit2D:
    def __init__(self, arrays_data ) -> None:
        self.vectors = arrays_data
    @classmethod
    def input( cls, arrays_data ):
        return cls( arrays_data )
    

    def get_dcp_s23( self ):
        vec_chi2 = self.vectors[2]                                               # Calling the vector chi2
        min_chi2 = min( vec_chi2 )                                               # chi2_min : minimum in chi2
        pos = np.where( vec_chi2 == min_chi2 )                                   # Find the position of the value in the array
    
        vectors = Organization_2D( self.vectors ).get_data()
        col1 = vectors[0]
        col2 = vectors[1]
        matrix_chi2 = vectors[2]
        
        number = int( len( col1 ) )
        matrix_DifChi2 = np.zeros( ( number, number) )
        for i in range( number ):
            for j in range( number ):
                matrix_DifChi2[i][j] = matrix_chi2[i][j] - min_chi2              # Matrix ( chi2 - chi2_min )

        interp_chi2 = RBS_interp2d( col1, col2, matrix_DifChi2 )                 # Interpolation : col1 x col2 x (chi2 - chi2_min)

        # Start plot
        plt.figure( figsize=(12, 10) )                                                          # Creates the figure with a customized proportion
        
        plt.xlim( -1, 1 )                                                                       # Axis limit 
        plt.ylim( 0, 1 )
        plt.subplots_adjust(left=0.15, right=0.96, bottom=0.13, top=0.96)#, wspace=0.4, hspace=0.4)

        # Adjust the edges of the frame
        plt.gca().spines['top'].set_linewidth(4)                                                # Top edge
        plt.gca().spines['right'].set_linewidth(4)                                              # Right edge
        plt.gca().spines['bottom'].set_linewidth(4)                                             # Bottom edge
        plt.gca().spines['left'].set_linewidth(4)                                               # left edge

        ax = plt.gca()                                                                          # Getting the current axes and setting the scale markers / scale numbers
        ax.tick_params(axis='x',    direction='in', pad = 11, length=12)                        # For x-axis markers
        ax.tick_params(axis='y',    direction='in', pad = 11, length=12)                        # For y-axis markers
        ax.tick_params(axis='both', which='major', width=3.5, labelsize=24)                     # For the main numbers: 'major' / 'minor' / 'both'

        # Specifying the values that will appear on the x and y axes
        plt.xticks([-1, -0.5, 0, 0.5, 1])                                                       # Only the values -1, -0.5, 0, 0.5, 1 will be shown on the x-axis
        plt.yticks([0, 0.25, 0.5, 0.685, 0.75, 1])                                                     # Only the values 0, 0.25, 0.5, 0.75, 1 will be shown on the y-axis

        plt.xlabel(r'${\delta_{\rm CP}/\pi}$', fontdict={'size':34}, labelpad=9)                # Add label x-axis
        plt.ylabel(r'${\sin^{2}\theta_{23}}$', fontdict={'size':34}, labelpad=9)                # Add label y-axis
        
        plt.grid('true')                                                                        # Grid: true


        # Setup: grid data
        x_values = np.linspace(col1[0], col1[int(len(col1))-1], 400)
        y_values = np.linspace(col2[0], col2[int(len(col2))-1], 400)
        axis_X, axis_Y = np.meshgrid(y_values, x_values)

        # Plot Contour:
        contour1 = plt.contour( axis_Y, axis_X, interp_chi2(x_values, y_values), levels=[2.30], colors='darkgreen', linewidths=2.5, linestyles='dashed' )    # 1 sigma ( k = 2 : 2.30 )
        contour2 = plt.contour( axis_Y, axis_X, interp_chi2(x_values, y_values), levels=[11.83], colors='darkgreen', linewidths=2.5 )                        # 3 sigma ( k = 2 : 11.83 )
        
        # Plot Region:
        plt.contourf( axis_Y, axis_X, interp_chi2(x_values, y_values), levels=[-0.1, 2.300], colors='green', alpha=0.6 )                                     # 1 sigma ( k = 2 : 2.30 )
        plt.contourf( axis_Y, axis_X, interp_chi2(x_values, y_values), levels=[2.30, 11.83], colors='green', alpha=0.3 )                                     # 3 sigma ( k = 2 : 11.83 )
        
        # Plot Best-Fit:
        bf_x, bf_y = self.vectors[0], self.vectors[1]
        point_1 = pos[0][0]
        plt.plot( bf_x[point_1], bf_y[point_1],  marker='o', color='black', markersize=10 )
        point_2 = pos[0][1]
        plt.plot( bf_x[point_2], bf_y[point_2],  marker='o', color='black', markersize=10 )

        # Legend:
        plt.legend( [ contour1.collections[0], contour2.collections[0], plt.Line2D( [0],[0], marker='o', color='black', markersize=10 ) ],\
                    [ r'${1 \ \sigma}$', r'${3 \ \sigma}$', 'Best-Fit' ], handlelength=1.6, loc='upper right', fontsize=24, frameon=True ) 

        
        plt.pause(0.01)                                                                         # Displaying the graph and pausing execution
        input("Enter to continue: ")                                                            # Waiting for keyboard input to continue
        plt.close()

        return None



if __name__ == "__main__":
    
    show = 1

    if show ==1:
        graph_dcp_s23 = Graph_fit2D.input(In_dcp_s23).get_dcp_s23()
        print( graph_dcp_s23 )

