#!/usr/local/lib/python3
#
#  calculo da taxa de deciaimento de mesons escalares em leptons
# feito por Leonardo Leite
# acompanha o programa com os valores das taxas experimentais.
#
# coding:  utf-8
import os, sys

 
# sys.path.append('/usr/local/Cellar/')

"""
@author: leonardo
"""

import math as m
import numpy as np
import constants as ct
import sympy as spy
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd



# calculo das correcoes radiativas do decaimento pion em letpons
#
def L(z):
    I = integrate.quad(lambda t: -np.log(1 - t)/t, 0, z)
    return I[0]

def fL(z):
    t = spy.symbols('t')
    I = spy.integrate(-spy.log(1 - t)/t, (t,0,z))
    return I

def fF(z):
    
    F = 3/2*spy.log(z)+(13-19*z)/(8*(1-z))-(8-5*z)*z*spy.log(z)/(4*(1-z)**2)-(2+(1+z)*spy.log(z)/(1-z))*spy.log(1-z)-2*(1+z)*fL(1-z)/(1-z)

    return F

def fRad(alpha, mZ, mrho, c1, c2, c3, c4, ct2, mmes, ml,rad):
    
    if rad:
        Rad = (1+(2*alpha/np.pi)*spy.log(mZ/mrho))*(1+(alpha/np.pi)*fF(ml**2/mmes**2))*(1-(alpha/np.pi)*((3/2)*spy.log(mrho/mmes)+c1+(ml**2/mrho**2)*(c2*spy.log(mrho**2/ml**2)+c3+c4*(ml/mmes))-(mmes**2/mrho**2)*ct2*spy.log(mrho**2/ml**2)))
    else:
        Rad = 1

    return Rad

def F(z):
    
    F = 3/2*np.log(z)+(13-19*z)/(8*(1-z))-(8-5*z)*z*np.log(z)/(4*(1-z)**2)-(2+(1+z)*np.log(z)/(1-z))*np.log(1-z)-2*(1+z)*L(1-z)/(1-z)

    return F

def Rad(ml,mmes):
    
    alpha = ct.alpha
    mZ = ct.mZ
    mrho = ct.mrho
    if mmes == ct.mpi:
        c1 = -2.56
        c2 = 5.2
        c3 = -10.5
        c4 = 1.69
        ct2 = 0
    elif mmes == ct.mK:
        c1 = -1.98
        c2 = 4.3
        c3 = -4.73
        c4 = 0.22
        ct2 = 7.84e-2
    else:
        return 1
    
    Rad = (1+(2*alpha/np.pi)*np.log(mZ/mrho))*(1+(alpha/np.pi)*F(ml**2/mmes**2))*(1-(alpha/np.pi)*((3/2)*np.log(mrho/mmes)+c1+(ml**2/mrho**2)*(c2*np.log(mrho**2/ml**2)+c3+c4*(ml/mmes))-(mmes**2/mrho**2)*ct2*np.log(mrho**2/ml**2)))

    return Rad

def fgamma(mu,md,alpha,mZ,mrho,c1,c2,c3,c4,ct2,MW,GF,V,fP,mP,ml,x,rad):
    
    Delta = (mP**2/(mu+md))*x
    Gamma = fRad(alpha, mZ, mrho, c1, c2, c3, c4, ct2, mP, ml,rad)*(GF**2*V**2*fP**2/(8*np.pi))*mP*ml**2*(1-ml**2/mP**2)**2*spy.conjugate((1-Delta))*(1-Delta)
    
    return Gamma
#
# Taxa de decaimento de pions em leptons no BSM 
#
def gamma(mPs,fPs,Vs,mus,mds,mls,x):
    
    Delta = (mPs**2/(mls*(mus+mds)))*x/2
    Gamma = Rad(mls,mPs)*((ct.GF**2*Vs**2*fPs**2/(8*np.pi))*mPs*mls**2*(1-mls**2/mPs**2)**2)*((1-Delta)*np.conj(1-Delta))
    
    return Gamma

