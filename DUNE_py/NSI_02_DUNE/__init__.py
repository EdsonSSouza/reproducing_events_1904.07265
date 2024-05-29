"""
       -- NSI_02_DUNE -- 

Library for describing new events in DUNE for the NSI scenario in the distant detector using __init__.py:
       chi2BC_NSI; new_events_NSI; sensitivity_NSI; etc
"""

# creation date May 19, 2024
__version__ = "1.0.0"
__author__  = 'Edson Souza'
__credits__ = 'https://inspirehep.net/authors/2722580'


from NSI_02_DUNE.py0_chi2BC_NSI     import Chi2BC_NSI, Chi2BC_331_NSI
from NSI_02_DUNE.py0_new_events_NSI import Prob_ratio_NSI, NewEvent_true_NSI, NewEvent_reco_NSI

