#Constants in Units of MeV

#  constante para o decaimento do mesons escalares  em leptons
#
#
import numpy as np
import sympy as spy

#Decay constants & Rad Corrections

GF=1.1663787e-11
ErrGF = 0.0000006e-11
SMvev = 1/np.sqrt(np.sqrt(2)*GF)
ErrSMvev = (1/((np.sqrt(np.sqrt(2)))*(GF)**(3/2)))*ErrGF
MW=80.379e3
ErrMW = 0.012e3

mrho = 775.26
Errmrho = 0.25
mZ = 91.1876e3
ErrmZ = 0.0021e3
alpha = 7.2973525693e-3
Erralpha = 0.0000000011e-3
C1 = 0
ErrC1 = 2.4
C3 = 0
ErrC3 = 10

#Meson K

fK=155.7
ErrfK=3
mK=493.677
ErrmK=0.013
Vus=0.2245
pVus = 0
ErrVus=0.0008
mu=2.16
Errmu=0.49
ms=93
Errms=11
c1K = -1.98
c2K = 4.3
c3K = -4.73
c4K = 0.22
ct2K = 7.84e-2

Errc1K = 0.5
Errc2K = np.sqrt(0.4**2+0.01**2)
Errc3K = np.sqrt(2.3**2+0.28**2)
Errc4K = 0.01
Errct2K = 0.07e-2

mesonK = (fK,ErrfK,mK,ErrmK,Vus,ErrVus,mu,Errmu,ms,Errms)

#Meson pi

fpi=130.2
Errfpi=1.2
mpi = 139.57061
Errmpi = 0.00024
Vud = 0.97420
pVud = 0
ErrVud = 0.00021
mu = 2.16
Errmu=0.49
md = 4.67
Errmd = 0.48
barmud = 2*3.45
Errbarmud = 2*0.55
c1Pi = -2.56
c2Pi = 5.2
c3Pi = -10.5
c4Pi = 1.69
ct2Pi = 0

Errc1Pi = 0.5
Errc2Pi = np.sqrt(0.4**2+0.01**2)
Errc3Pi = np.sqrt(2.3**2+0.53**2)
Errc4Pi = 0.07
Errct2Pi = 0

mesonpi = (fpi,Errfpi,mpi,Errmpi,Vud,ErrVud,mu,Errmu,md,Errmd)

#Meson D

fD=212.6
ErrfD=7
mD = 1869.65
ErrmD = 0.05
Vcd = 0.221
pVcd = -3.14098
ErrVcd = 0.004
#mc = 1.27e3
mc = ms*11.76
Errmc=0.02e3
md = 4.67
Errmd = 0.48

mesonD = (fD,ErrfD,mD,ErrmD,Vcd,ErrVcd,mc,Errmc,md,Errmd)

#Meson Ds

fDs=249.9
ErrfDs=5
mDs = 1968.34
ErrmDs = 0.07
Vcs = 0.987
pVcs = -0.0000324671
ErrVcs = 0.011
#mc = 1.27e3
mc = ms*11.76
Errmc=0.02e3
ms=93
Errms=11

mesonDs = (fDs,ErrfDs,mDs,ErrmDs,Vcs,ErrVcs,mc,Errmc,ms,Errms)

#Meson B

fB = 190.0
ErrfB = 1.3
mB = 5279.34
ErrmB = 0.12
Vub = 3.82e-3
pVub = -1.144
ErrVub = 0.24e-3
mu = 2.16
Errmu=0.49
mb = 4.18e3
Errmb= 0.03e3

mesonB = (fB,ErrfB,mB,ErrmB,Vub,ErrVub,mu,Errmu,mb,Errmb)

#PMNS
    
theta12 = np.arcsin(np.sqrt(0.307))
theta23 = np.arcsin(np.sqrt(0.545))
theta13 = np.arcsin(np.sqrt(2.18e-2))

x = spy.symbols('x')