def deltachisq(meson,lepton,xs):
    
    if meson == "pion":
        mus = ct.mu
        mds = ct.md
        fPs = ct.fpi
        Vs = ct.Vud
        mPs = ct.mpi
        
        Errmus = ct.Errmu
        Errmds = ct.Errmd
        ErrfPs = ct.Errfpi
        ErrVs = ct.ErrVud
        ErrmPs = ct.Errmpi
        
        c1s = -2.56
        c2s = 5.2
        c3s = -10.5
        c4s = 1.69
        ct2s = 0
        
        Errc1s = 0.5
        Errc2s = np.sqrt(0.4**2+0.01**2)
        Errc3s = np.sqrt(2.3**2+0.53**2)
        Errc4s = 0.07
        Errct2s = 0
        
        rad = 1
        
        if lepton == "electron":
            
            mls = ct.me
            
            Errmls = ct.Errme
            
            Data = [ct.ExpDataGammaPi[0],ct.ExpDataGammaPi[1]]
            
        elif lepton == "muon":
            
            mls = ct.mmu
            
            Errmls = ct.Errmmu
            
            Data = [ct.ExpDataGammaPi[2],ct.ExpDataGammaPi[3]]
        
    elif meson == 'K':
        mus = ct.mu
        mds = ct.ms
        fPs = ct.fK
        Vs = ct.Vus
        mPs = ct.mK
        
        Errmus = ct.Errmu
        Errmds = ct.Errms
        ErrfPs = ct.ErrfK
        ErrVs = ct.ErrVus
        ErrmPs = ct.ErrmK
        
        c1s = -1.98
        c2s = 4.3
        c3s = -4.73
        c4s = 0.22
        ct2s = 7.84e-2
        
        Errc1s = 0.5
        Errc2s = np.sqrt(0.4**2+0.01**2)
        Errc3s = np.sqrt(2.3**2+0.28**2)
        Errc4s = 0.01
        Errct2s = 0.07e-2
        
        rad = 1
        
        if lepton == "electron":
            
            mls = ct.me
            
            Errmls = ct.Errme
            
            Data = [ct.ExpDataGammaK[0],ct.ExpDataGammaK[1]]
            
        elif lepton == "muon":
            
            mls = ct.mmu
            
            Errmls = ct.Errmmu
            
            Data = [ct.ExpDataGammaK[2],ct.ExpDataGammaK[3]]
            
    elif meson == 'D':
        mus = ct.mc
        mds = ct.md
        fPs = ct.fD
        Vs = ct.Vcd
        mPs = ct.mD
        
        Errmus = ct.Errmc
        Errmds = ct.Errmd
        ErrfPs = ct.ErrfD
        ErrVs = ct.ErrVcd
        ErrmPs = ct.ErrmD
        
        c1s = 0
        c2s = 0
        c3s = 0
        c4s = 0
        ct2s = 0
        
        Errc1s = 0
        Errc2s = 0
        Errc3s = 0
        Errc4s = 0
        Errct2s = 0
        
        rad = 0
        
        if lepton == "electron":
            
            mls = ct.me
            
            Errmls = ct.Errme
            
            Data = [ct.ExpDataGammaD[0],ct.ExpDataGammaD[1]]
            
        elif lepton == "muon":
            
            mls = ct.mmu
            
            Errmls = ct.Errmmu
            
            Data = [ct.ExpDataGammaD[2],ct.ExpDataGammaD[3]]
        else:
            
            mls = ct.mtau
            
            Errmls = ct.Errmtau
            
            Data = [ct.ExpDataGammaD[4],ct.ExpDataGammaD[5]]
        
    elif meson == 'Ds':
        mus = ct.mc
        mds = ct.ms
        fPs = ct.fDs
        Vs = ct.Vcs
        mPs = ct.mDs
        
        Errmus = ct.Errmc
        Errmds = ct.Errms
        ErrfPs = ct.ErrfDs
        ErrVs = ct.ErrVcs
        ErrmPs = ct.ErrmDs
        
        c1s = 0
        c2s = 0
        c3s = 0
        c4s = 0
        ct2s = 0
        
        Errc1s = 0
        Errc2s = 0
        Errc3s = 0
        Errc4s = 0
        Errct2s = 0
        
        rad = 0
        
        if lepton == "electron":
            
            mls = ct.me
            
            Errmls = ct.Errme
            
            Data = [ct.ExpDataGammaDs[0],ct.ExpDataGammaDs[1]]
            
        elif lepton == "muon":
            
            mls = ct.mmu
            
            Errmls = ct.Errmmu
            
            Data = [ct.ExpDataGammaDs[2],ct.ExpDataGammaDs[3]]
        else:
            
            mls = ct.mtau
            
            Errmls = ct.Errmtau
            
            Data = [ct.ExpDataGammaDs[4],ct.ExpDataGammaDs[5]]
    
    elif meson == 'B':
        mus = ct.mu
        mds = ct.mb
        fPs = ct.fB
        Vs = ct.Vub
        mPs = ct.mB
        
        Errmus = ct.Errmu
        Errmds = ct.Errmb
        ErrfPs = ct.ErrfB
        ErrVs = ct.ErrVub
        ErrmPs = ct.ErrmB
        
        c1s = 0
        c2s = 0
        c3s = 0
        c4s = 0
        ct2s = 0
        
        Errc1s = 0
        Errc2s = 0
        Errc3s = 0
        Errc4s = 0
        Errct2s = 0
        
        rad = 0
        
        if lepton == "electron":
            
            mls = ct.me
            
            Errmls = ct.Errme
            
            Data = [ct.ExpDataGammaB[0],ct.ExpDataGammaB[1]]
            
        elif lepton == "muon":
            
            mls = ct.mmu
            
            Errmls = ct.Errmmu
            
            Data = [ct.ExpDataGammaB[2],ct.ExpDataGammaB[3]]
        else:
            
            mls = ct.mtau
            
            Errmls = ct.Errmtau
            
            Data = [ct.ExpDataGammaB[4],ct.ExpDataGammaB[5]]
            
    mu,md,alpha,mZ,mrho,c1,c2,c3,c4,ct2,MW,GF,V,fP,mP,ml = spy.symbols('mu,md,alpha,mZ,mrho,c1,c2,c3,c4,ct2,MW,GF,V,fP,mP,ml',real=True)
    Errmu,Errmd,Erralpha,ErrmZ,Errmrho,Errc1,Errc2,Errc3,Errc4,Errct2,ErrMW,ErrGF,ErrV,ErrfP,ErrmP,Errml = spy.symbols('Errmu,Errmd,Erralpha,ErrmZ,Errmrho,Errc1,Errc2,Errc3,Errc4,Errct2,ErrMW,ErrGF,ErrV,ErrfP,ErrmP,Errml',real=True)
    
    x = spy.symbols('x')
    
    variables = [mu,md,alpha,mZ,mrho,c1,c2,c3,c4,ct2,MW,GF,V,fP,mP,ml]
    Errq = [Errmu,Errmd,Erralpha,ErrmZ,Errmrho,Errc1,Errc2,Errc3,Errc4,Errct2,ErrMW,ErrGF,ErrV,ErrfP,ErrmP,Errml]
    
    Err = 0
    
    for j in range(len(variables)):
        Err += ((spy.diff(fgamma(mu,md,alpha,mZ,mrho,c1,c2,c3,c4,ct2,MW,GF,V,fP,mP,ml,x,rad),variables[j]))*Errq[j])**2
    
    Value = spy.N(Err.subs([(mu,mus),(md,mds),(alpha,ct.alpha),(mZ,ct.mZ),(mrho,ct.mrho),(c1,c1s),(c2,c2s),(c3,c3s),(c4,c4s),(ct2,ct2s),(MW,ct.MW),(GF,ct.GF),(V,Vs),(fP,fPs),(mP,mPs),(ml,mls),(Errmu,Errmus),(Errmd,Errmds),(Erralpha,ct.Erralpha),(ErrmZ,ct.ErrmZ),(Errmrho,ct.Errmrho),(Errc1,Errc1s),(Errc2,Errc2s),(Errc3,Errc3s),(Errc4,Errc4s),(Errct2,Errct2s),(ErrMW,ct.ErrMW),(ErrGF,ct.ErrGF),(ErrV,ErrVs),(ErrfP,ErrfPs),(ErrmP,ErrmPs),(Errml,Errmls)]))

    args = x

    ErrRate = spy.lambdify(args,Value,modules='numpy')
    
    Gamma = np.real(gamma(mPs,fPs,Vs,mus,mds,mls,xs))
    
    #print(ErrRate(xs))
