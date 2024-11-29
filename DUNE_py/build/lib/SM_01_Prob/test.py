import numpy as np
from Init_00_tau.read_vec    import *
from Init_00_tau.histogram   import Histogram
from Init_00_tau.migrate     import Gaussian_interp2D
from Init_00_tau.rules_reco  import Rule_smear
from Init_00_tau.graphic_bar import Graph_all, Graph_HE_comp


hist = Histogram.get_Uniform_WB(0,20,0.5)
print( f"\n{ [(ibin.left, ibin.right)   for ibin in hist.bins] }" )

print( f"\n{In_pre_MHE_Nu}\n" )

energy = np.linspace(0,20,401)
gau_interp = Gaussian_interp2D.input_data( energy ).get_function2D()
print( f"{gau_interp(4.37, 7.35)}\n" )

In_begin = In_MNu_true_Nu
In_Norm  = Norm5x5_MNu_Nu
In_data  = In_pre_MNu_Nu
Ev_reco  = Rule_smear.input_data( hist, In_begin ).get_5to5( In_Norm )
for i in range(len(In_begin)): print( f"{In_data[i]} \t {Ev_reco[i]} \t\t {round( abs(In_data[i]-Ev_reco[i]), 3 )}" )

Cal_Mnu_reco_Nu   = Rule_smear.input_data( hist, In_MNu_true_Nu   ).get_5to5_pre( Norm5x5_MNu_Nu )
Cal_MAn_reco_Anti = Rule_smear.input_data( hist, In_MAn_true_Anti ).get_5to5_pre( Norm5x5_MAn_Anti )
graph = Graph_all.input_data( +1, hist, In_MNu_true_Nu, Cal_Mnu_reco_Nu, In_MAn_true_Anti, Cal_MAn_reco_Anti ).get_plot_bar(40, [0, 10, 20, 30, 40])
print()

graph_comp = Graph_HE_comp.input_data( hist, Cal_MAn_reco_Anti ).get_plot_bar(25, [0, 5, 10, 15, 20, 25])
print()