Errtheta12 = spy.N((spy.diff(spy.asin(spy.sqrt(x)),x).subs(x,0.307))*0.013)
Errtheta23 = spy.N((spy.diff(spy.asin(spy.sqrt(x)),x).subs(x,0.545))*0.021)
Errtheta13 = spy.N((spy.diff(spy.asin(spy.sqrt(x)),x).subs(x,2.18e-2))*0.07e-2)

#Errtheta12 = spy.N((spy.diff(spy.asin(x),x).subs(x,spy.sqrt(0.307)))*0.013)
#Errtheta23 = spy.N((spy.diff(spy.asin(x),x).subs(x,spy.sqrt(0.545)))*0.021)
#Errtheta13 = spy.N((spy.diff(spy.asin(x),x).subs(x,spy.sqrt(2.18e-2)))*0.07e-2)

Angles = (theta12,theta23,theta13,Errtheta12,Errtheta23,Errtheta13)

def NumPMNS(delta,beta1,beta2):
    #theta12,theta13,theta23,delta,beta1,beta2 = spy.symbols('x y z w u v')
    
    U1=[[1, 0, 0], [0, np.cos(theta23), np.sin(theta23)], [0, -np.sin(theta23), 
     np.cos(theta23)]]
    U2=[[np.cos(theta13), 0, 
     np.sin(theta13)*np.exp(-delta*1j)], [0, 1, 
     0], [-np.sin(theta13)*np.exp(delta*1j), 0, np.cos(theta13)]]
    U3=[[np.cos(theta12), np.sin(theta12), 0], [-np.sin(theta12), np.cos(theta12), 
     0], [0, 0, 1]]
    Phases=np.diag([np.exp(beta1*1j), np.exp(beta2*1j), 1])
    
    return np.matmul(np.matmul(U1,np.matmul(U2,U3)),Phases)

#leptons

me = 0.5109989461
Errme = 0.0000000031
mmu = 105.6583745
Errmmu = 0.0000024
mtau = 1776.86
Errmtau = 0.12

Mlmatrix = [[me,0,0],[0,mmu,0],[0,0,mtau]]

#Experimental Values

h = 6.58211899e-22 #Planck's reduced constant

#Pion

TauPion = 2.6033e-8 #Pion lifetime
DeltaTauPi = 0.0005e-8 #Uncertainty

TauNaturalPion = TauPion/h #Pion lifetime in natural units
DeltaTauNaturalPi = DeltaTauPi/h #Uncertainty

GammaXPPion = (1/TauNaturalPion) #Pion total decay rate
DeltaGammaXPPion = (DeltaTauNaturalPi/TauNaturalPion)*GammaXPPion #Uncertainty
#
# este e o valor do branching RATIO
#
GammaXPMuPion = 0.999877*GammaXPPion #Muon decay rate
#
# esta linha foi incluida para fazer o limite a partir da razao
# de pions em eletrons sobre pions em muons
#
#GammaXPMuPion = 0.994341*GammaXPPion #Muon decay rate
GammaXPEPion = 1.230e-4*GammaXPPion #Electron decay rate
#
# esta linha foi incluida para fazer o limite a partir da razao
# de pions em eletrons sobre pions em muons
#GammaXPEPion = 1.23255e-4*GammaXPPion #Electron decay rate

DeltaGammaMuXPPi = np.sqrt((0.0000004/0.999877)**2 + (DeltaGammaXPPion/GammaXPPion)**2)*GammaXPMuPion #Uncertainty
#
# esta linha foi incluida para fazer o limite a partir da razao
# de pions em eletrons sobre pions em muons

#DeltaGammaMuXPPi = np.sqrt((0.0043/0.994341)**2 + (DeltaGammaXPPion/GammaXPPion)**2)*GammaXPMuPion #Uncertainty

DeltaGammaEXPPi = np.sqrt((0.004e-4/(1.230e-4))**2 + (DeltaGammaXPPion/GammaXPPion)**2)*GammaXPEPion #Uncertainty
#DeltaGammaEXPPi = np.sqrt((0.0023e-4/(1.230e-4))**2 + (DeltaGammaXPPion/GammaXPPion)**2)*GammaXPEPion #Uncertainty