#
# esta taxa inclue os erros do modelo, erros experimentais e erros do MP
#
#    chisq = ((Gamma-Data[0])**2)/(np.real(ErrRate(xs))+Data[1]**2)
#
# esta taxa inclue os erros exoerimentais
#
    chisq=   ((Gamma-Data[0])**2)/(Data[1]**2)
# esta taxa inclue os  erros experimentais e erros do MP
#
    chisq=   ((Gamma-Data[0])**2)/(np.real(ErrRate(0))+Data[1]**2) 
    return chisq

log = 0

if log:
    # Limites para calcular os parâmetros (em escala log)
    
    xi = -4
    xf =-3
    
    # Número de pontos em cada eixo
    
    N = 1000
    
    # Eixos x e y para calcular o chi2
    
    # x = 10**np.arange(xi, xf+(xf-xi)/N, (xf-xi)/(N+2))
    # y = 10**np.arange(yi, yf+(yf-yi)/N, (yf-yi)/(N))
    
    x = 10**np.linspace(xi, xf, N)
    y = 10**np.linspace(xi, xf, N)
    X,Y = np.meshgrid(x,y)

else:
    # Limites para calcular os parâmetros (escala linear)
    
#    xi = 0
#    xf = 1.2e-3
    
#    yi = 0
#    yf = 0.8e-3

