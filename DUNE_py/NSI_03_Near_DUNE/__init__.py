"""
       -- NSI_03_Near_DUNE -- 

Library for describing new events in DUNE for the NSI scenario in the distant detector using __init__.py:
       chi2BC_NSI; new_events_NSI; sensitivity_NSI; etc
"""

# creation date May 23, 2024
__version__ = "1.0.0"
__author__  = 'Edson Souza'
__credits__ = 'https://inspirehep.net/authors/2722580'


from NSI_03_Near_DUNE.py0_chi2BC_NSI      import Chi2BC_Near_NSI, Chi2BC_331_Near_NSI
from NSI_03_Near_DUNE.py0_new_events_NSI  import Prob_Near_ratio_NSI, NewEvent_Near_true_NSI, NewEvent_Near_reco_NSI
from NSI_03_Near_DUNE.lib_Near_rules_reco import Rule_smear_Near

