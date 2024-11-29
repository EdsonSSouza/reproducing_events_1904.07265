"""
       -- SM_01_Prob -- 

Library to describe the probability oscillation (SM) of DUNE using __init__.py:
       mass_order; matrix_PMNS; hamilton_mass; s_matrix_mass; prob_SM
"""

# creation date May 18, 2024
__version__ = "1.0.0"
__author__  = 'Edson Souza'
__credits__ = 'https://inspirehep.net/authors/2722580'


from SM_01_Prob.mass_order    import Mass_order
from SM_01_Prob.matrix_PMNS   import Matrix_Osc
from SM_01_Prob.hamilton_mass import Hamilton_matrix
from SM_01_Prob.s_matrix_mass import S_matrix
from SM_01_Prob.prob_SM       import Probability_SM