# para ver a elipse
        
    xi = -1.5e-1
    xf = 1.5e-1
    
    yi = -1e-1
    yf = 1e-1
    
    xi = -1.0e-4
    xf = 1.0e-3
    
    yi = -1.0e-3
    yf = 1.0e-3

        
    xi = -2.0e-3
    xf = 2.0e-3
    
    yi = -2.0e-3
    yf = 2.0e-3

#    xi = -5.0e-3
#    xf = 5.0e-3
    
#    yi = -5.0e-3
#    yf = 5.0e-3
    
    # Número de pontos em cada eixo
    
    N = 10000
    
    # Eixos x e y para calcular o chi2
    
    # x = 10**np.arange(xi, xf+(xf-xi)/N, (xf-xi)/(N+2))
    # y = 10**np.arange(yi, yf+(yf-yi)/N, (yf-yi)/(N))
    
    x = np.linspace(xi, xf, N)
    y = np.linspace(yi, yf, N)
    X,Y = np.meshgrid(x,y)

#levels1 = [0, 2.3, 6.18, 11.83]
#
# 90 % C.L. para dois parametros
#
levels1 =[0,4.61]
#level = [2.3]
#level1 = [2.3,6.18,11.83]
#levels = [0,2.3]
#fig, ax = plt.subplots(1,1)
#ax.plot(x,y)

tick_spacing = 0.01
#ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

plt.rc('text', usetex=True)
plt.rc('xtick',labelsize=40)
plt.rc('ytick',labelsize=40)

Unid = 1e3  # Parâmetro para reescalonar o gráfico se quiser trocar a unidad
#Unid = 1  # Parâmetro para reescalonar o gráfico se quiser trocar a unidade

file = open('intervalComplex.csv','w')

#file.write('\n Interval at 1 sigma for the GWP region\n\n')

#file.write('Meson,Min (MeV-1),Max (MeV-1),Central Value at GWP (MeV-1),ΔΧ² minimum at GWP\n')

