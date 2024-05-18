"""
       -- Init_00_tau -- 

Functions to describe article 1904.07265 using __init__.py:
       Graphs; Sensitivity; Data collection; ect
"""

# creation date 20 APRIl 2024
__version__ = "1.0.0"
__author__  = 'Edson Souza'
__credits__ = 'https://inspirehep.net/authors/2722580'

from .read_vec     import *
from .histogram    import Histogram
from .migrate      import Gaussian_interp2D, Mapping_matrix
from .graphic_part import Graph_each, Graph_each_HE
from .graphic_bar  import Graph_all , Graph_all_comp, Graph_HE     , Graph_HE_comp
from .graphic_fill import Graph_fill, Graph_fill_Cp , Graph_fill_HE, Graph_fill_Cp_HE
from .rules_reco   import Rule_smear