ExpDataGammaPi = (GammaXPEPion,DeltaGammaEXPPi,GammaXPMuPion,DeltaGammaMuXPPi)

BranchingRatioThPi = 1.2352e-4 #Ratio e/mu theory
ErrBranchingRatioThPi = 0.0001e-4 #Unc. ratio e/mu theory
BranchingRatioXPPi = 1.2327e-4 #Ratio e/mu
ErrBranchingRatioXPPi = 0.0023e-4 #Uncertainty

ExpDataBranchingPion = (BranchingRatioXPPi,ErrBranchingRatioXPPi)

#Kaon

TauK = 1.2380e-8
DeltaTauK = 0.0020e-8

TauNaturalK = TauK/h
DeltaTauNaturalK = DeltaTauK/h

GammaXPK = (1/TauNaturalK)
DeltaGammaXPK = (DeltaTauNaturalK/TauNaturalK)*GammaXPK

GammaXPMuK = 0.6356*GammaXPK
GammaXPEK = 1.582e-5*GammaXPK

DeltaGammaMuXPK = np.sqrt((0.0011/0.6356)**2 + (DeltaGammaXPK/GammaXPK)**2)*GammaXPMuK
DeltaGammaEXPK = np.sqrt((0.007e-5/(1.582e-5))**2 + (DeltaGammaXPK/GammaXPK)**2)*GammaXPEK

ExpDataGammaK = (GammaXPEK,DeltaGammaEXPK,GammaXPMuK,DeltaGammaMuXPK)

BranchingRatioThK = 2.477e-5 #Ratio e/mu theory
ErrBranchingRatioThK = 0.001e-5 #Unc. ratio e/mu theory
BranchingRatioXPK = 2.488e-5
ErrBranchingRatioXPK = 0.009e-5

ExpDataBranchingK = (BranchingRatioXPK,ErrBranchingRatioXPK)

#D Meson

TauD = 1040e-15
DeltaTauD = 7e-15

TauNaturalD = TauD/h
DeltaTauNaturalD = DeltaTauD/h

GammaXPD = (1/TauNaturalD)
DeltaGammaXPD = (DeltaTauNaturalD/TauNaturalD)*GammaXPD

GammaXPMuD = 3.74e-4*GammaXPD*(1-0.018) ##Corrections from PDG
GammaXPED = 0*GammaXPD
GammaXPTauD = 1.2e-3*GammaXPD*(1-0.018) ##Corrections from PDG

DeltaGammaMuXPD = np.sqrt((0.17e-4/3.74e-4)**2 + (DeltaGammaXPD/GammaXPD)**2)*GammaXPMuD
DeltaGammaEXPD = 8.8e-6*GammaXPD
DeltaGammaTauXPD = np.sqrt((0.27e-3/1.2e-3)**2 + (DeltaGammaXPD/GammaXPD)**2)*GammaXPTauD

ExpDataGammaD = (GammaXPED,DeltaGammaEXPD,GammaXPMuD,DeltaGammaMuXPD,GammaXPTauD,DeltaGammaTauXPD)

BranchingRatioXPD = GammaXPED/GammaXPMuD
ErrBranchingRatioXPD = DeltaGammaEXPD/GammaXPMuD

BranchingRatioMuTauXPD = GammaXPMuD/GammaXPTauD
ErrBranchingRatioMuTauXPD = np.sqrt((DeltaGammaMuXPD/GammaXPMuD)**2+(DeltaGammaTauXPD/GammaXPTauD)**2)*BranchingRatioMuTauXPD

ExpDataBranchingD = (BranchingRatioXPD,ErrBranchingRatioXPD,BranchingRatioMuTauXPD,ErrBranchingRatioMuTauXPD)

#Ds Meson

TauDs = 504e-15
DeltaTauDs = 4e-15

TauNaturalDs = TauDs/h
DeltaTauNaturalDs = DeltaTauDs/h

GammaXPDs = (1/TauNaturalDs)
DeltaGammaXPDs = (DeltaTauNaturalDs/TauNaturalDs)*GammaXPDs