mesondata = (ct.mesonpi,ct.ExpDataGammaPi)
#
#e este inclue a taxa pions into muons e eletrons entao
# seria epsilon_mue sendo  hermitiano
#
#TablePi = np.real(deltachisq('pion','electron',X+Y*1j)+deltachisq('pion','muon',X+Y*1j))
#
#e este inclue a taxa pions into muons entao seria epsilon_mue
#
# se voce incluir pions e muons, isto calcula o limite
# para epsilon_muX
TablePi = np.real(deltachisq('pion','muon',X+Y*1j))
TablePiR = np.real(deltachisq('pion','muon',x))
#
#print to file
#df = pd.DataFrame(TablePiR)
#df.to_csv('output.txt', sep='\t', index=False)
#e este inclue a taxa pions into eletrons entao seria epsilon_emu
#
#TablePi = np.real(deltachisq('pion','electron',X+Y*1j))
ind = np.unravel_index(np.argmin(TablePi, axis=None), TablePi.shape)
chimin = TablePi[ind[0],ind[1]]
DeltaTable = TablePi - chimin
Chi2 = DeltaTable
#
#print to file
ind2 = np.unravel_index(np.argmin(TablePiR, axis=None), TablePiR.shape)
chimin2 = TablePiR[ind2[0]]
deltaTab2 = TablePiR-chimin2
data = {
    'Var': x,
    'Chi2': deltaTab2
    }
df2 = pd.DataFrame(data)
df2.to_csv('output2.txt', sep='\t', index=False)

#%% Plot

colors = ['navy','darkgoldenrod','lime']
colors.reverse()
fig1, ax1 = plt.subplots(figsize=(16,16))
#    if Chi2<4.61
    
#K1s2 = x[Chi2<1]
#xaxisK1s2 = np.zeros(len(K1s2))+4.61
#file = open('saida.csv','w')
#file.write('K,%.7f,%.7f,%.7f,%.7f\n' %(chi2,xaxisK1s2,x*ind[0],y*ind[1]))


mesondata = (ct.mesonpi,ct.ExpDataGammaPi)
theplot=plt.contourf(X*Unid,Y*Unid,Chi2,levels1,alpha=1,colors=colors)
Radius = Unid*(ct.mu+ct.md)/ct.mpi**2
#
# Mostra o ponto de best fit, eu temporiamente desliguei isto.
#
#plot2 = plt.contour(X*Unid, Y*Unid, ((X*Unid-Radius)**2 + (Y*Unid)**2 - Radius**2), [0],linewidths=5,linestyles='dashed',colors='red')
smplot=plt.scatter(Unid*x[ind[1]],Unid*y[ind[0]],s=600,c='r',marker='*',zorder=10)
ax1.set_xlabel(r"$\Re \epsilon_{e\mu}\,(10^{-3})$",fontsize=40)
if log:
    ax1.set_yscale('log')
ax1.set_ylabel(r"$\Im \epsilon_{e\mu}\, (10^{-3})$",fontsize=40)
if log:
    ax1.set_xscale('log')
ax1.set_title(r'$\pi$',fontsize=36)
ax1.grid(True)

proxy=[plt.Rectangle((0,0),1,1,fc=fc.get_facecolor()[0])
        for fc in theplot.collections]

#plt.legend([smplot]+proxy,[r'Best fit',r'$1\sigma$',r'$2\sigma$',r'$3\sigma$'],fontsize=28,loc='lower left',framealpha=0.9,fancybox=True)


plt.show()

