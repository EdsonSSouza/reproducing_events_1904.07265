from SM_01_Prob.mass_order import Mass_order
from SM_01_Prob.matrix_PMNS import Matrix_Osc
from SM_01_Prob.hamilton_mass import Hamilton_matrix
from SM_01_Prob.s_matrix_mass import S_matrix
from SM_01_Prob.prob_SM import Probability_SM
from NSI_01_Prob.matrix_NSI import Matrix_Tmut
from NSI_01_Prob.prob_NSI import Probability_NSI
import numpy as np


mass_print = Mass_order.input_data( 7.20e-5, 3.3e-3 ).get_ordering()
print(mass_print)

PMNS_print = Matrix_Osc.input_data( 0.31, 0.021, 0.56, 0.7*np.pi ).get_U()
print(PMNS_print)

PMNS = Matrix_Osc.input_data( 0.310, 0.02240, 0.582, 1.204225*np.pi )
mass = Mass_order.input_data( 7.39*1e-5, 2.525*1e-3 )

ham  = Hamilton_matrix.input_data( +1, 2.1, 2, PMNS, mass ).get_base_mass()
s_mat = S_matrix.input_data( +1, 2.1, 1300, 2.848, PMNS, mass ).get_S_bm()
prob_SM = Probability_SM.input_data( +1, 0.01, 1300, PMNS, mass, 2.848 ).get_osc_SM()
print(ham)
print(s_mat)
print(f"\n{prob_SM}")

Tmut = Matrix_Tmut.input_data( 1e-3, 1.0*np.pi )
prob_NSI = Probability_NSI.input_data(+1, 0.01, 1300, PMNS, Tmut, mass, 2.848 ).get_osc_NSI()
print(prob_NSI)

