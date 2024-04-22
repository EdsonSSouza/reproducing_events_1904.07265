from Init_00_tau.histogram import Histogram
from Init_00_tau.read_vec import *
from Init_00_tau.migrate import Gaussian_interp2D
from Init_00_tau.rules_reco import Rule_smear
from Init_00_tau.graphic_bar import Graph_all
from SM_01_Prob.prob_SM import Probability_SM
from SM_01_Prob.mass_order import Mass_order
from SM_01_Prob.matrix_PMNS import Matrix_Osc
import numpy as np


hist = Histogram.get_Uniform_WB(0, 20, 0.5)
print([bin.left for bin in hist.bins])
print(np.shape(In_matrix_pre_40x40))

energy = np.linspace(0, 20, 401)
map_gau = Gaussian_interp2D.input_data(energy).get_function2D()
print(map_gau(5,8)[0][0])


Calc_reco_Nu   = Rule_smear.input_data( hist, In_MNu_true_Nu   ).get_5to5_pre()
Calc_reco_Anti = Rule_smear.input_data( hist, In_MNu_true_Anti ).get_5to5()

print(f"\n{Calc_reco_Nu}\n{Calc_reco_Anti}")

graph = Graph_all.input_data( +1, hist, In_MNu_true_Nu, Calc_reco_Nu, In_MNu_true_Anti, Calc_reco_Anti ).get_plot_bar()

PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, 1.204225*np.pi )
mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )
prob_SM = Probability_SM.input_data( +1, 0.01, 1300, PMNS, mass, 2.848 ).get_osc_SM()
print(prob_SM)

