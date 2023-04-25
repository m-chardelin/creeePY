#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 11:26:06 2021

@author: antoinemaitre
"""

import numpy as np
import matplotlib.pyplot as plt


"""Construction du profil rhéologique du gabbro du Queyras"""


'Gradient géothermique'

z = np.arange(0,100,0.1)             #Profondeur (km)
q = 15*10**(-3)                      #Chaleur (J = N.m)
T = (q*(z*10**3))+273                #Température (K)



"""Comportement fragile - Byerlee"""

'Pression lithostatique'

rho = 3300                           #Masse volumique (kg/m3)

g = 9.81                             #Accélération de pesanteur (m/s2)
Plith = rho*g*(z*10**3)              #Pression lithostatique (Pa)
mu = 0.6                             #Coefficient de friction (/)
pf=0.9                               #Pression fluide (comprise entre 0 et 1)

taub = (mu*Plith*(1-pf))*10**(-6)    #Contrainte déviatorique (MPa)



"""Comportement ductile - fluage dislocation"""

'Albite'

n = 3                       #Exposant de contrainte (/)
logA1 = 3.4
A1 = 10**logA1              #Constante différente chaque phase minérale (MPa)
#fH2O= 0.2                  #Pourcentage d'H2O (wt%)
Q = 332*10**3               #Énergie d'activation (J.mol^(-1))
R = 8.314                   #Constante des gaz parfaits ((kPa.L)/(mol.K))
strainrate = 10**(-14)      #Taux de déformation (s-1)

taud1 = (strainrate/A1)**(1/n)*np.exp(Q/(R*T*n))    #Contrainte déviatorique (MPa)


# 'Anorthite 1'
    
# n = 3                       #Exposant de contrainte (/)
# logA2 = 12.7
# A2 = 10**logA2              #Constante différente chaque phase minérale (MPa)
# #fH2O= 0.2                  #Pourcentage d'H2O (wt%)
# Q = 648*10**3               #Énergie d'activation (J.mol^(-1))
# R = 8.314                   #Constante des gaz parfaits ((kPa.L)/(mol.K))
# strainrate = 10**(-14)      #Taux de déformation (s-1)

# taud2 = (strainrate/A2)**(1/n)*np.exp(Q/(R*T*n))    #Contrainte déviatorique (MPa)

# 'Anorthite 2'

# n = 3                       #Exposant de contrainte (/)
# logA3 = 2.6
# A3 = 10**logA3              #Constante différente chaque phase minérale (MPa)
# #fH2O= 0.2                  #Pourcentage d'H2O (wt%)
# Q = 356*10**3               #Énergie d'activation (J.mol^(-1))
# R = 8.314                   #Constante des gaz parfaits ((kPa.L)/(mol.K))
# strainrate = 10**(-14)      #Taux de déformation (s-1)

# taud3 = (strainrate/A3)**(1/n)*np.exp(Q/(R*T*n))    #Contrainte déviatorique (MPa)


'Clinopyroxène (diospide wet)'

n = 5.5                     #Exposant de contrainte (/)
logA4 = 0.8 
A4 = 10**logA4              #Constante différente chaque phase minérale (MPa)
#fH2O= 0.2                  #Pourcentage d'H2O (wt%)
Q = 534*10**3               #Énergie d'activation (J.mol^(-1))
R = 8.314                   #Constante des gaz parfaits ((kPa.L)/(mol.K))
strainrate = 10**(-14)      #Taux de déformation (s-1)

taud4 = (strainrate/A4)**(1/n)*np.exp(Q/(R*T*n))    #Contrainte déviatorique (MPa)


'Amphibole'

#n = 3
#logA5 =
#A5 = 10**logA5
#fH2O= 0.2
#Q = 
#R = 8.314
#strainrate = 10**(-14)      #Taux de déformation (s-1)

#taud5 = (strainrate/A5)**(1/n)*np.exp(Q/(R*T*n))    #Contrainte déviatorique (MPa)


"""Représentation"""


'Profil rhéologique (Loi de fluage - Profondeur)'

plt.figure(1)       

#Loi de Byerlee :

#plt.plot(taub,-z,'black', label='Loi de Byerlee', linewidth = 2)

#Loi de fluage : Albite - Arnothite 1 - Anorthite 2 - Clinopyroxène :
    
#plt.plot(taud1,-z,'-g',label='Albite wet', linewidth = 2)
#plt.plot(taud2,-z,'--b',label='Anorthite 1',linewidth = 1)
#plt.plot(taud3,-z,'--g',label ='Anorthite 2',linewidth = 1)
#plt.plot(taud4,-z,'-r',label='Clinopyroxène',linewidth = 2)
#plt.plot(T-273, -z,'b')

plt.legend(loc = 'lower right')
plt.grid()
plt.xlim(0,200)
plt.ylim (-100,0)
plt.xlabel('Contrainte déviatorique (MPa)') ; plt.ylabel('Profondeur (km)')
plt.title("Profil rhéologique")


'Géotherme'

plt.figure(2)   
    
plt.plot(T-273, -z,'r')

plt.xlabel('Température (°C)') ; plt.ylabel('Profondeur (km)')
plt.title("Géotherme")
plt.grid()
plt.legend()


'Loi de fluage'

plt.figure(3)

plt.plot(T-273,taud1,'-y',label='Albite wet')
#plt.plot(T-273,taud2,'--b',label='Anorthite 1')
#plt.plot(T-273,taud3,'--g',label ='Anorthite 2')
plt.plot(T-273,taud4,'-r',label='Clinopyroxène')

plt.ylim(0,800)
plt.grid()
plt.legend(loc = 'upper right')
plt.xlabel('Température (°C)') ; plt.ylabel('Contrainte déviatorique (MPa)')
plt.title("Lois de fluage")
