"""
mesondata = (ct.mesonK,ct.ExpDataGammaK)
TableK = deltachisq('K','electron',x)+deltachisq('K','muon',x)
ind = np.unravel_index(np.argmin(TableK, axis=None), TableK.shape)
chimin = TableK[ind[0]]
DeltaTable = TableK - chimin
Chi2 = DeltaTable

KBF2 = x[Chi2 == 0]
xaxisKBF2 = np.zeros(len(KBF2))+1

K1s2 = x[Chi2<1]
xaxisK1s2 = np.zeros(len(K1s2))+1

K2s2 = x[Chi2<4]
xaxisK2s2 = np.zeros(len(K2s2))+1

K3s2 = x[Chi2<9]
xaxisK3s2 = np.zeros(len(K3s2))+1

plt.scatter(xaxisK3s2,K3s2,marker='s',s=100,c=colors[0])

plt.scatter(xaxisK2s2,K2s2,marker='s',s=100,c=colors[1])

plt.scatter(xaxisK1s2,K1s2,marker='s',s=100,c=colors[2])

plt.scatter(xaxisKBF2,KBF2,marker='*',s=400,c='r')

interv2K = np.amax(K1s2)
proxer = K1s2[K1s2>1e-4]
interv1K = np.amin(proxer)
proxer2 = Chi2[x>1e-4]
proxerx = x[x>1e-4]
ind = np.unravel_index(np.argmin(proxer2, axis=None), proxer2.shape)
chinmin = proxer2[ind[0]]
centerK = proxerx[ind[0]]

file.write('K,%.7f,%.7f,%.7f,%.7f\n' %(interv1K,interv2K,centerK,chinmin))

mesondata = (ct.mesonD,ct.ExpDataGammaD)
TableD = deltachisq('D','electron',x)+deltachisq('D','muon',x)+deltachisq('D','tau',x)
ind = np.unravel_index(np.argmin(TableD, axis=None), TableD.shape)
chimin = TableD[ind[0]]
DeltaTable = TableD - chimin
Chi2 = DeltaTable

DBF2 = x[Chi2 == 0.0]

D1s2 = x[Chi2<1]
xaxisD1s2 = np.zeros(len(D1s2))+2

D2s2 = x[Chi2<4]
xaxisD2s2 = np.zeros(len(D2s2))+2

D3s2 = x[Chi2<9]
xaxisD3s2 = np.zeros(len(D3s2))+2

plt.scatter(xaxisD3s2,D3s2,marker='s',s=100,c=colors[0])

plt.scatter(xaxisD2s2,D2s2,marker='s',s=100,c=colors[1])

plt.scatter(xaxisD1s2,D1s2,marker='s',s=100,c=colors[2])

plt.scatter(2,DBF2,marker='*',s=400,c='r')

interv2D = np.amax(D1s2)
proxer = D1s2[D1s2>1e-4]
interv1D = np.amin(proxer)
proxer2 = Chi2[x>1e-4]
proxerx = x[x>1e-4]
ind = np.unravel_index(np.argmin(proxer2, axis=None), proxer2.shape)
chinmin = proxer2[ind[0]]
centerD = proxerx[ind[0]]

file.write('D,%.7f,%.7f,%.7f,%.7f\n' %(interv1D,interv2D,centerD,chinmin))

mesondata = (ct.mesonDs,ct.ExpDataGammaDs)
TableDs = deltachisq('Ds','electron',x)+deltachisq('Ds','muon',x)+deltachisq('Ds','tau',x)
ind = np.unravel_index(np.argmin(TableDs, axis=None), TableDs.shape)
chimin = TableDs[ind[0]]
DeltaTable = TableDs - chimin
Chi2 = DeltaTable

DsBF2 = x[Chi2 == 0.0]

Ds1s2 = x[Chi2<1]
xaxisDs1s2 = np.zeros(len(Ds1s2))+3

Ds2s2 = x[Chi2<4]
xaxisDs2s2 = np.zeros(len(Ds2s2))+3

Ds3s2 = x[Chi2<9]
xaxisDs3s2 = np.zeros(len(Ds3s2))+3

plt.scatter(xaxisDs3s2,Ds3s2,marker='s',s=100,c=colors[0])

plt.scatter(xaxisDs2s2,Ds2s2,marker='s',s=100,c=colors[1])

plt.scatter(xaxisDs1s2,Ds1s2,marker='s',s=100,c=colors[2])

plt.scatter(3,DsBF2,marker='*',s=400,c='r')

interv2Ds = np.amax(Ds1s2)
proxer = Ds1s2[Ds1s2>1e-4]
interv1Ds = np.amin(proxer)
proxer2 = Chi2[x>1e-4]
proxerx = x[x>1e-4]
ind = np.unravel_index(np.argmin(proxer2, axis=None), proxer2.shape)
chinmin = proxer2[ind[0]]
centerDs = proxerx[ind[0]]

file.write('Ds,%.7f,%.7f,%.7f,%.7f\n' %(interv1Ds,interv2Ds,centerDs,chinmin))

mesondata = (ct.mesonB,ct.ExpDataGammaB)
TableB = deltachisq('B','electron',x)+deltachisq('B','muon',x)+deltachisq('B','tau',x)
ind = np.unravel_index(np.argmin(TableB, axis=None), TableB.shape)
chimin = TableB[ind[0]]
DeltaTable = TableB - chimin
Chi2 = DeltaTable

BBF2 = x[Chi2 == 0.0]

B1s2 = x[Chi2<1]
xaxisB1s2 = np.zeros(len(B1s2))+4

B2s2 = x[Chi2<4]
xaxisB2s2 = np.zeros(len(B2s2))+4

B3s2 = x[Chi2<9]
xaxisB3s2 = np.zeros(len(B3s2))+4

plt.scatter(xaxisB3s2,B3s2,marker='s',s=100,c=colors[0])

plt.scatter(xaxisB2s2,B2s2,marker='s',s=100,c=colors[1])

plt.scatter(xaxisB1s2,B1s2,marker='s',s=100,c=colors[2])

plt.scatter(4,BBF2,marker='*',s=400,c='r')

interv2B = np.amax(B1s2)
proxer = B1s2[B1s2>1e-4]
interv1B = np.amin(proxer)
proxer2 = Chi2[x>1e-4]
proxerx = x[x>1e-4]
ind = np.unravel_index(np.argmin(proxer2, axis=None), proxer2.shape)
chinmin = proxer2[ind[0]]
centerB = proxerx[ind[0]]

file.write('B,%.7f,%.7f,%.7f,%.7f\n' %(interv1B,interv2B,centerB,chinmin))

ChiTotComb2 = TablePi+TableK+TableD+TableDs+TableB
ind = np.unravel_index(np.argmin(ChiTotComb2, axis=None), ChiTotComb2.shape)
chimin = ChiTotComb2[ind[0]]
DeltaChiTotComb2 = ChiTotComb2 - chimin
Chi = DeltaChiTotComb2

CombBF = x[Chi == 0]

Comb1s = x[Chi<1]
xaxisComb1s = np.zeros(len(Comb1s))+5

Comb2s = x[Chi<4]
xaxisComb2s = np.zeros(len(Comb2s))+5

Comb3s = x[Chi<9]
xaxisComb3s = np.zeros(len(Comb3s))+5

plt.scatter(xaxisComb3s,Comb3s,marker='s',s=100,c=colors[0],label='$3\sigma$')

plt.scatter(xaxisComb2s,Comb2s,marker='s',s=100,c=colors[1],label='$2\sigma$')

plt.scatter(xaxisComb1s,Comb1s,marker='s',s=100,c=colors[2],label='$1\sigma$')

plt.scatter(5,CombBF,marker='*',s=400,c='r',label='Best fit')

legend1 = plt.legend(fontsize=25,loc='lower right',framealpha=0.4,fancybox=True)

labels = [r'$\pi$',r'$K$',r'$D$',r'$D_s$',r'$B$',r'Combined']

plt.xlim(-1,7)
#plt.ylim(1e-7,1e-1)
#plt.ylim(2e-4,1.4e-3)
plt.xticks([0, 1, 2, 3, 4,5], labels)
ax1.minorticks_on()
ax1.grid(True,axis='y')
ax1.set_xlabel(r"Meson",fontsize=30)
ax1.set_yscale('log')
#ax1.set_ylabel(r"$(G^P_{\eta}/G_{F}) U^{-1} m_l^{-1} (\mathrm{MeV}^{-1})$",fontsize=30)
ax1.set_ylabel(r"$a^P/G_F\, (\mathrm{MeV}^{-1})$",fontsize=30)
ax1.set_title('Allowed region with GWP hypothesis',fontsize=30)
ax1.add_artist(legend1)

plt.show()

"""
file.close()
