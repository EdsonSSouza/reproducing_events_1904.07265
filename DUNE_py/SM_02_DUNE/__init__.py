"""
       -- SM_02_DUNE -- 

Library for describing new events in DUNE for the SM scenario in the distant detector using __init__.py:
       chi2_BC; new_events_SM; sensitivity; etc
"""

# creation date May 19, 2024
__version__ = "1.0.0"
__author__  = 'Edson Souza'
__credits__ = 'https://inspirehep.net/authors/2722580'


from SM_02_DUNE.py00_chi2BC_SM     import Chi2BC, Chi2BC_331
from SM_02_DUNE.py00_new_events_SM import Prob_ration_SM, NewEvent_true_SM, NewEvent_reco_SM

