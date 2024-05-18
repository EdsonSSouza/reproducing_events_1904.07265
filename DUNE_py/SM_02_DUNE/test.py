import numpy as np
from Init_00_tau.read_vec     import *
from Init_00_tau.rules_reco   import Rule_smear
from Init_00_tau.histogram    import Histogram
from SM_01_Prob.mass_order    import Mass_order
from SM_01_Prob.matrix_PMNS   import Matrix_Osc
from SM_01_Prob.hamilton_mass import Hamilton_matrix
from SM_01_Prob.s_matrix_mass import S_matrix
from SM_01_Prob.prob_SM       import Probability_SM
from NSI_01_Prob.matrix_NSI   import Matrix_Tmut
from NSI_01_Prob.prob_NSI     import Probability_NSI

#print(sum(In_MNu_true_Nu))
#print(sum(In_MNu_reco_Nu))
#print(sum(Pre_cal_MNu_Nu))
print(sum(In_MNu_true_Nu)/sum(In_pre_MNu_Nu))

print()
hist = Histogram.get_Uniform_WB(0, 20, 0.5)
my_data_true = [10*i for i in In_MNu_true_Nu]
vec_true_1, vec_reco_1, norm = Rule_smear.input_data(hist, my_data_true).get_middle()
my_norm = sum( my_data_true )/sum(vec_reco_1)
print(my_norm)
print(norm)
print( sum( my_data_true )/sum([norm*vec for vec in vec_reco_1]) )


print()
hist = Histogram.get_Uniform_WB(0, 20, 0.5)
my_data_true = [1*i for i in In_MAn_true_Nu]
vec_true_1, vec_reco_1, norm = Rule_smear.input_data(hist, my_data_true).get_middle()
my_norm = sum( my_data_true )/sum(vec_reco_1)
print(my_norm)
print(norm)
print( sum( my_data_true )/sum([norm*vec for vec in vec_reco_1]) )


print()
hist = Histogram.get_Uniform_WB(0, 20, 0.5)
my_data_true = np.zeros(len(In_MNu_true_Nu))
for i in range( len(In_MNu_true_Nu) ):
    if i < 10:
        my_data_true[i] = 700.3*In_MNu_true_Nu[i]
    elif 10 <= i < 20:
        my_data_true[i] = 10.1*In_MNu_true_Nu[i]
    elif 20 <= i < 30:
        my_data_true[i] = 2.1*In_MNu_true_Nu[i]
    else:
        my_data_true[i] = 3.1*In_MNu_true_Nu[i]

vec_true_1, vec_reco_1, norm = Rule_smear.input_data(hist, my_data_true).get_middle()
my_norm = sum( my_data_true )/sum(vec_reco_1)
print(my_norm)
print(norm)
print( sum( my_data_true )/sum([norm*vec for vec in vec_reco_1]) )

