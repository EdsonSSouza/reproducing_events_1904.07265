"""
       -- Init_00_tau -- 

Functions to describe article 1904.07265 using __init__.py:
       Graphs; Sensitivity; Data collection; etc
"""

# creation date May 18, 2024
__version__ = "1.0.0"
__author__  = 'Edson Souza'
__credits__ = 'https://inspirehep.net/authors/2722580'


from Init_00_tau.read_vec     import *
from Init_00_tau.histogram    import Histogram
from Init_00_tau.migrate      import Gaussian_interp2D, Mapping_matrix
from Init_00_tau.rules_reco   import Rule_smear
from Init_00_tau.graphic_part import Graph_each, Graph_each_HE
from Init_00_tau.graphic_bar  import Graph_all , Graph_all_comp, Graph_HE     , Graph_HE_comp
from Init_00_tau.graphic_fill import Graph_fill, Graph_fill_Cp , Graph_fill_HE, Graph_fill_Cp_HE