GammaXPMuDs = 5.49e-3*GammaXPDs*(1-0.018) ##Corrections from PDG
GammaXPEDs = 0*GammaXPDs
GammaXPTauDs = 5.48e-2*GammaXPDs*(1-0.018) ##Corrections from PDG

DeltaGammaMuXPDs = np.sqrt((0.16e-3/5.49e-3)**2 + (DeltaGammaXPDs/GammaXPDs)**2)*GammaXPMuDs
DeltaGammaEXPDs = 8.3e-5*GammaXPDs
DeltaGammaTauXPDs = np.sqrt((0.23e-2/5.48e-2)**2 + (DeltaGammaXPDs/GammaXPDs)**2)*GammaXPTauDs

ExpDataGammaDs = (GammaXPEDs,DeltaGammaEXPDs,GammaXPMuDs,DeltaGammaMuXPDs,GammaXPTauDs,DeltaGammaTauXPDs)

BranchingRatioXPDs = GammaXPEDs/GammaXPMuDs
ErrBranchingRatioXPDs = DeltaGammaEXPDs/GammaXPMuDs

BranchingRatioMuTauXPDs = GammaXPMuDs/GammaXPTauDs
ErrBranchingRatioMuTauXPDs = np.sqrt((DeltaGammaMuXPDs/GammaXPMuDs)**2+(DeltaGammaTauXPDs/GammaXPTauDs)**2)*BranchingRatioMuTauXPDs

ExpDataBranchingDs = (BranchingRatioXPDs,ErrBranchingRatioXPDs,BranchingRatioMuTauXPDs,ErrBranchingRatioMuTauXPDs)

#B Meson

TauB = 1.638e-12
DeltaTauB = 0.004e-12

TauNaturalB = TauB/h
DeltaTauNaturalB = DeltaTauB/h

GammaXPB = (1/TauNaturalB)
DeltaGammaXPB = (DeltaTauNaturalB/TauNaturalB)*GammaXPB

GammaXPMuB = ((1.07e-6+2.9e-7)/2)*GammaXPB
GammaXPEB = 0*GammaXPB
GammaXPTauB = 1.09e-4*GammaXPB

DeltaGammaMuXPB = np.sqrt((((1.07e-6-2.9e-7)/2)/((1.07e-6+2.9e-7)/2))**2 + (DeltaGammaXPB/GammaXPB)**2)*GammaXPMuB
DeltaGammaEXPB = 9.8e-7*GammaXPB
DeltaGammaTauXPB = np.sqrt((0.24e-4/1.09e-4)**2 + (DeltaGammaXPB/GammaXPB)**2)*GammaXPTauB

ExpDataGammaB = (GammaXPEB,DeltaGammaEXPB,GammaXPMuB,DeltaGammaMuXPB,GammaXPTauB,DeltaGammaTauXPB)

BranchingRatioXPB = GammaXPEB/GammaXPMuB
ErrBranchingRatioXPB = DeltaGammaEXPB/GammaXPMuB

BranchingRatioMuTauXPB = GammaXPMuB/GammaXPTauB
ErrBranchingRatioMuTauXPB = np.sqrt((DeltaGammaMuXPB/GammaXPMuB)**2+(DeltaGammaTauXPB/GammaXPTauB)**2)*BranchingRatioMuTauXPB

ExpDataBranchingB = (BranchingRatioXPB,ErrBranchingRatioXPB,BranchingRatioMuTauXPB,ErrBranchingRatioMuTauXPB)

#B Anomaly

RSMD = 0.299
ErrRSMD = 0.003
RSMDExc = 0.258
ErrRSMDExc = 0.005

RDXP = 0.407
ErrRDXP = np.sqrt(0.039**2+0.024**2)
RDExcXP = 0.306
ErrRDExcXP = np.sqrt(0.013**2+0.007**2)

fBc = 427 #([Blanke]BAnomaly.pdf)

Vcb = 38.4e-3
ErrVcb = np.sqrt(0.7e-3**2+0.5e-3**2+1e-3**2)

#LFV limits

Gamma10 = 8e-3
