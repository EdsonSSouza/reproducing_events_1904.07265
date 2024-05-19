###########################################################
##### 				created by:						  ##### 
#####                                                 #####
#####				Edson Souza 					  #####
#####		https://inspirehep.net/authors/2722580	  #####
##### 												  ##### 
##### 				creation date					  ##### 
##### 				23th April 2024	                  #####
###########################################################

import numpy as np
import matplotlib.pyplot as plt

# Import our libraries
from SM_01_Prob.mass_order  import Mass_order
from SM_01_Prob.matrix_PMNS import Matrix_Osc
from SM_01_Prob.prob_SM     import Probability_SM


PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.523176, 1.204225*np.pi )
mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
prob_mut = Probability_SM.input_data( +1, 0.01, 1300, PMNS, mass, 2.848 ).get_osc_SM()[1][2]

def ProbInf_mut( energy ):
    PMNS_i = Matrix_Osc.input_data( 0.310, 0.00001, 0.5, 0.0*np.pi )
    mass_i = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
    return [ Probability_SM.input_data( +1, en, 1300, PMNS_i, mass_i, 2.848 ).get_osc_SM()[1][2]    for en in energy ]

def Prob_BF( energy ):
    PMNS_i = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, 0.0*np.pi )
    mass_i = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
    return [ Probability_SM.input_data( +1, en, 1300, PMNS_i, mass_i, 2.848 ).get_osc_SM()[1][2]    for en in energy ]

def ProbSup_mut( energy ):
    PMNS_i = Matrix_Osc.input_data( 0.310, 0.02240, 0.154738, 0.0*np.pi )
    mass_i = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
    return [ Probability_SM.input_data( +1, en, 1300, PMNS_i, mass_i, 2.848 ).get_osc_SM()[1][2]    for en in energy ]


# Creates the figure with a customized proportion
plt.figure(figsize=(14, 12))
# Adjust the edges of the frame
plt.gca().spines['top'].set_linewidth(4)                                                    # Top edge
plt.gca().spines['right'].set_linewidth(4)                                                  # Right edge
plt.gca().spines['bottom'].set_linewidth(4)                                                 # Bottom edge
plt.gca().spines['left'].set_linewidth(4)                                                   # left edge

# Getting the current axes and setting the scale markers / scale numbers
ax = plt.gca()
ax.tick_params(axis='x', direction='in', pad=12, length=24, bottom=True, top=True)          # For x-axis markers
ax.tick_params(axis='y', direction='in', pad=12, length=24, left=True, right=True)          # For y-axis markers
ax.tick_params(axis='both', which='major', width=2.8, labelsize=25)                         # For the main numbers: 'major' / 'minor' / 'both'

# Specifying the values that will appear on the x and y axes
plt.xticks([0, 2, 4, 6, 8, 10])                                                             # Only the values 0, 2, 4, ... , 10 will be shown on the x-axis
plt.yticks([0, 0.25, 0.5, 0.75, 1])                                                         # Only the values 0, 0.25, 0.5, ... , 1 will be shown on the y-axis

plt.xlim(0,10)                                                                              # Axis limit
plt.ylim(0,1)
plt.xlabel( r'${\rm E}_{\nu} \ [{\rm GeV}]$', fontsize=27 )
plt.ylabel( r'${\rm P}\left(\nu_\mu \ \rightarrow \ \nu_\tau\right)$', fontsize=27, labelpad=8 )
plt.text( 5.5, 0.8, r'$0.5\: <\: \sin^{2}\left(2\theta_{\mu\tau}\right)\: <\: 1$', color='black', fontsize=24 )
plt.text( 2.85, 0.034, r'$E_{\nu} < E_{\tau}^{\rm threshold}$', color='black', fontsize=30, rotation=90 )

en = np.linspace(0.5,10.5,501)
plt.plot(en, ProbInf_mut(en), color='black', linewidth=6)
plt.plot(en, Prob_BF(en), color='blue', linewidth=2, linestyle='--')
plt.plot(en, ProbSup_mut(en), color='black', linewidth=6)


plt.fill_between(en, ProbInf_mut(en), ProbSup_mut(en), color='gray', alpha=0.6)             # Filling in the area between the plots
plt.plot([3.35,3.35], [0,1], color='blue', linewidth=3.5, alpha=0.3)
plt.fill_between([0, 3.35], [0, 0], [1, 1], color='blue', alpha=0.17)                       # Filling in the rectangular boundary area

# Displaying the graph and pausing execution
plt.pause(0.01)

#plt.savefig('../Image_article/Fig4_Prob_SM.pdf', format='pdf')                              # Save with .pdf

# Waiting for keyboard input to continue
input("Enter to continue: ")
plt.close()

